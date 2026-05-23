# Example: Philosophy & Comparative Religion Research

This is a fully configured 5-agent setup for comparative philosophy and religious studies across world traditions.

## Why this domain?

Comparative philosophy and religious studies was chosen as the primary example because it stress-tests all three of the system's core innovations simultaneously:

- **Epistemic parallelism** — the traditions are genuinely distinct. An Indic agent and a Western agent will produce completely different source bases, languages, and conceptual frameworks for the same topic. There is no overlap to paper over.
- **Luhmann linkage** — the potential for cross-tradition convergence is exceptionally high. Concepts like *ātman*, *Seele*, and *soul* converge and diverge in ways that generate dense, meaningful wikilinks across the vault.
- **Agent improvement** — the domain is demanding enough (multilingual, multi-script, spanning 5000 years) that agents consistently find gaps, which drives the improvement loop with real evidence.

If the system works well for comparative philosophy, it works well for any domain.

## What it covers

| Agent | File | Domain |
|---|---|---|
| Agent A — Indic Traditions | `agent_a_indic.md` | Vedic corpus, Upanishads, Buddhist (Pali & Mahayana), Jain, Sikh, Tantric, modern teachers. Languages: Sanskrit, Pali, Tibetan, Bengali, Tamil. |
| Agent B — Western Philosophy | `agent_b_western.md` | German idealism (Kant, Hegel, Heidegger), existentialism, Greek classics, Christian mysticism, Jungian psychology. Languages: German, Greek, Latin, French. |
| Agent C — Ancient Civilizations | `agent_c_civilizations.md` | Egyptian, Mesopotamian, Hebrew, Norse, Celtic, Mayan, Persian, Zoroastrian. Languages: Egyptian hieroglyphic, Hebrew, Avestan, Old Norse, Latin. |
| Agent D — Contemporary Scholarship | `agent_d_contemporary.md` | Academic cross-tradition synthesis, consciousness studies, African philosophy, NDE research. |
| Agent E — Science & Technology | `agent_e_science.md` | Quantum physics, astrophysics, consciousness science, AI and machine cognition. |

## Using this example

Copy the agent prompts into `.agents/prompts/` before your first run:

```bash
cp examples/philosophy-research/.agents/prompts/*.md .agents/prompts/
```

The `AGENTS.md` Phase 2 mapping already references the philosophy agent filenames (`agent_a_indic.md` etc.), so no other changes are needed.

## Example topics this handles well

- "What is the self?" — spans Upanishadic ātman, Buddhist anatta, Kantian subject, Jungian ego
- "Consciousness and matter" — Samkhya dualism, Western physicalism, quantum theories
- "Death and rebirth" — reincarnation doctrines across every tradition
- "The nature of time" — cyclical vs. linear views across cultures
- "The hard problem of consciousness" — philosophy of mind across traditions

## Boundary case routing

The `config.yaml` `routing_defaults` section defines how ambiguous topics are assigned. For this example:
- Tibetan Buddhist texts → Indic Traditions (Buddhist origin, not Tibetan culture)
- Jung, Freud → Western Philosophy
- Tarot, astrology (academic) → Contemporary Scholarship
- Celtic, Norse, Mayan → Ancient Civilizations

See `AGENTS_REFERENCE.md` for the full 15-rule routing table.
