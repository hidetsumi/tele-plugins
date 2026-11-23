# TCL Smart TV Pro (G08, Google TV 14, MediaTek MT5896)

Firmware `UTT2.250416.001 AU02`, unos 2,4 GB de RAM. Lista de desactivados basada en los perfiles
`tcl-85rm7l-google-tv` y `tcl-c755-google-tv` de cleanyourtv.

## Qué se desactivó (pm disable-user, nada desinstalado)

- Rastreo de TCL: `com.tcl.ttvs` (Samba TV, analíticas, T-Cast), `com.tcl.logkit`, `com.tcl.usercenter`.
- Anuncios y contenido de TCL: `channelplus`, `tclhome_passive`, `partnercustomizer`, `interactive`, `messagebox`,
  `waterfall.overseas`, modo demo y hotel, instalador silencioso de partners (`gtvpai`, `partnersetup`).
- Extras sin uso: manual, guía de reparación, Alexa, feedback, Play Juegos, YouTube Music, navegador TCL, Miracast,
  T-Cast, reproductor USB, galería, actualizador de barras de sonido, TCL Guard.
- Asistente de voz (`com.google.android.katniss`): usaba ~25 % de un núcleo en reposo.
- Inicio de Google (`launcherx`) y el asistente de configuración (`setupwraith`), recién después de tener DreamOS.

Se dejaron: Chromecast, AirPlay, el modo juego, el modo ambiente con Google Photos y todo lo de entradas/TV.

## Resultado medido (en reposo, después de reiniciar)

| | Antes | Después |
|---|---|---|
| CPU ocupada | ~11 % | ~4 % |
| Swap usada | 389 MB | 109 MB |
| RAM disponible | 1050 MB | ~960-973 MB |

## Trucos de este modelo

- **setupwraith es dueño del Wi-Fi** guardado en la configuración inicial: desactivarlo desconecta la tele. Antes hay
  que olvidar la red y volver a conectarse desde Ajustes (pasa a ser de `com.android.tv.settings`).
- **Arranque automático de TCL**: bloquea providers y servicios de apps instaladas a mano
  (`[TclAppBoot] ... callee_does't_have_OP_AUTO_START_permission`). Se permite con
  `appops set <paquete> AUTO_START allow; appops set <paquete> ASSOC_START allow; appops write-settings`.
- **Elegir el álbum de Google Photos** del modo ambiente necesita el inicio de Google activo: reactivar `launcherx` y
  `setupwraith` un rato, elegir el álbum y volver a desactivarlos.
- **Bluetooth**: el control es infrarrojo y el Bluetooth venía apagado.
- **AirPods**: se vinculan y conectan bien, pero no informan la batería a Android, y las señales de proximidad de
  Apple no le llegan a las apps (CAPod no los detecta, ni con todas sus opciones de compatibilidad).
