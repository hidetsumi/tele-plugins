"""Asks Google Gemini (free tier) for new weather phrases and adds them to phrases/phrases.json.

Runs from .github/workflows/ai-phrases.yml. Needs the GEMINI_API_KEY secret (a free key from
https://aistudio.google.com/apikey). GEMINI_MODEL pins a model; by default the newest stable "flash" models the key
can use are tried in turn. PHRASES_PER_CATEGORY sets how many new phrases to ask for per category.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

import phrases_lib

API = "https://generativelanguage.googleapis.com/v1beta"
PER_CATEGORY = int(os.environ.get("PHRASES_PER_CATEGORY", "2"))
TRANSIENT = {429, 500, 502, 503, 504}

STYLE_GUIDE = phrases_lib.FILE.parent / "style-guide.md"


def system_prompt():
    """The style guide (phrases/style-guide.md) is the instruction; the reply format is fixed by RESPONSE_SCHEMA."""
    return STYLE_GUIDE.read_text(encoding="utf-8").replace("{max_length}", str(phrases_lib.MAX_LENGTH))


def response_schema(data):
    """Gemini must answer in this shape, and only with category ids that exist."""
    return {
        "type": "OBJECT",
        "properties": {
            "phrases": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "category": {"type": "STRING", "enum": [c["id"] for c in data["categories"]]},
                        "text": {"type": "STRING", "maxLength": phrases_lib.MAX_LENGTH},
                    },
                    "required": ["category", "text"],
                },
            }
        },
        "required": ["phrases"],
    }


def request_text(data):
    parts = [f"Write {PER_CATEGORY} new phrases for each category below, following the style guide. "
             "Each category lists its condition and the phrases that already exist; do not repeat them.\n"]
    for c in data["categories"]:
        parts.append(f"## {c['id']} ({phrases_lib.describe(c)})")
        parts.extend(f"- {p['text']}" for p in c["phrases"])
        parts.append("")
    return "\n".join(parts)


def call(key, path, body=None):
    req = urllib.request.Request(
        f"{API}/{path}",
        data=None if body is None else json.dumps(body).encode(),
        method="GET" if body is None else "POST",
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def models(key):
    """GEMINI_MODEL if set; else the stable flash models this key can call, newest first."""
    if os.environ.get("GEMINI_MODEL"):
        return [os.environ["GEMINI_MODEL"]]
    candidates = []
    for m in call(key, "models?pageSize=200").get("models", []):
        name = m.get("name", "").removeprefix("models/")
        if "generateContent" not in m.get("supportedGenerationMethods", []):
            continue
        if "flash" not in name or re.search(r"lite|preview|exp|image|tts|audio|live|thinking|latest", name):
            continue
        version = re.search(r"gemini-(\d+(?:\.\d+)?)", name)
        if version:
            candidates.append((float(version.group(1)), name))
    if not candidates:
        raise RuntimeError("no flash model is available for this key")
    return [name for _, name in sorted(candidates, reverse=True)]


def ask(key, model, data):
    reply = call(key, f"models/{model}:generateContent", {
        "systemInstruction": {"parts": [{"text": system_prompt()}]},
        "contents": [{"role": "user", "parts": [{"text": request_text(data)}]}],
        "generationConfig": {
            "temperature": 0.9,
            "responseMimeType": "application/json",
            "responseSchema": response_schema(data),
        },
    })
    try:
        text = "".join(p.get("text", "") for p in reply["candidates"][0]["content"]["parts"])
        return json.loads(text)["phrases"]
    except (KeyError, IndexError, json.JSONDecodeError, TypeError):
        print(f"Unexpected reply: {json.dumps(reply, ensure_ascii=False)[:500]}")
        raise


def ask_with_retries(key, data):
    """Busy or rate-limited models are common on the free tier: retry, then try the next flash model."""
    last = None
    for model in models(key)[:3]:
        for wait in (0, 15, 45):
            time.sleep(wait)
            try:
                print(f"Model: {model}")
                return ask(key, model, data)
            except urllib.error.HTTPError as e:
                if e.code not in TRANSIENT:
                    raise
                last = e
                print(f"  {model} returned {e.code}, retrying")
    raise last


def main():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("GEMINI_API_KEY is not set; no phrases generated.")
        return 0
    data = phrases_lib.load()
    try:
        new = ask_with_retries(key, data)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        if e.code in TRANSIENT:
            print(f"Gemini is busy or out of free quota ({e.code}); trying again next run. {detail}")
            return 0
        print(f"Gemini returned {e.code}: {detail}")
        return 1
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"Could not reach Gemini: {e}")
        return 1
    except (KeyError, IndexError, json.JSONDecodeError, TypeError, RuntimeError) as e:
        print(f"The reply was not in the expected format ({e}).")
        return 1

    added = 0
    for p in new:
        if not isinstance(p, dict):
            continue
        error = phrases_lib.add(data, p.get("category", ""), p.get("text", ""), "ai")
        if error:
            print(f"Skipped ({error}): {p.get('text')}")
        else:
            added += 1
            print(f"+ [{p['category']}] {phrases_lib.clean(p['text'])}")
    if added:
        phrases_lib.save(data)
    print(f"{added} new phrases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
