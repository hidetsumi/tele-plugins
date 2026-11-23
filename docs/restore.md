# Undoing everything

Every change was made with `pm disable-user`, so all of it can be undone. The applied list is
[`debloat.txt`](debloat.txt). With USB debugging on, from a clone of
[cleanyourtv](https://github.com/Gathin23/cleanyourtv):

```bash
TV_HOST=<tv ip> tools/restore.sh ../tele-plugins/docs/debloat.txt com.google.android.apps.tv.launcherx
```

That re-enables everything that was disabled and brings back the Google TV home screen. The added apps (DreamOS
`com.gathin.tvhome`, the `io.github.*` add-ons and CAPod `eu.darken.capod`) can then be removed in Settings > Apps, or
with `pm uninstall <package>`.

If the setup wizard (`setupwraith`) is re-enabled while the Google TV home screen is still disabled, the TV can end
up on a black screen: always re-enable `launcherx` first.
