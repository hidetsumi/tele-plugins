"""Adds the phrase from a "Nueva frase" issue (its body comes in the ISSUE_BODY environment variable).

Prints the result for the issue comment and exits 0 when the phrase was added, 1 when it was refused.
"""
import os
import sys

import frases


def campos(cuerpo):
    """An issue form's body is '### Label' followed by the answer, one block per field."""
    resultado, actual, lineas = {}, None, []
    for linea in cuerpo.splitlines():
        if linea.startswith("### "):
            if actual:
                resultado[actual] = "\n".join(lineas).strip()
            actual, lineas = linea[4:].strip(), []
        else:
            lineas.append(linea)
    if actual:
        resultado[actual] = "\n".join(lineas).strip()
    return resultado


def main():
    f = campos(os.environ.get("ISSUE_BODY", ""))
    rango, texto = f.get("Rango", ""), f.get("Frase", "")
    data = frases.cargar()
    error = frases.agregar(data, rango, texto, "manual")
    if error:
        print(f"No la agregué: {error}.")
        return 1
    frases.guardar(data)
    print(f"Listo, agregué «{frases.limpiar(texto)}» en {rango}. La tele la va a mostrar en menos de 30 minutos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
