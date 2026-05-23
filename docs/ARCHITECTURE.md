# Architecture

## Overview

The system is a multi-agent research pipeline that runs inside OpenCode. It uses a central behavioral specification (`AGENTS.md`) that OpenCode reads on every session start. Everything else — agents, memory, vault — is referenced from there.

```
User types topic
      ↓
Phase 1: Orchestrator builds source map (which agent covers what)
      ↓
Phase 2: 5 domain agents run in parallel → 5 research files
      ↓
Phase 3: Orchestrator synthesizes → auto-eval → auto-improve
      ↓
Phase 4: Optional sync to second Obsidian vault
      ↓
User types "ingest" → atomic notes extracted → vault updated
```

---

## Phase 1 — Pre-Dispatch Planning

The orchestrator reads `config.yaml` and the topic, then produces a JSON source map:

```json
{
  "slug": "consciousness-and-hard-problem",
  "research_question": "...",
  "agent_assignments": {
    "indic_traditions": { "scope": "...", "known_sources": [...] },
    "western_philosophy": { "scope": "...", "known_sources": [...] }
  },
  "boundary_cases": [...]
}
```

The source map is saved to `vault/research/{slug}/_source_map.json` before any agent runs.

**Why this matters:** Without explicit pre-dispatch assignment, agents overlap, duplicate work, and produce inconsistent coverage of boundary topics. The source map resolves ambiguity before it becomes bad output.

---

## Phase 2 — Parallel Agent Dispatch

All domain agents run simultaneously. Each receives a dispatch message specifying:
- The research topic and question
- Their scope (from the source map)
- Known sources to consult
- Languages to search in
- Special routing instructions for boundary cases

Each agent writes its output to a separate file: `vault/research/{slug}/{agent_name}.md`

Agent settings: temperature 0.3, max_tokens 12000.

The agents never see each other's output — cross-tradition synthesis is intentionally reserved for the orchestrator.

---

## Phase 3 — Review, Evaluation, and Improvement

### Orchestrator Review

After all agents complete, the orchestrator reads all 5 output files and produces:
- A synthesis of convergences across traditions
- Identified contradictions with their significance
- A gap analysis (what was missed and why)
- A cross-reference map for atomic note linking

### Auto-Evaluation (Step A)

Every run is scored on 7 metrics:

| Metric | What it measures |
|---|---|
| Source Density | Quality and specificity of citations |
| Language Coverage | Multilingual source diversity |
| Gap Rate | Missing obvious sources or traditions |
| Cross-Tradition Richness | Quality of connections found across domains |
| Boundary Accuracy | Correct routing of ambiguous topics |
| Temporal Depth | Historical span covered |
| Contradiction Quality | Depth of engagement with conflicting views |

The orchestrator is scored separately on: Source Map Quality, Synthesis Quality, Gap Identification.

Results are appended to `.memory/eval_history.json`.

### Gap Logging (Step B)

Any metric below 6/10 triggers a specific gap entry in `.memory/gap_log.json`:
```json
{
  "slug": "topic-slug",
  "agent": "western_philosophy",
  "gap": "Heidegger interpretation needs Gesamtausgabe edition, not Macquarrie & Robinson",
  "timestamp": "..."
}
```

### Auto-Improvement (Step C)

If any agent scores below 60% of its maximum across 2+ consecutive runs, or if a single metric is below 6/10 repeatedly:

1. The `improvement_agent.md` reads the current prompt and the gap log
2. Generates a targeted improvement — not a generic rewrite, but a specific fix for the identified gap
3. Snapshots the old prompt to `.memory/prompt_versions/{timestamp}_{agent}.md`
4. Writes the new prompt to `.agents/prompts/{agent}.md`
5. Opens a GitHub PR for human review

**You always review and merge the PR — the system never auto-merges.**

This is the system's learning loop. Every research run produces evidence. Evidence accumulates in the gap log. The gap log drives targeted fixes. Fixes get verified in subsequent runs. Over time, agents become demonstrably better at their domain — not through fine-tuning, but through prompt engineering guided by empirical evaluation.

### Verification (Step D)

On each subsequent run, the system checks whether previous improvements worked:
- Score on the targeted metric improved → `confirmed`
- Score regressed → `regression` (needs review)
- Unchanged → stays `pending`

---

## Ingest Pipeline — Atomic Notes

Triggered by typing `ingest` after a research run.

The system extracts structured atomic notes into `vault/atomic-notes/{type}/`:

### The Luhmann Linkage Model

The atomic note system is modelled on Niklas Luhmann's Zettelkasten — the slip-box method he used to produce over 70 books and 400 articles. Luhmann's key insight: knowledge does not grow by accumulation but by *connection*. Each slip in his box linked to other slips, creating emergent structure that no individual note contained.

This system implements that principle digitally, extended across traditions:

| Link type | Notation | Meaning |
|---|---|---|
| Causal | `[[A]] → [[B]]` | A causes, produces, or leads to B |
| Effect | `[[A]] ← [[B]]` | A is produced by or results from B |
| Convergence | `[[A]] ↔ [[B]]` | A and B are parallel concepts from different traditions |

The convergence links (`↔`) are the most important. They are not manual — they are derived from the orchestrator's Phase 3 cross-reference map. If the orchestrator identifies that *saṃskāra* (Indic habit-formation) converges with *automaticity* (cognitive science) and *Verdrängung* (Freudian repression), the ingest pipeline adds `↔` links between all three notes automatically.

**Merge rule:** If a note already exists, only a new cross-reference link is appended. The note is never overwritten. This means the vault grows richer with each research run without losing prior structure.

| Type | What it captures |
|---|---|
| `concepts` | Core ideas with causal/effect/symmetric links |
| `people` | Thinkers, scholars, teachers |
| `texts` | Foundational works |
| `patterns` | Structural patterns that recur across traditions |
| `traditions` | Named intellectual or spiritual lineages |
| `questions` | Research questions surfaced by this topic |

Each note uses Obsidian wikilinks to connect to related notes, including cross-tradition links found in the orchestrator's convergences section.

**Merge rule:** If a note file already exists, only a cross-reference link is appended — the note is never overwritten.

After extraction, the Atomic Notes Agent evaluates each note on 5 quality metrics and amends any scoring below 8/10.

---

## Memory System

Five files in `.memory/` track system state across runs:

| File | What it stores |
|---|---|
| `domain_memory.json` | Last run slug, total note counts, research history |
| `eval_history.json` | Full scoring history for every run |
| `gap_log.json` | Specific gaps identified per agent per topic |
| `amendments_pending.json` | Improvement PRs awaiting verification |
| `atomic_notes_tracker.json` | Note quality history and amendment log |
| `prompt_versions/` | Snapshots of agent prompts before each improvement |

---

## Script Triad System

For multilingual research, agents use a hybrid format balancing readability with scholarly precision. See `AGENTS_REFERENCE.md` for the full specification.

**Summary:**
- First use of a key term: blockquote with original script + transliteration + English
- Subsequent mentions: inline within prose
- Verse citations: 3-line blockquote (original / transliteration / translation)
- Maximum 8-10 blockquotes per section

---

## File Layout

```
vault/research/{slug}/
  _source_map.json          Phase 1 output
  {agent_name}.md           Phase 2 output (one per agent)
  orchestrator_review.md    Phase 3 synthesis

vault/atomic-notes/{type}/
  {concept-name}.md         Obsidian atomic notes

.memory/
  eval_history.json         Evaluation scores
  gap_log.json              Gap tracking
  amendments_pending.json   Improvement verification
  domain_memory.json        Run history
  atomic_notes_tracker.json Note quality tracking
  prompt_versions/          Agent prompt snapshots
```
