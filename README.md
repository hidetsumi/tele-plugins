# tele-plugins

Plugins y ajustes para una tele Android TV / Google TV (TCL G08) con el launcher DreamOS de
[cleanyourtv](https://github.com/Gathin23/cleanyourtv).

| Sección | Qué hay |
|---|---|
| [`frases/`](frases/) | Las frases del widget del clima ("30° Hace un re lorca"). La tele las descarga de acá. |
| [`launcher/`](launcher/) | DreamOS con widgets: clima, auriculares, fuentes HDMI, botón fijo de auriculares y frases. |
| [`complementos/`](complementos/) | Apps chicas que se suman a DreamOS. Hoy: [`clima`](complementos/clima/). |
| [`docs/`](docs/) | Notas de la tele y cómo volver todo atrás. |
| [`scripts/`](scripts/) | Lo que usan las automatizaciones de GitHub. |

## Agregar una frase

1. **Issues → New issue → Nueva frase**.
2. Elegí el rango, escribí la frase (hasta 40 caracteres) y mandala.
3. Una GitHub Action la suma a `frases/frases.json` y cierra el issue. La tele la muestra en menos de 30 minutos.

Solo se aplican las frases que manda el dueño del repo. También se puede editar `frases/frases.json` a mano.

## Frases con IA

Todos los lunes, la Action **Frases nuevas con IA** le pide frases nuevas a Google Gemini (nivel gratuito) y
las agrega solas, marcadas `"origen": "ia"`. Necesita una clave gratis de [Google AI Studio](https://aistudio.google.com/apikey)
guardada como secreto `GEMINI_API_KEY` (Settings → Secrets and variables → Actions); sin ella, la Action no hace nada. Cuando un rango pasa las 40 frases, se borran las de IA más viejas; las
escritas a mano nunca se borran. Se puede correr a mano desde **Actions → Frases nuevas con IA → Run workflow**.

## Licencia

MIT. El código del launcher y de los complementos deriva de [cleanyourtv](https://github.com/Gathin23/cleanyourtv)
(MIT, © 2026 Gathin) y de sus complementos (cada uno con su autor, ver los README).
