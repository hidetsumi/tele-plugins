# tele-plugins

Plugins and settings for an Android TV / Google TV set (TCL G08) running the DreamOS home screen from
[cleanyourtv](https://github.com/Gathin23/cleanyourtv).

| Folder | Contents |
|---|---|
| [`phrases/`](phrases/) | Weather widget phrases ("30° Hace un re lorca") and the AI style guide. The TV downloads them from here. |
| [`launcher/`](launcher/) | DreamOS with home screen widgets: weather, headphones, HDMI devices, a headphones button and phrases. |
| [`addons/`](addons/) | Small apps that extend DreamOS. Currently [`weather`](addons/weather/). |
| [`docs/`](docs/) | Notes on this TV and how to undo every change. |
| [`scripts/`](scripts/) | Code used by the GitHub Actions. |

## Adding a phrase

1. Open **Issues → New issue → New phrase**.
2. Pick a category, write the phrase (up to 40 characters) and submit.
3. The **Add phrase** action adds it to `phrases/phrases.json` and closes the issue. The TV shows it within 30 minutes.

Only issues opened by the repository owner are applied. `phrases/phrases.json` can also be edited by hand.

## AI-generated phrases

Every Monday the **AI phrases** action asks Google Gemini (free tier) for new phrases and adds them with
`"source": "ai"`. The instructions it follows are in [`phrases/style-guide.md`](phrases/style-guide.md), and the reply
must match a fixed JSON schema. The action needs a free key from [Google AI Studio](https://aistudio.google.com/apikey)
stored as the `GEMINI_API_KEY` repository secret (Settings → Secrets and variables → Actions); without it the action
does nothing. It can also be run by hand from **Actions → AI phrases → Run workflow**.

## Cost

Everything here is free: GitHub Actions and Issues on a public repository, `raw.githubusercontent.com` for the
download, and Gemini's free tier for the AI step.

## License

MIT. The launcher and add-on code derives from [cleanyourtv](https://github.com/Gathin23/cleanyourtv)
(MIT, © 2026 Gathin) and its add-ons (each with its own author; see their READMEs).
