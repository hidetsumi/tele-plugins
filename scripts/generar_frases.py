"""Asks Google Gemini (free tier) for new weather phrases in rioplatense slang and adds them to frases/frases.json.

Runs from .github/workflows/frases-ia.yml. Needs the GEMINI_API_KEY secret (a free key from
https://aistudio.google.com/apikey). MODELO picks a model; by default the newest stable "flash" model the key can use.
NUEVAS_POR_RANGO sets how many phrases to ask for per range.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

import frases

API = "https://generativelanguage.googleapis.com/v1beta"
NUEVAS_POR_RANGO = int(os.environ.get("NUEVAS_POR_RANGO", "2"))

SISTEMA = f"""Escribís frases cortas para el widget del clima de una tele en Buenos Aires.
Se muestran después de la sensación térmica, por ejemplo: "30° Hace un re lorca".

Cómo tienen que ser:
- Castellano rioplatense de la calle, con voseo y lunfardo (che, re, posta, birra, lorca, joya, bondi, laburo).
- Graciosas y con onda, como las diría un amigo porteño. Pueden ser un poco zarpadas, pero sin insultar a nadie ni a ningún grupo.
- Que tengan que ver con el clima del rango y con la vida en Buenos Aires (mate, pileta, subte, asado, colectivo, laburo).
- Máximo {frases.LARGO_MAXIMO} caracteres cada una. Sin comillas, sin emojis, sin punto final.
- Que no repitan ni parafraseen las que ya existen.

Respondé solo con JSON, así: {{"frases": [{{"rango": "<uno de los rangos>", "texto": "<la frase>"}}]}}
Los rangos válidos son exactamente: {", ".join(frases.RANGOS)}."""


def pedido(data):
    partes = [f"Escribí {NUEVAS_POR_RANGO} frases nuevas para cada rango. Estas son las que ya existen:\n"]
    for rango in frases.RANGOS:
        partes.append(f"## {rango} ({frases.DESCRIPCION[rango]})")
        partes.extend(f"- {f['texto']}" for f in data["rangos"][rango])
        partes.append("")
    return "\n".join(partes)


def llamar(clave, ruta, cuerpo=None):
    req = urllib.request.Request(
        f"{API}/{ruta}",
        data=None if cuerpo is None else json.dumps(cuerpo).encode(),
        method="GET" if cuerpo is None else "POST",
        headers={"x-goog-api-key": clave, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def elegir_modelo(clave):
    """MODELO if set; else the newest stable flash model this key can call (names change as Google releases)."""
    if os.environ.get("MODELO"):
        return os.environ["MODELO"]
    candidatos = []
    for m in llamar(clave, "models?pageSize=200").get("models", []):
        nombre = m.get("name", "").removeprefix("models/")
        if "generateContent" not in m.get("supportedGenerationMethods", []):
            continue
        if "flash" not in nombre or re.search(r"lite|preview|exp|image|tts|audio|live|thinking|latest", nombre):
            continue
        version = re.search(r"gemini-(\d+(?:\.\d+)?)", nombre)
        if version:
            candidatos.append((float(version.group(1)), nombre))
    if not candidatos:
        raise RuntimeError("no hay ningún modelo flash disponible para esta clave")
    return max(candidatos)[1]


def preguntar(clave, modelo, data):
    respuesta = llamar(clave, f"models/{modelo}:generateContent", {
        "systemInstruction": {"parts": [{"text": SISTEMA}]},
        "contents": [{"role": "user", "parts": [{"text": pedido(data)}]}],
        "generationConfig": {"temperature": 1.0, "responseMimeType": "application/json"},
    })
    try:
        texto = "".join(p.get("text", "") for p in respuesta["candidates"][0]["content"]["parts"])
        return json.loads(texto)["frases"]
    except (KeyError, IndexError, json.JSONDecodeError, TypeError):
        print(f"Respuesta recibida: {json.dumps(respuesta, ensure_ascii=False)[:500]}")
        raise


def main():
    clave = os.environ.get("GEMINI_API_KEY")
    if not clave:
        print("Falta el secreto GEMINI_API_KEY: no se generan frases.")
        return 0
    data = frases.cargar()
    try:
        modelo = elegir_modelo(clave)
        print(f"Modelo: {modelo}")
        nuevas = preguntar(clave, modelo, data)
    except urllib.error.HTTPError as e:
        detalle = e.read().decode(errors="replace")[:300]
        if e.code == 429:
            print(f"Límite gratis de Gemini alcanzado; se reintenta la próxima vez. {detalle}")
            return 0
        print(f"Gemini respondió {e.code}: {detalle}")
        return 1
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"No se pudo conectar con Gemini: {e}")
        return 1
    except (KeyError, IndexError, json.JSONDecodeError, TypeError, RuntimeError) as e:
        print(f"La respuesta no vino en el formato esperado ({e}).")
        return 1

    agregadas = 0
    for f in nuevas:
        if not isinstance(f, dict):
            continue
        error = frases.agregar(data, f.get("rango", ""), f.get("texto", ""), "ia")
        if error:
            print(f"Descartada ({error}): {f.get('texto')}")
        else:
            agregadas += 1
            print(f"+ [{f['rango']}] {frases.limpiar(f['texto'])}")
    if agregadas:
        frases.guardar(data)
    print(f"{agregadas} frases nuevas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
