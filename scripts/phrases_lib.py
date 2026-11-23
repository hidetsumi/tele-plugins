"""Shared helpers for phrases/phrases.json (schema version 2).

Each category has a stable id, a human label, a condition (feels-like range in °C, or a weather type) and its
phrases. The TV reads the conditions from the file, so ranges can change without updating the TV.
"""
import datetime
import json
import pathlib
import unicodedata

FILE = pathlib.Path(__file__).resolve().parent.parent / "phrases" / "phrases.json"
SCHEMA_VERSION = 2
# The pill on the TV fits about this many characters after the temperature.
MAX_LENGTH = 40
# Per category: past this, the oldest AI phrases make room for new ones. Manual phrases are never removed.
MAX_PER_CATEGORY = 40
SOURCES = ("manual", "ai")


def load():
    data = json.loads(FILE.read_text(encoding="utf-8"))
    if data.get("schemaVersion") != SCHEMA_VERSION:
        raise ValueError(f"expected schemaVersion {SCHEMA_VERSION}, found {data.get('schemaVersion')}")
    return data


def save(data):
    data["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def category(data, key):
    """A category by id or by label (the issue form shows labels)."""
    for c in data["categories"]:
        if key in (c["id"], c["label"]):
            return c
    return None


def describe(c):
    """The condition in words, for the AI prompt."""
    cond = c["condition"]
    if "weather" in cond:
        return f"weather is {cond['weather']}"
    low, high = cond.get("feelsLikeMin"), cond.get("feelsLikeMax")
    if low is not None and high is not None:
        return f"feels-like temperature {low}–{high} °C"
    if low is not None:
        return f"feels-like temperature {low} °C or more"
    return f"feels-like temperature {high} °C or less"


def normalize(text):
    """For spotting repeats: no accents, no punctuation, lower case, single spaces."""
    t = unicodedata.normalize("NFKD", text)
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = "".join(ch if ch.isalnum() else " " for ch in t.lower())
    return " ".join(t.split())


def clean(text):
    return " ".join(str(text).split()).strip().strip('"').strip()


def add(data, key, text, source):
    """Adds one phrase. Returns None when added, or the reason it was not."""
    c = category(data, key)
    text = clean(text)
    if c is None:
        return f'category "{key}" does not exist'
    if source not in SOURCES:
        return f'source "{source}" is not one of {SOURCES}'
    if not text:
        return "the phrase is empty"
    if len(text) > MAX_LENGTH:
        return f"the phrase is {len(text)} characters long; the maximum is {MAX_LENGTH}"
    existing = {normalize(p["text"]) for cat in data["categories"] for p in cat["phrases"]}
    if normalize(text) in existing:
        return "that phrase already exists"
    phrases = c["phrases"]
    phrases.append({"text": text, "source": source, "addedAt": datetime.date.today().isoformat()})
    while len(phrases) > MAX_PER_CATEGORY:
        ai = [p for p in phrases if p["source"] == "ai"]
        if not ai:
            break
        phrases.remove(min(ai, key=lambda p: p["addedAt"]))
    return None
