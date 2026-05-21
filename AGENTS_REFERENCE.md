# RESEARCH SYSTEM — REFERENCE MANUAL

Reference documentation for the multi-agent scholarly research system.
Not read on every run — consult when designing prompts or debugging routing.

---

## SCRIPT TRIAD SYSTEM — HYBRID FORMAT

The triad system balances scholarly rigor (original scripts + transliteration) with readability.

### Core Rule: Major → Blockquote, Secondary → Inline

| Tier | Format | Where | Example |
|---|---|---|---|
| **MAJOR** (central concept, first use of key term, verse citation) | Blockquote `>` | Standalone paragraph | `> **चित (citta)** — mind-stuff` |
| **SECONDARY** (adjacent terms, later mentions) | Inline in prose | Within paragraph text | `The term कर्म (karma) connects to धर्म (dharma)` |
| **Proper names** (teachers, texts) | Inline with full triad on first occurrence | Within paragraph | `शङ्कर (Śaṅkara) — Shankaracharya` |

### Blockquote Density Limit
- Maximum 8–10 blockquotes per section
- Most terms inline for content depth
- First occurrence of major term: blockquote. Subsequent: transliteration only

### Verse Citation Format
```
> {original_script}
> ({transliteration})
> — {english_translation}
```

### Per-Language Script Rules

| Language Family | Script | Transliteration Standard |
|---|---|---|
| **Sanskrit / Pali** | Devanagari (देवनागरी) | IAST (ISO 15919) |
| **Tibetan** | Tibetan script (བོད་སྐད) | Wylie transliteration |
| **Prakrit** | Devanagari | IAST |
| **Bengali / Assamese** | Bengali script | IAST with Bengali diacritics |
| **Tamil** | Tamil script (தமிழ்) | ISO 15919 |
| **Telugu / Kannada / Malayalam** | Respective Brahmic scripts | ISO 15919 |
| **Hindi / Marathi / Gujarati** | Devanagari / Gujarati script | IAST / ISO 15919 |
| **Ancient Greek** | Greek alphabet (Ἑλληνική) | IAST for Greek |
| **Latin** | Roman script | Classical Latin |
| **German** | Fraktur where original, otherwise Roman | Standard German orthography |
| **Hebrew** | Hebrew script (עִבְרִית) | ISO 259 / SBL |
| **Aramaic / Syriac** | Syriac script (ܐܪܡܝܐ) | SBL / ALA-LC |
| **Arabic** | Arabic script (العربية) | IQTIDAL / ALA-LC |
| **Persian** | Persian script (فارسی) | ALA-LC |
| **Avestan** | Avestan script where available, otherwise transliteration | Geldner / Hoffmann |
| **Egyptian** | Hieroglyphic transliteration | Gardiner sign list |
| **Old Norse** | Latin (transliterated runes) | Standard scholarly transliteration |
| **Old Irish** | Latin (transliterated ogham) | Standard scholarly transliteration |
| **Japanese** | Kanji + Kana (日本語) | Hepburn (rōmaji) |
| **French** | Standard French | N/A (use original orthography) |
| **English technical terms** | Standard English | N/A |

### Per-Agent Triad Guidance

| Agent | Triad Usage | Notes |
|---|---|---|
| **Indic (A)** | Full triad — Devanagari + IAST + English | Always include original script. Tibetan for Buddhist terms. |
| **Western (B)** | Greek/Latin/Hebrew with transliteration | German terms in Fraktur where original. German titles: "Sein und Zeit (Being and Time)". |
| **Civilizations (C)** | Heavy triad across 8+ language families | Hebrew, Arabic, Greek, Egyptian, Old Norse, Latin, Avestan, German. |
| **Contemporary (D)** | Optional triad — prioritise German, Japanese, French terms | Most contemporary terms are English. Use triad for nuance-bearing foreign terms. |
| **Science & Tech (E)** | Minimal triad — 5–8 blockquotes per section max | Most terms are English. Use blockquote for German philosophical terms in physics. |

### Examples

Major Concept (Indic):
```
> **चित (citta)** — mind-stuff — the total field of conscious and subconscious mental activity
```

Inline Secondary:
```
The term कर्म (karma) connects to धर्म (dharma) through action and law.
```

Verse Citation (Indic):
```
> ब्रह्म सत्यं जगन्मिथ्या (brahma satyaṃ jagan mithyā)
> — "Brahman is real, the world is false"
```

Greek Concept (Western):
```
> **ψυχή (psyche)** — soul/life principle — originally meant "breath"
```

Hebrew Concept (Civilizations):
```
> **נפש (nephesh)** — soul/animating principle — appears in Genesis 2:7
```

Proper Name:
```
शङ्कर (Śaṅkara) — Shankaracharya (8th century CE Advaita philosopher)
```

---

## BOUNDARY CASE ROUTING RULES

Apply in order when assigning ambiguous sources:

1. Tibetan Buddhist texts → indic_traditions (Indian Buddhist origin)
2. Sufi poetry (Rumi, Ibn Arabi, Hafez) → ancient_civilizations
3. Jung, Freud, Adler → western_philosophy
4. Ken Wilber, Stanislav Grof → contemporary_scholarship
5. NDE/consciousness science research → contemporary_scholarship
6. Living Indian teachers regardless of language → indic_traditions
7. Academic papers cross-citing 3+ traditions → contemporary_scholarship
8. Celtic/Norse/Mayan/Aztec traditions → ancient_civilizations
9. Christian mysticism (Eckhart, Böhme) → western_philosophy
10. Hermeticism, Alchemy, Western Demonology → ancient_civilizations
11. Tarot, Oracle, Astrology (academic) → contemporary_scholarship
12. Energy Healing, Reiki (academic research) → contemporary_scholarship
13. Quantum Physics, Astrophysics → science_technology
14. AI, Machine Consciousness, AGI → science_technology
15. When still ambiguous: assign to agent whose scope is BROADER for this topic

---

## TOKEN BUDGET REFERENCE

| Call | Temperature | Max Tokens |
|---|---|---|
| Phase 1 (source map) | 0.2 | 3000 |
| Each agent (×5) | 0.3 | 12000 |
| Phase 3 (review) | 0.4 | 4000 |
| Ingest extraction | 0.2 | 15000 |
| Evaluate | 0.1 | 6000 |
| Improve | 0.3 | 6000 |
| Amendment (notes) | 0.2 | 4000 |

---

## AMENDMENTS PENDING STRUCTURE

```json
{
  "research_amendments": [
    {
      "run_id": "{slug}",
      "agent": "{agent_name}",
      "metric": "{metric_name}",
      "score": {n},
      "gap_detail": "description of missing coverage",
      "amendment_action": "description of what needs to change",
      "created_at": "{timestamp}",
      "pr_url": null,
      "status": "pending",
      "verified_on": null
    }
  ],
  "atomic_amendments": [
    {
      "run_id": "{slug}",
      "note": "{note_title}",
      "score": {n},
      "issue": "description of issue",
      "amendment_applied": "what was fixed",
      "created_at": "{timestamp}",
      "status": "pending",
      "verified_on": null
    }
  ]
}
```

---

## FILE PATH REFERENCE

| What | Where |
|---|---|
| Agent prompts | .agents/prompts/{name}.md |
| Orchestrator prompt | .agents/prompts/orchestrator.md |
| Atomic Note Agent | .agents/prompts/agent_atomic_notes.md |
| Research output | vault/research/{slug}/*.md |
| Atomic notes | vault/atomic-notes/{type}/{name}.md |
| Source map | vault/research/{slug}/_source_map.json |
| Domain memory | .memory/domain_memory.json |
| Gap log | .memory/gap_log.json |
| Eval history | .memory/eval_history.json |
| Atomic notes tracker | .memory/atomic_notes_tracker.json |
| Amendments pending | .memory/amendments_pending.json |
| Prompt snapshots | .memory/prompt_versions/{ts}_{agent}.md |
| Config | config.yaml |
