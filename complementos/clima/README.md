# Complemento: clima

`clima-widget.patch` se aplica sobre `addons/weather` de [cleanyourtv](https://github.com/Gathin23/cleanyourtv)
(autor original: [@Sumyabazar1](https://github.com/Sumyabazar1), datos de [Open-Meteo](https://open-meteo.com/)).

Lo que agrega:

- **Dato para el widget**: guarda la última lectura (temperatura, sensación térmica, estado) y se la pasa al launcher
  con un ContentProvider de solo lectura (`io.github.sumyabazar1.weather.widget`). El launcher no tiene internet.
- **Actualización sola**: un JobScheduler la refresca cada 30 minutos con red, aunque no abras la app.
- **Frases**: en cada actualización baja [`frases/frases.json`](../../frases/) y elige la frase del rango que toca.

Permisos nuevos: `RECEIVE_BOOT_COMPLETED` (que la tarea sobreviva al reinicio) y `ACCESS_NETWORK_STATE` (esperar
a tener red). En las TCL hay que permitir además el arranque automático, o el launcher no puede leer el dato:

```bash
tools/tv.py 'appops set io.github.sumyabazar1.weather AUTO_START allow; appops set io.github.sumyabazar1.weather ASSOC_START allow; appops write-settings'
```
