# Agent Manifest

Central registry of available specialists and subagents for LLM Wiki operations.

---

## Available Specialists

| Agent | Role | Capabilities | Trigger |
|-------|------|--------------|---------|
| `researcher` | Cross-traditional research | Sanskrit, German, Bengali, Civilizations, English-Language | `Research topic:` |
| `book_fetcher` | Book summarization | Chapter-by-chapter summaries, author voice | `Fetch book:` |
| `ocr_processor` | Image-to-text | Photo scanning, book page extraction | Manual trigger |
| `coder` | Code tasks | Python, scripts, automation | Task-specific |
| `editor` | Content polishing | Grammar, flow, formatting | Task-specific |
| `analyst` | Data analysis | Numbers, spreadsheets, insights | Task-specific |
| `writer` | Content creation | First drafts, content generation | Task-specific |
| `summarizer` | Condensation | Long content → key points | Task-specific |

---

## Agent Invocation Protocol

### Before calling an agent (PRE-FLIGHT CHECK):

1. **Verify template path exists** — use absolute path
2. **Verify output directory exists** — use absolute path
3. **Confirm save path in task prompt** — include full absolute path explicitly

```
### [AGENT_NAME]
- [HH:MM] [task description] | PENDING | [expected output path]
- Template: [absolute path to template]
- Output: [absolute path to output file]
```

### After completion (VERIFICATION):
- Confirm file exists at specified path
- If missing, retry with explicit absolute path
- Update status:

```
### [AGENT_NAME]
- [HH:MM] [task description] | COMPLETED | [actual output path]
- Verified: YES/NO
- Lines: [count]
```

---

## Session Log: 2026-05-17

### researcher (10 calls total)

| Time | Task | Status | Output |
|------|------|--------|--------|
| 14:30 | consciousness | COMPLETED | raw/sources/2026-05-17-consciousness.md |
| 14:35 | predictive processing | COMPLETED | raw/sources/2026-05-17-predictive-processing.md |
| 14:35 | advaita vedanta | COMPLETED | raw/sources/2026-05-17-advaita-vedanta.md |
| 14:35 | tagore education | COMPLETED | raw/sources/2026-05-17-tagore-education.md |
| 14:35 | kant ethics | COMPLETED | raw/sources/2026-05-17-kant-ethics.md |
| 14:47 | consciousness (retry) | COMPLETED | raw/sources/2026-05-17-consciousness.md |
| 14:49 | predictive processing (retry) | COMPLETED | raw/sources/2026-05-17-predictive-processing.md |
| 14:47 | kant ethics | COMPLETED | raw/sources/2026-05-17-kant-ethics.md |

### book_fetcher
- None invoked

### ocr_processor
- None invoked

---

## Efficiency Notes

- **Max parallel agents:** 4-5 (used 4 parallel for tests 2-5)
- **Retry rate:** 2/5 tasks needed retry due to save path issues
- **Total output:** 5 research documents, ~1,500 lines

---

## Files Generated

```
raw/sources/
├── 2026-05-17-advaita-vedanta.md     (270 lines, ~4,500 words)
├── 2026-05-17-consciousness.md       (312 lines, ~8,000 words)
├── 2026-05-17-kant-ethics.md         (252 lines, ~4,000 words)
├── 2026-05-17-predictive-processing.md  (180 lines, ~2,500 words)
└── 2026-05-17-tagore-education.md    (458 lines, ~4,200 words)
```