# Frases del clima

`frases.json` tiene las frases que la tele muestra después de la sensación térmica, agrupadas por rango:

| Rango | Cuándo |
|---|---|
| 35° o más · 30° a 34° · 25° a 29° · 19° a 24° · 13° a 18° · 7° a 12° · 6° o menos | Según la sensación térmica |
| Lluvia · Tormenta · Nieve | Cuando llueve, hay tormenta o nieva (tienen prioridad sobre la temperatura) |

Cada frase es `{"texto": "...", "origen": "manual" | "ia"}`. La tele elige una del rango que corresponde y la
cambia cada hora. Si no puede descargar este archivo, usa la última copia que bajó, y si nunca bajó ninguna,
las frases que trae incorporadas.

Reglas: hasta 40 caracteres, sin comillas ni emojis, sin repetir. Los nombres de los rangos tienen que ser
exactamente los de la tabla.

La tele lo lee de `https://raw.githubusercontent.com/hidetsumi/tele-plugins/main/frases/frases.json`.
