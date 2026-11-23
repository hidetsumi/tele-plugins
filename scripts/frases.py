"""Shared helpers for frases/frases.json: the weather phrases the TV shows next to the feels-like temperature."""
import json
import pathlib
import unicodedata

ARCHIVO = pathlib.Path(__file__).resolve().parent.parent / "frases" / "frases.json"

# Same names and order as the TV's weather add-on. Changing one here means changing it on the TV too.
RANGOS = [
    "35° o más", "30° a 34°", "25° a 29°", "19° a 24°", "13° a 18°", "7° a 12°", "6° o menos",
    "Lluvia", "Tormenta", "Nieve",
]
# What each range means, for people and for the AI prompt.
DESCRIPCION = {
    "35° o más": "sensación térmica de 35 °C o más: calor insoportable",
    "30° a 34°": "sensación térmica de 30 a 34 °C: mucho calor",
    "25° a 29°": "sensación térmica de 25 a 29 °C: calorcito lindo",
    "19° a 24°": "sensación térmica de 19 a 24 °C: clima ideal",
    "13° a 18°": "sensación térmica de 13 a 18 °C: fresco",
    "7° a 12°": "sensación térmica de 7 a 12 °C: frío",
    "6° o menos": "sensación térmica de 6 °C o menos: mucho frío",
    "Lluvia": "está lloviendo o lloviznando",
    "Tormenta": "hay tormenta eléctrica",
    "Nieve": "está nevando (rarísimo en Buenos Aires)",
}
# The pill on the TV fits about this many characters after the temperature.
LARGO_MAXIMO = 40
# Per range: past this, the oldest AI phrases make room for new ones. Manual phrases are never removed.
MAXIMO_POR_RANGO = 40


def cargar():
    data = json.loads(ARCHIVO.read_text(encoding="utf-8"))
    for r in RANGOS:
        data["rangos"].setdefault(r, [])
    return data


def guardar(data):
    ordenado = {"version": data.get("version", 1), "rangos": {r: data["rangos"].get(r, []) for r in RANGOS}}
    ARCHIVO.write_text(json.dumps(ordenado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalizar(texto):
    """For spotting repeats: no accents, no punctuation, lower case, single spaces."""
    t = unicodedata.normalize("NFKD", texto)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = "".join(c if c.isalnum() else " " for c in t.lower())
    return " ".join(t.split())


def existentes(data):
    return {normalizar(f["texto"]) for lista in data["rangos"].values() for f in lista}


def limpiar(texto):
    return " ".join(str(texto).split()).strip().strip('"').strip()


def agregar(data, rango, texto, origen):
    """Adds one phrase. Returns None when added, or why it was not."""
    texto = limpiar(texto)
    if rango not in RANGOS:
        return f"el rango «{rango}» no existe"
    if not texto:
        return "la frase está vacía"
    if len(texto) > LARGO_MAXIMO:
        return f"la frase tiene {len(texto)} caracteres y el máximo es {LARGO_MAXIMO}"
    if normalizar(texto) in existentes(data):
        return "esa frase ya está"
    lista = data["rangos"][rango]
    lista.append({"texto": texto, "origen": origen})
    while len(lista) > MAXIMO_POR_RANGO:
        viejas_ia = [i for i, f in enumerate(lista) if f.get("origen") == "ia"]
        if not viejas_ia:
            break
        del lista[viejas_ia[0]]
    return None
