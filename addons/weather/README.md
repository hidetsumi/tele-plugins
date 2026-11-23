# Add-on: weather

`weather-widget.patch` applies to `addons/weather` in [cleanyourtv](https://github.com/Gathin23/cleanyourtv)
(original author: [@Sumyabazar1](https://github.com/Sumyabazar1); data from [Open-Meteo](https://open-meteo.com/)).

What it adds:

- **Data for the widget**: keeps the last reading (temperature, feels-like, conditions) and shares it with the
  launcher through a read-only ContentProvider (`io.github.sumyabazar1.weather.widget`). The launcher has no internet.
- **Background refresh**: a JobScheduler job refreshes it every 30 minutes while there is a network, without opening
  the app.
- **Hourly forecast**: each refresh also keeps 7 days of hourly forecast from Open-Meteo. The provider's
  `forecast` column summarizes it for the launcher's day card: the next hours, today's low and high, and the next
  rain (the first hour with rain or drizzle, or at least 0.2 mm).
- **Phrases**: each refresh also downloads [`phrases/phrases.json`](../../phrases/) and picks the phrase for the
  current conditions.

New permissions: `RECEIVE_BOOT_COMPLETED` (the job survives a reboot) and `ACCESS_NETWORK_STATE` (wait for a network).
On TCL sets auto-start must also be allowed, or the launcher cannot read the data:

```bash
tools/tv.py 'appops set io.github.sumyabazar1.weather AUTO_START allow; appops set io.github.sumyabazar1.weather ASSOC_START allow; appops write-settings'
```
