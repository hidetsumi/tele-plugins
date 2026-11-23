# TCL Smart TV Pro (G08, Google TV 14, MediaTek MT5896)

Firmware `UTT2.250416.001 AU02`, about 2.4 GB of RAM. The disable list ([`debloat.txt`](debloat.txt)) is based on
the `tcl-85rm7l-google-tv` and `tcl-c755-google-tv` profiles from cleanyourtv.

## What was disabled (pm disable-user; nothing uninstalled)

- TCL tracking: `com.tcl.ttvs` (Samba TV, analytics, T-Cast), `com.tcl.logkit`, `com.tcl.usercenter`.
- TCL ads and content: `channelplus`, `tclhome_passive`, `partnercustomizer`, `interactive`, `messagebox`,
  `waterfall.overseas`, retail and hotel modes, the silent partner-app installer (`gtvpai`, `partnersetup`).
- Unused extras: e-manual, repair guide, Alexa, feedback, Play Games, YouTube Music, TCL browser, Miracast, T-Cast,
  USB media player, gallery, soundbar updater, TCL Guard.
- The voice assistant (`com.google.android.katniss`): it used about 25% of a core at idle.
- The Google TV home screen (`launcherx`) and the setup wizard (`setupwraith`), only after DreamOS was in place.

Kept: Chromecast, AirPlay, the game bar, Ambient mode with Google Photos, and everything for inputs and live TV.

## Measured result (idle, after a reboot)

| | Before | After |
|---|---|---|
| CPU in use | ~11% | ~4% |
| Swap used | 389 MB | 109 MB |
| Available RAM | 1050 MB | ~960–973 MB |

## Quirks of this model

- **setupwraith owns the Wi-Fi network** saved during first-time setup: disabling it drops the TV off Wi-Fi. Forget
  the network and join it again in Settings first, so it belongs to `com.android.tv.settings`.
- **TCL auto-start blocking** stops providers and services of sideloaded apps
  (`[TclAppBoot] ... callee_does't_have_OP_AUTO_START_permission`). Allow it with
  `appops set <package> AUTO_START allow; appops set <package> ASSOC_START allow; appops write-settings`.
- **Choosing the Google Photos album** for Ambient mode needs the Google TV home screen: re-enable `launcherx` and
  `setupwraith`, pick the album, then disable them again (re-enable `launcherx` first).
- **Bluetooth** was off out of the box; the remote is infrared.
- **AirPods** pair and connect, but do not report their battery to Android, and Apple's proximity broadcasts do not
  reach apps on this set (CAPod never detected them, even with all its compatibility options on).
