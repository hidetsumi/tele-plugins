# Volver todo atrás

Todo se hizo con `pm disable-user`, así que se puede deshacer. La lista aplicada está en [`debloat.txt`](debloat.txt). Con la depuración USB activada, desde un clon de
[cleanyourtv](https://github.com/Gathin23/cleanyourtv):

```bash
TV_HOST=<ip de la tele> tools/restore.sh ../tele-plugins/docs/debloat.txt com.google.android.apps.tv.launcherx
```

Eso reactiva todo lo desactivado y vuelve a poner el inicio de Google. Después se pueden desinstalar las apps
agregadas (DreamOS `com.gathin.tvhome`, los complementos `io.github.*` y CAPod `eu.darken.capod`) desde Ajustes >
Apps, o con `pm uninstall <paquete>`.

Si el asistente de configuración (`setupwraith`) se reactiva con el inicio de Google desactivado, la tele puede
quedar en pantalla negra: siempre reactivar `launcherx` primero.
