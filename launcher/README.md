# Launcher: DreamOS with widgets

`widgets.patch` applies to [cleanyourtv](https://github.com/Gathin23/cleanyourtv) at commit `687b5ee`. It contains the
DreamOS template (photo wallpaper, glass dock, sounds) plus the additions made here:

| Option (`launcher/app/src/main/res/values/config.xml`) | What it does |
|---|---|
| `home_widgets` | A row of widgets under the clock: weather, connected headphones (with battery when reported) and devices on the HDMI ports. Each one hides itself when it has nothing to show. |
| `headphones_button` | A fixed headphones button next to Settings. It opens the TV's Bluetooth accessories, where Connect is one press away; Android does not let apps connect headphones themselves. |
| `weather_phrases` | Shows the weather as feels-like temperature plus a phrase ("30° Hace un re lorca"). Phrases come from the weather add-on, which downloads [`phrases/`](../phrases/); offline, the launcher uses its built-in phrases. |

The launcher still has no internet permission. The only new permission is `BLUETOOTH_CONNECT`, granted over ADB.

## Build and install

Requires JDK 17 and Android SDK platform 34. With the TV on the same network and USB debugging on:

```bash
git clone https://github.com/Gathin23/cleanyourtv && cd cleanyourtv
git checkout 687b5ee
git apply ../tele-plugins/launcher/widgets.patch
# DreamOS font, wallpaper and sounds are binary and not in the patch (see the dreamos template of the tv-makeover plugin)
cd launcher && TV_HOST=<tv ip> ./build-and-install.sh
TV_HOST=<tv ip> ../tools/venv/bin/python -I ../tools/tv.py 'pm grant com.gathin.tvhome android.permission.BLUETOOTH_CONNECT'
```

Updating an installed DreamOS needs an APK signed with the same key as before (`~/.android/debug.keystore`). If that
key is lost, the launcher has to be uninstalled and installed again.
