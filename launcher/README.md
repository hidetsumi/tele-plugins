# Launcher: DreamOS con widgets

`widgets.patch` se aplica sobre [cleanyourtv](https://github.com/Gathin23/cleanyourtv) en el commit `687b5ee`. Lleva
la plantilla DreamOS (foto de fondo, dock de vidrio, sonidos) más lo que se agregó acá:

| Opción (`launcher/app/src/main/res/values/config.xml`) | Qué hace |
|---|---|
| `home_widgets` | Fila de widgets debajo de la hora: clima, auriculares conectados (y batería si la informan) y aparatos en los HDMI. Cada uno se oculta si no tiene nada que mostrar. |
| `headphones_button` | Botón fijo de auriculares junto a Ajustes: abre los accesorios Bluetooth de la tele, donde Conectar queda a un toque. Android no deja que una app conecte auriculares por su cuenta. |
| `weather_phrases` | El clima como sensación térmica + frase ("30° Hace un re lorca"). Las frases vienen del complemento de clima, que las baja de [`frases/`](../frases/); sin conexión usa las que trae incorporadas. |

El launcher sigue sin permiso de internet. Lo nuevo que pide es `BLUETOOTH_CONNECT`, que se da por ADB.

## Compilar e instalar

Hace falta JDK 17 y el Android SDK 34. Con la tele en la misma red y la depuración USB activada:

```bash
git clone https://github.com/Gathin23/cleanyourtv && cd cleanyourtv
git checkout 687b5ee
git apply ../tele-plugins/launcher/widgets.patch
# fuente, fondo y sonidos de DreamOS: los binarios no están en el parche (ver la plantilla dreamos del plugin tv-makeover)
cd launcher && TV_HOST=<ip de la tele> ./build-and-install.sh
TV_HOST=<ip de la tele> ../tools/venv/bin/python -I ../tools/tv.py 'pm grant com.gathin.tvhome android.permission.BLUETOOTH_CONNECT'
```

Para actualizar un DreamOS ya instalado, el APK tiene que estar firmado con la misma clave que la vez anterior
(`~/.android/debug.keystore`). Si se pierde, hay que desinstalar el launcher e instalarlo de nuevo.
