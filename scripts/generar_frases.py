"""Asks an AI model for new weather phrases in rioplatense slang and adds them to frases/frases.json.

Runs from .github/workflows/frases-ia.yml with GitHub Models (free, uses the workflow's own GITHUB_TOKEN with the
models: read permission; no extra account or key). MODELO picks the model, NUEVAS_POR_RANGO how many to ask for.
"""
import json
import os
import sys
import urllib.error
import urllib.request

import frases

URL = "https://models.github.ai/inference/chat/completions"
MODELO = os.environ.get("MODELO", "openai/gpt-4.1-mini")
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


def preguntar(token, data):
    cuerpo = {
        "model": MODELO,
        "temperature": 1.0,
        "max_tokens": 4000,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "system", "content": SISTEMA}, {"role": "user", "content": pedido(data)}],
    }
    req = urllib.request.Request(URL, data=json.dumps(cuerpo).encode(), method="POST", headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(req, timeout=120) as r:
        respuesta = json.loads(r.read().decode())
    return json.loads(respuesta["choices"][0]["message"]["content"])["frases"]


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Falta GITHUB_TOKEN (la Action necesita el permiso models: read).")
        return 1
    data = frases.cargar()
    try:
        nuevas = preguntar(token, data)
    except urllib.error.HTTPError as e:
        detalle = e.read().decode(errors="replace")[:300]
        if e.code == 429:
            print(f"Límite gratis de GitHub Models alcanzado; se reintenta la próxima vez. {detalle}")
            return 0
        print(f"GitHub Models respondió {e.code}: {detalle}")
        return 1
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"No se pudo conectar con GitHub Models: {e}")
        return 1
    except (KeyError, IndexError, json.JSONDecodeError, TypeError):
        print("La respuesta no vino en el formato esperado.")
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
