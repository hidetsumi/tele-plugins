# Weather phrases

`phrases.json` holds the phrases the TV shows after the feels-like temperature. The TV downloads it from
`https://raw.githubusercontent.com/hidetsumi/tele-plugins/main/phrases/phrases.json` every 30 minutes.

## Format (schema version 2)

```json
{
  "schemaVersion": 2,
  "updatedAt": "2026-11-23T19:45:00Z",
  "categories": [
    {
      "id": "hot",
      "label": "Feels like 30–34 °C",
      "condition": { "feelsLikeMin": 30, "feelsLikeMax": 34 },
      "phrases": [
        { "text": "Hace un re lorca", "source": "manual", "addedAt": "2026-11-23" }
      ]
    },
    {
      "id": "rain",
      "label": "Rain or drizzle",
      "condition": { "weather": "rain" },
      "priority": 1,
      "phrases": []
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `id` | Stable identifier. The AI and the scripts refer to categories by it. |
| `label` | Human-readable name, shown in the issue form. |
| `condition.feelsLikeMin` / `feelsLikeMax` | Feels-like range in °C, both ends included. Either end may be left out. |
| `condition.weather` | `rain`, `thunderstorm` or `snow`. These categories win over temperature ranges. |
| `priority` | When several weather categories match, the highest wins. |
| `phrases[].source` | `manual` (written by a person) or `ai`. |
| `phrases[].addedAt` | Date added. When a category passes 40 phrases, the oldest AI phrases are removed; manual ones never are. |

## How the TV picks a phrase

1. If it is raining, storming or snowing, the matching weather category with the highest priority.
2. Otherwise, the first category whose feels-like range contains the current feels-like temperature.
3. Within the category, one phrase per hour, rotating through the list.

Ranges and categories can be changed here without updating the TV. If the TV cannot download the file it keeps the
last copy, and if it never had one it uses the phrases built into the launcher.

## Rules for phrases

Up to 40 characters, no quotes or emoji, no duplicates. The tone is described in [`style-guide.md`](style-guide.md),
which is also the AI's instruction.
