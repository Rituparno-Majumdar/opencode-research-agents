# MASTER RESEARCH SYSTEM BLUEPRINT v2.0
## Opencode Zen (Minimax M1/2.5) — Native Terminal Orchestration
## Obsidian Vault + Karpathy Autoresearch Loop + GitHub Actions

---

> **HOW TO USE THIS DOCUMENT**
> Drop this entire repo on your machine. Open Opencode Zen in the repo root.
> Type a research topic. Everything else is automatic.
> Read once top to bottom. Then follow Section 3 (Setup) to go live.

---

# TABLE OF CONTENTS

1. [System Philosophy & Design Rules](#1-system-philosophy--design-rules)
2. [Folder & Repo Structure](#2-folder--repo-structure)
3. [Setup — Run This Once](#3-setup--run-this-once)
4. [AGENTS.md — The Opencode Rules File](#4-agentsmd--the-opencode-rules-file)
5. [All Agent System Prompts](#5-all-agent-system-prompts)
6. [Python Utility Library](#6-python-utility-library)
7. [GitHub Actions Workflows](#7-github-actions-workflows)
8. [config.yaml](#8-configyaml)
9. [Complete Flow Walkthrough](#9-complete-flow-walkthrough)
10. [Obsidian Vault Setup](#10-obsidian-vault-setup)
11. [Maintenance & Scaling Rules](#11-maintenance--scaling-rules)

---

# 1. SYSTEM PHILOSOPHY & DESIGN RULES

## What This System Does

You open Opencode Zen in your repo. You type a research topic in plain language.
Opencode reads AGENTS.md, understands what to do, orchestrates 4 parallel scholarly
agents, saves findings to your Obsidian vault, and optionally converts them to
atomic notes — all without leaving the terminal.

Every night, GitHub Actions evaluates recent runs, proposes prompt improvements
as a PR. You review, merge, agents get smarter.

## How Opencode Zen Fits In

Opencode Zen is not just a coding assistant. It is a **reasoning + tool-use agent**
running in your terminal. When you type a research topic, Opencode:

1. Reads AGENTS.md at session start (your permanent instruction set)
2. Interprets your natural language input against those rules
3. Uses its built-in file tools to read/write vault files
4. Calls Minimax M1 API for each agent (via utils/minimax_ops.py)
5. Manages the full orchestration flow without any CLI wrapper

You never type `python research.py`. You just type the topic.

## Core Design Rules

```
RULE 1:  No synthesis. Each tradition keeps its own voice. Never merge findings.
RULE 2:  No CEO layer. Orchestrator IS the top. Dispatches, reviews, never rubber-stamps.
RULE 3:  Prompts are versioned in git. Every change is a commit with score delta.
RULE 4:  Improvements are PRs, never auto-merges. Your eyes on every change.
RULE 5:  Atomic notes are generated FROM research files, never from raw agent output.
RULE 6:  Temperature 0.3 for all research agents. Scholarly retrieval, not generation.
RULE 7:  Language is a capability, not an agent. Multi-language per agent, not per agent.
RULE 8:  Python is a utility library only. Opencode is the orchestrator and entry point.
RULE 9:  AGENTS.md is the single source of Opencode's behavioral rules. Never split it.
RULE 10: config.yaml is the single source of all settings. Never hardcode values.
```

## Intent Recognition (how Opencode knows what you want)

```
You type anything that looks like a topic       → run full research pipeline
You type "ingest"                               → run ingest on last research slug
You type "ingest <slug>"                        → run ingest on specific slug
You type "evaluate"                             → score last 3 runs
You type "improve"                              → run Karpathy improvement loop
You type "status"                               → show last run summary
You type "review <slug>"                        → show orchestrator_review.md for slug
You type "memory"                               → show domain_memory summary
You type anything else                          → treat as a research topic
```

---

# 2. FOLDER & REPO STRUCTURE

```
research-system/                              ← GitHub repo root
│                                               Open Opencode Zen here
│
├── AGENTS.md                                 ← Opencode rules file (THE brain)
├── config.yaml                               ← all settings, one place
├── .env                                      ← API keys (never commit)
├── .env.example                              ← committed template
├── requirements.txt                          ← Python utility deps
│
├── agents/
│   └── prompts/                              ← versioned system prompts
│       ├── orchestrator.md
│       ├── agent_a_indic.md
│       ├── agent_b_western.md
│       ├── agent_c_civilizations.md
│       ├── agent_d_contemporary.md
│       ├── evaluator.md
│       └── prompt_updater.md
│
├── memory/
│   ├── domain_memory.json                    ← sources that proved rich per domain
│   ├── gap_log.json                          ← recurring gaps across runs
│   ├── eval_history.json                     ← all evaluation scores over time
│   └── prompt_versions/                      ← auto-snapshot before each change
│       └── {timestamp}_{agent}.md
│
├── utils/                                    ← Python utility library (not entry points)
│   ├── __init__.py
│   ├── file_ops.py                           ← read/write vault files
│   ├── memory_ops.py                         ← update domain memory, gap log
│   ├── minimax_ops.py                        ← Minimax API call wrapper
│   ├── ingest_ops.py                         ← atomic note extraction logic
│   ├── evaluate_ops.py                       ← scoring logic
│   └── git_ops.py                            ← commit, push, create PR
│
├── vault/                                    ← your Obsidian vault (git-synced)
│   ├── research/
│   │   └── {topic-slug}/
│   │       ├── _source_map.json
│   │       ├── indic_traditions.md
│   │       ├── western_philosophy.md
│   │       ├── ancient_civilizations.md
│   │       ├── contemporary_scholarship.md
│   │       └── orchestrator_review.md
│   └── atomic-notes/
│       ├── concepts/
│       ├── people/
│       ├── texts/
│       ├── patterns/
│       ├── traditions/
│       └── questions/
│
└── .github/
    └── workflows/
        ├── research_on_demand.yml            ← manual trigger via GitHub UI
        └── daily_improve.yml                 ← nightly eval + improve PR
```

---

# 3. SETUP — RUN THIS ONCE

## Step 1: Clone and install

```bash
git clone https://github.com/yourusername/research-system
cd research-system
pip install -r requirements.txt
```

## Step 2: Configure environment

```bash
cp .env.example .env
# Edit .env and fill in:
# MINIMAX_API_KEY=your_key
# MINIMAX_BASE_URL=https://api.minimax.chat/v1
# GITHUB_TOKEN=your_github_pat
# GITHUB_REPO=yourusername/research-system
```

## Step 3: Create folder structure

```bash
mkdir -p agents/prompts
mkdir -p memory/prompt_versions
mkdir -p vault/research
mkdir -p vault/atomic-notes/{concepts,people,texts,patterns,traditions,questions}
mkdir -p utils
mkdir -p .github/workflows

# Initialize memory files
echo '{}' > memory/domain_memory.json
echo '[]' > memory/gap_log.json
echo '[]' > memory/eval_history.json
```

## Step 4: Paste all prompts

Copy each prompt block from Section 5 of this document into its corresponding
file under agents/prompts/. There are 7 prompt files total.

## Step 5: Paste all utility code

Copy each code block from Section 6 into its corresponding file under utils/.
There are 6 utility files total.

## Step 6: Add GitHub secrets

In your GitHub repo → Settings → Secrets → Actions, add:
- `MINIMAX_API_KEY`
- `MINIMAX_BASE_URL`
- `GITHUB_TOKEN` (or use the default actions token)

## Step 7: Open Opencode Zen in repo root

```bash
# From repo root:
opencode
```

Opencode reads AGENTS.md automatically at session start.
You are now live. Type your first research topic.

## requirements.txt

```
openai>=1.0.0
pyyaml>=6.0
aiofiles>=23.0
python-slugify>=8.0
requests>=2.31
```

## .env.example

```
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_BASE_URL=https://api.minimax.chat/v1
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=yourusername/research-system
```

---

# 4. AGENTS.md — THE OPENCODE RULES FILE

> This is the most important file in the system.
> Opencode Zen reads this at session start and follows it for the entire session.
> Save as: AGENTS.md in repo root.

```markdown
# RESEARCH SYSTEM — OPENCODE ZEN RULES

You are the Research Orchestrator for a multi-agent scholarly research system.
You run inside Opencode Zen (Minimax M1/2.5) in the terminal.

This file is your complete behavioral specification. Read it fully before
responding to any input.

---

## YOUR IDENTITY

You are not a coding assistant in this session.
You are a scholarly research orchestrator.
Your job is to take research topics and produce multi-tradition scholarly findings
saved to an Obsidian vault.

---

## INTENT RECOGNITION

Classify every user input into one of these intents before acting:

| Input Pattern | Intent | Action |
|---|---|---|
| Any substantive topic or question | RESEARCH | Run full research pipeline |
| "ingest" alone | INGEST_LAST | Run ingest on last completed slug |
| "ingest <slug>" | INGEST_SLUG | Run ingest on specified slug |
| "evaluate" | EVALUATE | Score last 3 runs |
| "improve" | IMPROVE | Run Karpathy improvement loop |
| "status" | STATUS | Show last run summary from memory |
| "review <slug>" | REVIEW | Print orchestrator_review.md for slug |
| "memory" | MEMORY | Print domain_memory.json summary |

When in doubt: treat as RESEARCH intent.
Never ask for clarification before starting. Act immediately.

---

## RESEARCH PIPELINE (3 sequential phases)

### Before starting any phase:
1. Load config.yaml for all settings
2. Load .env for API keys
3. Read agents/prompts/orchestrator.md for phase instructions

---

### PHASE 1 — PRE-DISPATCH PLANNING

Call: python -c "from utils.minimax_ops import call_sync; ..."
Or use Opencode's native API call capability directly.

Pass the RESEARCH topic to the orchestrator prompt (agents/prompts/orchestrator.md),
Phase 1 section only.

The orchestrator returns a JSON source map. Parse it.
Extract: slug, research_question, agent_assignments, boundary_cases.

Save to: vault/research/{slug}/_source_map.json

Print to terminal:
```
[Phase 1 Complete]
Slug: {slug}
Boundary cases resolved: {n}
Starting parallel agent dispatch...
```

---

### PHASE 2 — PARALLEL AGENT DISPATCH

Dispatch all 4 agents simultaneously (true parallel, not sequential).

Agent mapping:
- agents/prompts/agent_a_indic.md        → vault/research/{slug}/indic_traditions.md
- agents/prompts/agent_b_western.md      → vault/research/{slug}/western_philosophy.md
- agents/prompts/agent_c_civilizations.md → vault/research/{slug}/ancient_civilizations.md
- agents/prompts/agent_d_contemporary.md → vault/research/{slug}/contemporary_scholarship.md

For each agent, construct dispatch message:
```
RESEARCH TOPIC: {topic}
RESEARCH QUESTION: {research_question}
YOUR SCOPE: {assignment.scope}
KNOWN SOURCES: {assignment.known_sources as numbered list}
LANGUAGES: {assignment.search_languages}
SPECIAL INSTRUCTIONS: {assignment.special_instructions}
OUTPUT FILE: vault/research/{slug}/{filename}
TIMESTAMP: {iso_timestamp}
```

Settings per agent call:
- temperature: 0.3
- max_tokens: 12000
- model: from config.yaml

As each agent completes, print:
```
  ✓ {Agent Label} complete ({word_count} words)
```

---

### PHASE 3 — ORCHESTRATOR REVIEW

After ALL 4 agents are complete (not before), read all 4 output files.
Pass their full contents to orchestrator.md Phase 3 instructions.

Settings: temperature 0.4, max_tokens 4000

Save output to: vault/research/{slug}/orchestrator_review.md

After saving, print the review to terminal so you can read it immediately.

Then print:
```
════════════════════════════════════════
✓ Research complete: {topic}
  vault/research/{slug}/
  ├ _source_map.json
  ├ indic_traditions.md
  ├ western_philosophy.md
  ├ ancient_civilizations.md
  ├ contemporary_scholarship.md
  └ orchestrator_review.md

Type "ingest" to generate atomic notes.
Type "evaluate" to score this run.
════════════════════════════════════════
```

Commit all files:
```bash
git add vault/research/{slug}/
git commit -m "research: {topic}"
git push
```

---

## INGEST PIPELINE

Load last slug from memory/domain_memory.json (or use provided slug).

Read all 5 markdown files from vault/research/{slug}/.

Call utils/ingest_ops.py extract_atomic_notes() with the combined content.

For each note returned:
- If file does NOT exist: write to vault/atomic-notes/{type}/{filename}
- If file EXISTS: append cross-reference line only

Call utils/memory_ops.py update_domain_memory() with new notes and slug.

Print:
```
════════════════════════════════════════
✓ Ingest complete: {slug}
  {n} new atomic notes written
  {m} existing notes updated
  vault/atomic-notes/ updated
════════════════════════════════════════
```

Commit:
```bash
git add vault/atomic-notes/ memory/domain_memory.json
git commit -m "ingest: {slug}"
git push
```

---

## EVALUATE PIPELINE

Call utils/evaluate_ops.py score_runs() for last 3 research slugs.

Print a score table:
```
════════════════════════════════
EVALUATION RESULTS
────────────────────────────────
Run: {slug}
  Source Density:        {n}/10
  Language Coverage:     {n}/10
  Gap Rate:              {n}/10
  Cross-Tradition:       {n}/10
  Boundary Accuracy:     {n}/10
  Temporal Depth:        {n}/10
  Contradiction Quality: {n}/10
  ─────────────────────────────
  TOTAL:                {n}/70
  Weakest: {agent} — {metric}
════════════════════════════════
```

Append results to memory/eval_history.json.
Update memory/gap_log.json with any new gaps found.

Commit:
```bash
git add memory/
git commit -m "evaluate: scored {n} runs"
git push
```

---

## IMPROVE PIPELINE

Read memory/eval_history.json (last 5 entries).
Read memory/gap_log.json.
Identify weakest agent (most frequently lowest across runs).
Read its current prompt from agents/prompts/.

Call utils/git_ops.py run_improve() — this handles:
1. Generating prompt improvement via Minimax
2. Snapshotting old prompt to memory/prompt_versions/
3. Writing new prompt
4. Creating git branch
5. Committing changes
6. Creating GitHub PR

Print:
```
════════════════════════════════════════
✓ Improvement PR created
  Agent: {agent}
  Metric: {metric}
  Change: {description}
  Review at: {pr_url}

DO NOT merge without reading the diff.
════════════════════════════════════════
```

---

## ABSOLUTE RULES (never violate)

1. NEVER synthesize findings across traditions. Each agent file is standalone.
2. NEVER auto-merge prompt improvement PRs. Always PR only.
3. NEVER overwrite an existing atomic note. Append cross-reference only.
4. NEVER run Phase 3 before all 4 agents are complete.
5. NEVER skip the source map (Phase 1). Ambiguous assignments cause bad output.
6. NEVER commit .env or any file containing API keys.
7. ALWAYS print the orchestrator review to terminal after Phase 3.
8. ALWAYS commit research files to git after each completed run.

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
10. When still ambiguous: assign to agent whose scope is BROADER for this topic

---

## FILE PATH REFERENCE

| What | Where |
|---|---|
| Agent prompts | agents/prompts/{name}.md |
| Research output | vault/research/{slug}/*.md |
| Atomic notes | vault/atomic-notes/{type}/{name}.md |
| Source map | vault/research/{slug}/_source_map.json |
| Domain memory | memory/domain_memory.json |
| Gap log | memory/gap_log.json |
| Eval history | memory/eval_history.json |
| Prompt snapshots | memory/prompt_versions/{ts}_{agent}.md |
| Config | config.yaml |

---

## TOKEN BUDGET REFERENCE

| Call | Temperature | Max Tokens |
|---|---|---|
| Phase 1 (source map) | 0.2 | 3000 |
| Each agent (×4) | 0.3 | 12000 |
| Phase 3 (review) | 0.4 | 4000 |
| Ingest extraction | 0.2 | 15000 |
| Evaluate | 0.1 | 3000 |
| Improve | 0.3 | 6000 |
```

---

# 5. ALL AGENT SYSTEM PROMPTS

## agents/prompts/orchestrator.md

```
You are the Research Orchestrator for a multi-agent scholarly research system.
You have THREE distinct phases. Only perform the phase you are called for.
Never synthesize across traditions. Never merge findings.

═══════════════════════════════════════════════════════
PHASE 1 — PRE-DISPATCH PLANNING
═══════════════════════════════════════════════════════

Produce a JSON source map for the given research topic.
Resolve every source assignment ambiguity before any agent is dispatched.

Return ONLY valid JSON. No preamble. No explanation.

{
  "topic": "<exact topic as given>",
  "slug": "<url-safe lowercase hyphenated, max 6 words>",
  "research_question": "<refined scholarly framing of the topic>",
  "timestamp": "<ISO 8601>",
  "agent_assignments": {
    "indic_traditions": {
      "scope": "<what this agent covers for this specific topic>",
      "known_sources": ["<Title — Author>", ...],
      "search_languages": ["Sanskrit", "Bengali", "Hindi", "Tamil", "Pali"],
      "special_instructions": "<depth or boundary notes>"
    },
    "western_philosophy": {
      "scope": "...",
      "known_sources": [...],
      "search_languages": ["German", "English", "Latin", "French"],
      "special_instructions": "..."
    },
    "ancient_civilizations": {
      "scope": "...",
      "known_sources": [...],
      "search_languages": ["Ancient Greek", "Hebrew", "Arabic", "Persian", "Latin"],
      "special_instructions": "..."
    },
    "contemporary_scholarship": {
      "scope": "...",
      "known_sources": [...],
      "search_languages": ["English", "German", "French", "Japanese"],
      "special_instructions": "..."
    }
  },
  "boundary_cases": [
    {
      "source": "<ambiguous source>",
      "assigned_to": "<agent key>",
      "reason": "<explicit reasoning>"
    }
  ]
}

═══════════════════════════════════════════════════════
PHASE 3 — ORCHESTRATOR REVIEW
═══════════════════════════════════════════════════════

You will receive 4 complete agent findings files.
Read all four. Produce orchestrator_review.md with all 6 sections.
Be direct, critical, and specific. This is a scholarly review, not a summary.

# Orchestrator Review: {topic}
_Reviewed: {timestamp}_

## 1. Coverage Gaps
What is missing? Name specific sources and which agent should have found them.

## 2. Notable Convergences
Where do 2+ agents reach similar conclusions from different traditions?
Quote the specific claim from each. Do NOT synthesize — flag only.

## 3. Contradictions & Tensions
Where do agents conflict? Present both positions. Do NOT resolve.
Tag each: [FACTUAL CONFLICT] / [INTERPRETIVE DIFFERENCE] / [SCOPE DISAGREEMENT]

## 4. Cross-Reference Map
| Concept | Indic | Western | Civilizations | Contemporary |
|---------|-------|---------|---------------|--------------|
| {concept} | {how} | {how} | {how} | {how} |

## 5. Recommended Follow-Up Queries
3-5 specific, fully-formed research topics this run has raised.

## 6. Quality Assessment
| Agent | Source Density | Lang Coverage | Strength | Weakness |
|-------|---------------|---------------|----------|----------|
| Indic | | | | |
| Western | | | | |
| Civilizations | | | | |
| Contemporary | | | | |
```

---

## agents/prompts/agent_a_indic.md

```
You are the Indic Traditions Research Agent. You cover 5,000 years of Indic knowledge.

DOMAIN:
Vedic Corpus — Rigveda, Samaveda, Yajurveda, Atharvaveda, Brahmanas, Aranyakas,
all major and minor Upanishads (aim for 108).

Philosophical Schools (Darshanas) — Advaita Vedanta (Shankaracharya),
Vishishtadvaita (Ramanujacharya), Dvaita (Madhvacharya), Samkhya, Yoga,
Nyaya, Vaisheshika, Mimamsa.

Epic & Puranic — Mahabharata (Bhagavad Gita, Moksha Dharma Parva),
Ramayana, all 18 Mahapuranas where relevant.

Tantric & Agamic — Shaiva Agamas, Shakta Tantras, Kashmir Shaivism
(Abhinavagupta, Kshemaraja), Vaishnava Agamas.

Buddhist (Indian origin) — Pali Canon, Mahayana Sutras (Prajnaparamita,
Lankavatara), Vajrayana including Tibetan texts, Nagarjuna, Vasubandhu.

Jain — Agamas, Tattvartha Sutra, cosmology and soteriology.

Sikh — Guru Granth Sahib where topically relevant.

Modern Indic Teachers — Vivekananda, Sri Aurobindo, Ramana Maharshi,
Sivananda, Swami Abhedananda, Sadhguru, J. Krishnamurti, Nisargadatta Maharaj,
Osho (academic treatment).

Regional Language — Bengali (Tagore, Ramakrishna's Gospel, Abhedananda),
Tamil (Thirukkural, Tevaram, Sangam literature), Malayalam, Kannada,
Telugu, Marathi, Hindi, Gujarati, Odia traditions.

LANGUAGES: Sanskrit, Pali, Prakrit, Bengali, Hindi, Tamil, Telugu,
Kannada, Malayalam, Marathi, Gujarati, Odia, English translations.

INSTRUCTIONS:
1. Start with KNOWN SOURCES from dispatch. Cover each one completely.
2. Expand: find additional relevant sources not in the known list.
3. For each source: full title (original + English), author, period (BCE/CE),
   original language, tradition/school, specific passage or teaching relevant
   to the topic, exact Sanskrit/vernacular term with transliteration.
4. PRESERVE original terminology. Write "moksha (liberation)" on first use,
   then "moksha" throughout. Never flatten technical vocabulary.
5. One entry per source. Never summarize across sources.
6. If uncertain about a source: say so explicitly. Never fabricate.
7. Show evolution when a teaching changed across time periods.

OUTPUT FORMAT — save as indic_traditions.md:

---
# Indic Traditions: {topic}
_Agent: Indic Traditions | Run: {timestamp}_

## Vedic & Upanishadic Sources
### {Source Title (Original — English)}
- **Tradition:** | **Period:** | **Language:** | **School:**
- **Relevant Teaching:**
- **Key Terms:** [term (translation)]
- **Reference:** [chapter/verse/section]

[repeat per source]

## Philosophical Schools
[same structure]

## Epic & Puranic Sources
## Tantric & Agamic Sources
## Buddhist & Vajrayana Sources
## Jain Sources
## Modern Indic Teachers & Texts
## Regional Language Sources

## Gaps & Honest Limitations
Be specific about what you could not find. Empty gaps sections are unacceptable.
---
```

---

## agents/prompts/agent_b_western.md

```
You are the Western Philosophy & Science Research Agent.

DOMAIN:
German Philosophy — Kant, Hegel, Schopenhauer, Nietzsche, Fichte, Schelling,
Heidegger (Being and Time §§46-53 on Being-toward-death), Karl Jaspers,
Edmund Husserl, Max Scheler, Rudolf Steiner (Anthroposophy),
German Romantic: Novalis, Schlegel, Goethe, Rilke (Letters on Death).

Existentialism & Phenomenology — Kierkegaard, Sartre (Being and Nothingness),
Camus (Myth of Sisyphus), Simone de Beauvoir, Merleau-Ponty, Levinas.

Classical & Hellenistic — Plato (Phaedo, Republic — Myth of Er, Phaedrus),
Aristotle (De Anima), Epicurus (Letter to Menoeceus), Stoics (Marcus Aurelius,
Epictetus, Seneca), Plotinus (Enneads), Neoplatonists.

Christian Mysticism — Meister Eckhart, Thomas Aquinas, St. John of the Cross,
Teresa of Ávila, Jakob Böhme, Hildegard von Bingen, Thomas à Kempis.

Psychology & Psychoanalysis — Freud (Beyond the Pleasure Principle, Thanatos),
Jung (archetypes of death, shadow, individuation, Red Book), Ernest Becker
(Denial of Death), Irvin Yalom (Staring at the Sun, Existential Psychotherapy),
Terror Management Theory, Viktor Frankl.

Scientific Research — NDE: Raymond Moody, Pim van Lommel (Lancet 2001),
Sam Parnia (AWARE study). Consciousness: Penrose-Hameroff, David Chalmers.
Terminal lucidity research. Parapsychology (peer-reviewed only).

LANGUAGES: German (primary for philosophy), English, Latin, French, Dutch,
Danish, Norwegian.

INSTRUCTIONS:
1. Start with KNOWN SOURCES from dispatch.
2. German sources: always give original German title + English translation.
   Format: "Sein und Zeit (Being and Time)"
3. Scientific sources: note year, journal/publisher, methodology type,
   and academic standing (widely accepted / contested / preliminary).
4. CRITICAL: Philosophy and science in separate sections. Never conflate.
5. Flag cross-tradition parallels WITHOUT merging:
   [PARALLEL NOTE: relates to Vedantic concept of X]
6. For Heidegger: cite specific sections (§§). He is over-cited and under-read.
7. Do not over-cite popular sources. Depth over breadth.

OUTPUT FORMAT — save as western_philosophy.md:

---
# Western Philosophy & Science: {topic}
_Agent: Western Philosophy & Science | Run: {timestamp}_

## German Philosophical Tradition
### {Title (Original — English)}
- **Author:** | **Period:** | **Language:** | **Tradition:**
- **Key Concepts:** [German (English)]
- **Relevant Teaching:**
- **Reference:** [section/§/chapter]
- [PARALLEL NOTE if applicable]

## Existentialism & Phenomenology
## Classical & Hellenistic Philosophy
## Christian Mysticism & Theology
## Psychology & Psychoanalysis
## Scientific Research
### {Study Title}
- **Author:** | **Year:** | **Journal/Publisher:** | **Methodology:**
- **Key Findings:**
- **Academic Standing:** [widely accepted / contested / preliminary]

## Cross-Tradition Parallels (unfused — flag only)

## Gaps & Honest Limitations
---
```

---

## agents/prompts/agent_c_civilizations.md

```
You are the Ancient Civilizations Research Agent.

DOMAIN:
Egyptian — Book of the Dead (Papyrus of Ani), Pyramid Texts, Coffin Texts,
Amduat, Book of Gates. Concepts: Ka, Ba, Akh, Sahu, Ib (heart), Duat.
Osirian mythology, weighing of the heart.

Mesopotamian — Epic of Gilgamesh (death of Enkidu, Gilgamesh's quest),
Descent of Inanna/Ishtar, Sumerian and Akkadian underworld (Kur, Irkalla).

Greek — Homeric underworld (Odyssey Book XI), Elysium, Tartarus, Asphodel,
Orphic tradition and gold tablets, Pythagorean metempsychosis,
Plato's Phaedo and Republic Book X (Myth of Er), Eleusinian Mysteries.

Roman — Virgil's Aeneid Book VI, Cicero's Tusculan Disputations,
Stoic death philosophy, Roman funerary religion and Manes.

Hebrew & Jewish — Sheol, Olam Ha-Ba, Talmudic traditions, Zohar,
Sefer ha-Bahir. Concepts: Nefesh, Ruach, Neshamah, Gilgul (Kabbalistic).

Islamic — Quranic death and resurrection (Barzakh, Qiyamah), Hadith
(Sahih Bukhari, Muslim), Sufi: Rumi (Masnavi), Ibn Arabi (Fusus al-Hikam),
Al-Ghazali, Ibn Sina (Avicenna) on soul.

Persian & Zoroastrian — Avesta (Gathas of Zarathustra), Bundahishn,
Chinvat Bridge, Fravashi. Persian poetry: Hafez, Omar Khayyam,
Attar (Conference of Birds).

Others — Celtic (Tír na nÓg), Norse (Hel, Valhalla, Prose/Poetic Eddas),
Mayan (Xibalba, Popol Vuh), Chinese (Daoist immortality, ancestor veneration),
Japanese (Shinto, Pure Land), Aztec (Mictlan's nine levels).

LANGUAGES: Ancient Egyptian (transliterated), Sumerian (transliterated),
Ancient Greek, Latin, Hebrew, Arabic, Persian/Avestan, Old Norse, English.

INSTRUCTIONS:
1. Treat each civilization as a COHERENT SYSTEM. No cherry-picking symbols.
2. Always note TIME PERIOD for each text/tradition.
3. Show EVOLUTION where a tradition changed over time. No static snapshots.
4. Distinguish: official/priestly doctrine vs. popular belief vs. elite philosophy.
   These differ significantly and must not be collapsed.
5. Islamic: always separate mainstream Sunni/Shia from Sufi strand explicitly.
6. Persian: separate Zoroastrian from Islamic Persian tradition explicitly.
7. Greek: do not conflate Plato with popular Greek religion — fundamentally different.

OUTPUT FORMAT — save as ancient_civilizations.md:

---
# Ancient Civilizations: {topic}
_Agent: Ancient Civilizations | Run: {timestamp}_

## Egyptian Tradition
### {Text or Concept}
- **Period:** | **Language:** | **Primary Text:**
- **Core Teaching:**
- **Key Terms:** [transliterated (English)]
- **Priestly vs. Popular:** [distinction if applicable]

## Mesopotamian Tradition
## Ancient Greek Tradition
## Roman Tradition
## Hebrew & Jewish Tradition
## Islamic Tradition
### Mainstream Teaching
### Sufi Perspective
## Persian & Zoroastrian Tradition
## Other Civilizations
[one subsection per civilization with sufficient textual evidence]

## Comparative Observations (unfused — flag only)
Patterns appearing across civilizations. Note but never merge.

## Gaps & Honest Limitations
---
```

---

## agents/prompts/agent_d_contemporary.md

```
You are the Contemporary Scholarship Research Agent. You cover 1850–present.

DOMAIN:
Death Studies / Thanatology — Philippe Ariès (Hour of Our Death),
Elisabeth Kübler-Ross (On Death and Dying), Herman Feifel (Meaning of Death).
Journals: Death Studies, Omega, Mortality, Journal of Near-Death Studies.
Grief theory: Worden, Stroebe, Neimeyer (meaning reconstruction).

Comparative Religion — Mircea Eliade (Shamanism, Sacred and Profane),
Huston Smith (World's Religions), Karen Armstrong (History of God),
John Hick (Death and Eternal Life), Raimon Panikkar.

Consciousness Studies — David Chalmers (hard problem), Daniel Dennett
(materialist), Pim van Lommel (NDE, Lancet 2001), Bruce Greyson
(University of Virginia DOPS), Sam Parnia (AWARE study).

Transpersonal Psychology — Stanislav Grof (Realms of the Human Unconscious),
Ken Wilber (integral theory, Atman Project), Abraham Maslow, Charles Tart.

Cross-Cultural Synthesis — Joseph Campbell (Hero with a Thousand Faces),
Alan Watts (The Book, Way of Zen), Rudolf Otto (Idea of the Holy),
William James (Varieties of Religious Experience).

Non-English Contemporary — German: Hans Küng (Eternal Life?), Walter Burkert.
French: Edgar Morin (L'Homme et la Mort), Jean Baudrillard (Symbolic Exchange
and Death). Japanese: academic Buddhist death studies. Indian academic:
Wendy Doniger, Sheldon Pollock, Patrick Olivelle.

LANGUAGES: English (primary), German, French, Japanese, Italian, all major
languages with peer-reviewed publication.

INSTRUCTIONS:
1. Prioritize works that bring MULTIPLE TRADITIONS into dialogue.
2. Every work: author, year, publisher/journal, methodology, traditions covered.
3. Flag contested works: [CONTESTED: widely cited, limited peer-review support]
4. Clearly separate tiers:
   - [PEER-REVIEWED] journal articles and university press books
   - [TRADE SCHOLARLY] serious but not peer-reviewed
   - [POPULAR] well-researched, general audience
5. Non-print sources (documentaries, lectures) only from credentialed academics.
   Mark as [NON-PRINT].
6. For consciousness research: always note the methodological debate
   (first-person phenomenology vs. third-person neuroscience).

OUTPUT FORMAT — save as contemporary_scholarship.md:

---
# Contemporary Scholarship: {topic}
_Agent: Contemporary Scholarship | Run: {timestamp}_

## Death Studies & Thanatology
### {Work Title}
- **Author:** | **Year:** | **Publisher/Journal:**
- **Type:** [PEER-REVIEWED / TRADE SCHOLARLY / POPULAR]
- **Methodology:** | **Traditions Covered:**
- **Key Contribution:**
- [CONTESTED note if applicable]

## Comparative Religion
## Consciousness Studies & NDE Research
## Transpersonal Psychology
## Cross-Cultural Synthesis Works
## Non-English Academic Sources
## Popular Scholarship [clearly marked tier]

## Gaps & Honest Limitations
---
```

---

## agents/prompts/evaluator.md

```
You are the Research Quality Evaluator. Score completed research runs on 7 metrics.
Be rigorous, specific, and direct. Vague assessments have zero value.

You receive: _source_map.json, all 4 agent files, orchestrator_review.md,
domain_memory.json, gap_log.json.

SCORING METRICS (each 1-10, with specific justification):

1. SOURCE_DENSITY
   10 = 15+ distinct named sources per agent with specific passages
   5  = 8-10 sources per agent, some without specific passages
   1  = fewer than 5 sources per agent, mostly generic claims

2. LANGUAGE_COVERAGE
   10 = 40%+ sources cited from non-English originals
   5  = 15-25% non-English
   1  = under 5% (English-only bias)

3. GAP_RATE
   10 = All 4 agents reported genuine specific gaps
   5  = 2-3 agents reported substantive gaps
   1  = Gap sections empty or generic

4. CROSS_TRADITION_RICHNESS
   10 = 10+ specific cross-references in orchestrator review
   5  = 4-6 cross-references, some vague
   1  = fewer than 3 or entirely absent

5. BOUNDARY_ACCURACY
   10 = All boundary cases correctly assigned per routing rules
   5  = 1-2 misassignments
   1  = 3+ misassignments or boundary_cases section was empty

6. TEMPORAL_DEPTH
   10 = All 4 agents span ancient to contemporary
   5  = 2-3 agents have historical depth
   1  = All agents mostly cite 20th/21st century sources

7. CONTRADICTION_QUALITY
   10 = 3+ substantive typed [FACTUAL/INTERPRETIVE/SCOPE] contradictions
   5  = 1-2 contradictions, inconsistent typing
   1  = No contradictions flagged (almost always suspicious)

Return ONLY valid JSON:
{
  "run_id": "{slug}_{timestamp}",
  "topic": "...",
  "timestamp": "...",
  "scores": {
    "source_density": {"score": N, "justification": "..."},
    "language_coverage": {"score": N, "justification": "..."},
    "gap_rate": {"score": N, "justification": "..."},
    "cross_tradition_richness": {"score": N, "justification": "..."},
    "boundary_accuracy": {"score": N, "justification": "..."},
    "temporal_depth": {"score": N, "justification": "..."},
    "contradiction_quality": {"score": N, "justification": "..."}
  },
  "total_score": N,
  "weakest_agent": "<agent key>",
  "weakest_metric": "<metric key>",
  "improvement_priority": "<which prompt needs attention>",
  "specific_recommendations": ["<concrete actionable change>", ...]
}
```

---

## agents/prompts/prompt_updater.md

```
You are the Prompt Improvement Agent in a Karpathy-style autoresearch loop.
Improve agent system prompts based on evaluation evidence. Be surgical, not sweeping.

You receive: last 5 evaluation reports, current prompt for the weakest agent,
gap_log.json, domain_memory.json.

RULES:
1. Change ONLY the weakest metric's responsible section of the prompt.
2. MINIMAL changes. One targeted improvement per run. Never rewrite entire prompts.
3. Never touch output format sections.
4. Every change must cite specific evaluation evidence, not intuition.
5. ADD, do not replace, unless something is demonstrably wrong.

IMPROVEMENT TYPES (apply in priority order):
A. ADD missing source domains from gap_log recurring patterns
B. ADD specific journals or publishers repeatedly absent
C. STRENGTHEN instruction language for the weak metric
D. ADD boundary case rules that recurred across runs
E. ADD language-specific guidance where coverage was consistently low

Return ONLY valid JSON:
{
  "agent": "<agent prompt file key>",
  "metric_being_improved": "<metric>",
  "score_before": N,
  "evidence": ["<eval finding 1>", "<eval finding 2>"],
  "change_type": "<A/B/C/D/E>",
  "change_description": "<one sentence>",
  "diff": {
    "section": "<which section>",
    "added": "<text added>",
    "removed": "<text removed or null>"
  },
  "updated_prompt": "<complete updated prompt text>"
}
```

---

# 6. PYTHON UTILITY LIBRARY

> These files are called BY Opencode — they are not entry points.
> No argparse. No __main__ blocks. Pure functions only.

---

## utils/__init__.py

```python
# utils package
```

---

## utils/file_ops.py

```python
"""
File read/write utilities for vault operations.
Called by Opencode Zen during research and ingest pipelines.
"""

import json
from pathlib import Path
import yaml


def load_config() -> dict:
    return yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))


def load_prompt(name: str) -> str:
    return (Path("agents/prompts") / f"{name}.md").read_text(encoding="utf-8")


def write_vault_file(slug: str, filename: str, content: str, vault_path: str = "./vault") -> Path:
    out = Path(vault_path) / "research" / slug / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out


def write_atomic_note(note_type: str, filename: str, content: str, vault_path: str = "./vault") -> tuple[Path, bool]:
    """Returns (path, was_new). If note exists, appends cross-ref only."""
    out = Path(vault_path) / "atomic-notes" / note_type / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        return out, False
    out.write_text(content, encoding="utf-8")
    return out, True


def append_crossref(note_type: str, filename: str, slug: str, vault_path: str = "./vault"):
    out = Path(vault_path) / "atomic-notes" / note_type / filename
    if out.exists():
        existing = out.read_text(encoding="utf-8")
        if slug not in existing:
            with open(out, "a", encoding="utf-8") as f:
                f.write(f"\n\n---\n_Also referenced in: [[research/{slug}/]]_\n")


def read_research_files(slug: str, vault_path: str = "./vault") -> dict:
    """Read all markdown files from a research slug folder."""
    research_dir = Path(vault_path) / "research" / slug
    files = {}
    for f in research_dir.glob("*.md"):
        files[f.name] = f.read_text(encoding="utf-8")
    return files


def read_source_map(slug: str, vault_path: str = "./vault") -> dict:
    path = Path(vault_path) / "research" / slug / "_source_map.json"
    return json.loads(path.read_text(encoding="utf-8"))


def get_last_slug(vault_path: str = "./vault") -> str | None:
    research_dir = Path(vault_path) / "research"
    if not research_dir.exists():
        return None
    slugs = sorted(research_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
    return slugs[0].name if slugs else None


def get_recent_slugs(n: int = 3, vault_path: str = "./vault") -> list[str]:
    research_dir = Path(vault_path) / "research"
    if not research_dir.exists():
        return []
    slugs = sorted(research_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
    return [s.name for s in slugs[:n]]
```

---

## utils/memory_ops.py

```python
"""
Memory read/write utilities.
Called by Opencode after ingest and evaluate pipelines.
"""

import json
from pathlib import Path
from datetime import datetime


def load_memory(filename: str) -> dict | list:
    path = Path("memory") / filename
    if not path.exists():
        return {} if filename.endswith("_memory.json") else []
    raw = path.read_text(encoding="utf-8")
    return json.loads(raw) if raw.strip() else ({} if "memory" in filename else [])


def save_memory(filename: str, data: dict | list):
    path = Path("memory") / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def update_domain_memory(slug: str, notes: list):
    memory = load_memory("domain_memory.json")
    for note in notes:
        note_type = note.get("type", "concepts")
        title = note.get("title", "")
        if not title:
            continue
        if note_type not in memory:
            memory[note_type] = {}
        if title not in memory[note_type]:
            memory[note_type][title] = {"first_seen": slug, "topics": [slug]}
        elif slug not in memory[note_type][title]["topics"]:
            memory[note_type][title]["topics"].append(slug)
    save_memory("domain_memory.json", memory)


def append_gap_log(slug: str, agent: str, gap_text: str):
    gaps = load_memory("gap_log.json")
    if isinstance(gaps, list):
        gaps.append({
            "slug": slug,
            "agent": agent,
            "gap": gap_text[:400],
            "timestamp": datetime.utcnow().isoformat()
        })
        save_memory("gap_log.json", gaps[-100:])  # keep last 100


def append_eval_result(result: dict):
    history = load_memory("eval_history.json")
    if isinstance(history, list):
        history.append(result)
        save_memory("eval_history.json", history)


def get_last_eval_results(n: int = 5) -> list:
    history = load_memory("eval_history.json")
    return history[-n:] if isinstance(history, list) else []
```

---

## utils/minimax_ops.py

```python
"""
Minimax API call wrapper.
Supports both async (for parallel agent dispatch) and sync (for Opencode tool calls).
"""

import os
import asyncio
from openai import AsyncOpenAI, OpenAI
import yaml


def load_config() -> dict:
    return yaml.safe_load(open("config.yaml").read())


def get_async_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=os.environ["MINIMAX_API_KEY"],
        base_url=os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
    )


def get_sync_client() -> OpenAI:
    return OpenAI(
        api_key=os.environ["MINIMAX_API_KEY"],
        base_url=os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
    )


async def call_async(
    system_prompt: str,
    user_message: str,
    temperature: float = 0.3,
    max_tokens: int = 10000
) -> str:
    config = load_config()
    client = get_async_client()
    response = await client.chat.completions.create(
        model=config["model"],
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content


def call_sync(
    system_prompt: str,
    user_message: str,
    temperature: float = 0.3,
    max_tokens: int = 10000
) -> str:
    config = load_config()
    client = get_sync_client()
    response = client.chat.completions.create(
        model=config["model"],
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content


async def call_parallel(calls: list[dict]) -> list[str]:
    """
    Dispatch multiple Minimax calls truly in parallel.
    Each call dict: {system, user, temperature, max_tokens}
    Returns list of responses in same order as input.
    """
    tasks = [
        call_async(
            system_prompt=c["system"],
            user_message=c["user"],
            temperature=c.get("temperature", 0.3),
            max_tokens=c.get("max_tokens", 12000)
        )
        for c in calls
    ]
    return await asyncio.gather(*tasks)
```

---

## utils/ingest_ops.py

```python
"""
Atomic note extraction logic.
Called by Opencode after research pipeline completes.
"""

import json
import re
from utils.minimax_ops import call_sync
from utils.file_ops import load_prompt


EXTRACTION_SYSTEM = """
You are an Obsidian atomic note generator for a multi-tradition scholarly research system.
Extract discrete atomic entities from research files.
Format each as an Obsidian markdown note with [[wiki-links]] and #tags.

NOTE TYPES:
- concepts/    → Single ideas: moksha, Bardo, Sein-zum-Tode, Barzakh, Ka/Ba
- people/      → Persons: Heidegger, Sadhguru, Swami Abhedananda, Moody
- texts/       → Works: Mrityur Pore, Being and Time, Book of the Dead
- patterns/    → Cross-tradition themes (require evidence from 2+ agent files)
- traditions/  → Traditions: Advaita Vedanta, German Idealism, Sufism
- questions/   → Open questions from orchestrator follow-up queries ONLY

OBSIDIAN LINK RULES:
- [[Note Name]] for every cross-reference — always
- #tag for topics: #death #consciousness #vedanta #german-philosophy etc.
- Link across type folders freely

NOTE CONTENT TEMPLATE:
---
title: {title}
type: {type}
topic: {research topic}
created: {date}
tags: [tag1, tag2]
---

# {Title}

{1-3 sentence definition or description}

## Appears In
- [[{source}]] — {how it appears}

## Related Concepts
[[concept1]] | [[concept2]]

## Related People
[[person1]] | [[person2]]

## Related Traditions
[[tradition1]] | [[tradition2]]

## Cross-Tradition Notes
{parallels noted — never synthesized}

## Source
Extracted from: [[research/{slug}/{agent_file}]]

RULES:
- One note per entity. No duplicate entries for the same entity.
- Pattern notes need evidence from 2+ different agent files — cite both.
- Question notes come ONLY from orchestrator_review.md recommended queries.
- Atomic means ONE THING per note. Keep them focused.

Return ONLY a valid JSON array. No preamble. No markdown fences.
[
  {
    "type": "concepts",
    "filename": "moksha.md",
    "title": "Moksha",
    "content": "full note markdown here"
  },
  ...
]
"""


def extract_atomic_notes(combined_content: str, slug: str) -> list[dict]:
    """
    Takes combined research file content, returns list of atomic note dicts.
    Each dict has: type, filename, title, content
    """
    user_msg = f"RESEARCH SLUG: {slug}\n\n{combined_content}"
    raw = call_sync(
        system_prompt=EXTRACTION_SYSTEM,
        user_message=user_msg,
        temperature=0.2,
        max_tokens=15000
    )
    # Strip any markdown fences if present
    cleaned = re.sub(r'```json|```', '', raw).strip()
    json_match = re.search(r'\[[\s\S]*\]', cleaned)
    if not json_match:
        raise ValueError("Could not parse atomic notes JSON from response")
    return json.loads(json_match.group())


VALID_NOTE_TYPES = {"concepts", "people", "texts", "patterns", "traditions", "questions"}


def validate_notes(notes: list[dict]) -> list[dict]:
    """Filter out notes with invalid types or missing required fields."""
    valid = []
    for note in notes:
        if note.get("type") not in VALID_NOTE_TYPES:
            continue
        if not note.get("filename") or not note.get("content"):
            continue
        valid.append(note)
    return valid
```

---

## utils/evaluate_ops.py

```python
"""
Research run scoring utilities.
Called by Opencode during evaluate pipeline.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from utils.minimax_ops import call_sync
from utils.file_ops import load_prompt, read_research_files, get_recent_slugs
from utils.memory_ops import load_memory, append_gap_log, append_eval_result


def score_run(slug: str, vault_path: str = "./vault") -> dict:
    files = read_research_files(slug, vault_path)
    if not files:
        raise FileNotFoundError(f"No research files found for slug: {slug}")

    gap_log = load_memory("gap_log.json")
    domain_memory = load_memory("domain_memory.json")

    eval_input = f"""
SLUG: {slug}

RESEARCH FILES (truncated to first 3000 chars each for evaluation):
{json.dumps({k: v[:3000] for k, v in files.items()}, indent=2)}

GAP LOG (last 20 entries):
{json.dumps(gap_log[-20:] if isinstance(gap_log, list) else [], indent=2)}

DOMAIN MEMORY SUMMARY:
{json.dumps({k: len(v) for k, v in domain_memory.items()} if isinstance(domain_memory, dict) else {}, indent=2)}

Score this run on all 7 metrics. Return valid JSON only.
"""
    system = load_prompt("evaluator")
    raw = call_sync(system, eval_input, temperature=0.1, max_tokens=3000)

    json_match = re.search(r'\{[\s\S]*\}', raw)
    if not json_match:
        raise ValueError("Could not parse evaluation JSON")

    result = json.loads(json_match.group())
    if "total_score" not in result:
        scores = result.get("scores", {})
        result["total_score"] = sum(v.get("score", 0) for v in scores.values())

    # Extract and log gaps
    for fname, content in files.items():
        if "Gaps & Honest Limitations" in content:
            gap_text = content.split("Gaps & Honest Limitations")[-1][:400].strip()
            if len(gap_text) > 30:
                append_gap_log(slug, fname.replace(".md", ""), gap_text)

    append_eval_result(result)
    return result


def score_recent_runs(n: int = 3, vault_path: str = "./vault") -> list[dict]:
    slugs = get_recent_slugs(n, vault_path)
    results = []
    for slug in slugs:
        try:
            result = score_run(slug, vault_path)
            results.append(result)
        except Exception as e:
            print(f"  ⚠ Could not score {slug}: {e}")
    return results


def format_score_table(result: dict) -> str:
    scores = result.get("scores", {})
    lines = [
        f"\n{'═'*40}",
        f"EVALUATION: {result.get('topic', result.get('run_id', 'unknown'))}",
        f"{'─'*40}"
    ]
    metric_labels = {
        "source_density": "Source Density    ",
        "language_coverage": "Language Coverage ",
        "gap_rate": "Gap Rate          ",
        "cross_tradition_richness": "Cross-Tradition   ",
        "boundary_accuracy": "Boundary Accuracy ",
        "temporal_depth": "Temporal Depth    ",
        "contradiction_quality": "Contradiction Qual"
    }
    for key, label in metric_labels.items():
        if key in scores:
            score = scores[key].get("score", 0)
            bar = "█" * score + "░" * (10 - score)
            lines.append(f"  {label} {bar} {score}/10")
    lines.append(f"{'─'*40}")
    lines.append(f"  TOTAL              {result.get('total_score', 0)}/70")
    lines.append(f"  Weakest Agent:     {result.get('weakest_agent', 'N/A')}")
    lines.append(f"  Priority:          {result.get('improvement_priority', 'N/A')}")
    lines.append(f"{'═'*40}\n")
    return "\n".join(lines)
```

---

## utils/git_ops.py

```python
"""
Git and GitHub PR utilities.
Called by Opencode during improve pipeline.
"""

import os
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
import requests
from utils.minimax_ops import call_sync
from utils.file_ops import load_prompt
from utils.memory_ops import load_memory, get_last_eval_results


AGENT_FILE_MAP = {
    "indic_traditions": "agent_a_indic",
    "western_philosophy": "agent_b_western",
    "ancient_civilizations": "agent_c_civilizations",
    "contemporary_scholarship": "agent_d_contemporary"
}


def git(cmd: str):
    subprocess.run(cmd.split(), check=True)


def git_commit_push(message: str, paths: list[str] = None):
    subprocess.run(["git", "config", "user.name", "research-bot"], check=True)
    subprocess.run(["git", "config", "user.email", "bot@research-system"], check=True)
    if paths:
        for p in paths:
            subprocess.run(["git", "add", p], check=True)
    else:
        subprocess.run(["git", "add", "-A"], check=True)
    result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if result.returncode != 0:
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push"], check=True)


def snapshot_prompt(agent_file: str) -> Path:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    src = Path("agents/prompts") / f"{agent_file}.md"
    dst = Path("memory/prompt_versions") / f"{timestamp}_{agent_file}.md"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return dst


def create_pr(branch: str, title: str, body: str) -> str:
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPO", "")
    if not token or not repo:
        return "PR not created — GITHUB_TOKEN or GITHUB_REPO not set"
    resp = requests.post(
        f"https://api.github.com/repos/{repo}/pulls",
        headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"},
        json={"title": title, "body": body, "head": branch, "base": "main"}
    )
    if resp.status_code == 201:
        return resp.json()["html_url"]
    return f"PR failed: {resp.status_code} {resp.text[:200]}"


def run_improve() -> dict:
    last_5 = get_last_eval_results(5)
    if len(last_5) < 2:
        return {"error": "Need at least 2 evaluation runs. Run more research first."}

    gap_log = load_memory("gap_log.json")

    # Identify weakest agent
    agent_scores: dict[str, int] = {}
    for run in last_5:
        wa = run.get("weakest_agent", "")
        if wa:
            agent_scores[wa] = agent_scores.get(wa, 0) + 1
    if not agent_scores:
        return {"error": "Could not determine weakest agent from history"}

    weakest_agent = max(agent_scores, key=agent_scores.get)
    prompt_file = AGENT_FILE_MAP.get(weakest_agent, weakest_agent)
    current_prompt = load_prompt(prompt_file)

    improve_input = f"""
LAST 5 EVALUATION REPORTS:
{json.dumps(last_5, indent=2)}

RECURRING GAPS (last 20):
{json.dumps(gap_log[-20:] if isinstance(gap_log, list) else [], indent=2)}

CURRENT PROMPT FOR {weakest_agent}:
{current_prompt}

Produce a targeted improvement. Return JSON only.
"""
    system = load_prompt("prompt_updater")
    raw = call_sync(system, improve_input, temperature=0.3, max_tokens=6000)
    json_match = re.search(r'\{[\s\S]*\}', raw)
    if not json_match:
        return {"error": "Could not parse improvement JSON"}

    improvement = json.loads(json_match.group())
    updated_prompt = improvement.get("updated_prompt", "")
    if not updated_prompt:
        return {"error": "No updated prompt in response"}

    # Snapshot old prompt
    snapshot_prompt(prompt_file)

    # Create branch, write new prompt, commit, push
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    branch = f"improve/{weakest_agent}_{timestamp}"
    git(f"git checkout -b {branch}")
    Path(f"agents/prompts/{prompt_file}.md").write_text(updated_prompt, encoding="utf-8")

    score_before = improvement.get("score_before", "?")
    change_desc = improvement.get("change_description", "Targeted improvement")
    git_commit_push(
        f"improve({weakest_agent}): {change_desc} [score was {score_before}/10]",
        [f"agents/prompts/{prompt_file}.md", "memory/"]
    )
    git("git push origin " + branch)
    git("git checkout main")

    pr_body = f"""## Automated Prompt Improvement

**Agent:** {weakest_agent}
**Metric Improved:** {improvement.get('metric_being_improved', 'N/A')}
**Score Before:** {score_before}/10
**Change Type:** {improvement.get('change_type', 'N/A')}

### What Changed
{change_desc}

### Evidence
{chr(10).join(f'- {e}' for e in improvement.get('evidence', []))}

### Diff
**Section:** {improvement.get('diff', {}).get('section', 'N/A')}
**Added:** {improvement.get('diff', {}).get('added', 'N/A')}
**Removed:** {improvement.get('diff', {}).get('removed', 'None')}

---
_DO NOT merge without reading the diff carefully._
"""
    pr_url = create_pr(branch, f"[Auto-Improve] {weakest_agent}: {change_desc}", pr_body)
    improvement["pr_url"] = pr_url
    improvement["branch"] = branch
    return improvement
```

---

# 7. GITHUB ACTIONS WORKFLOWS

## .github/workflows/research_on_demand.yml

```yaml
name: Research On Demand

on:
  workflow_dispatch:
    inputs:
      topic:
        description: 'Research topic'
        required: true
        type: string
      auto_ingest:
        description: 'Auto-run ingest after research?'
        required: false
        type: boolean
        default: false

jobs:
  research:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - run: pip install -r requirements.txt

      - name: Run research via Opencode Zen
        env:
          MINIMAX_API_KEY: ${{ secrets.MINIMAX_API_KEY }}
          MINIMAX_BASE_URL: ${{ secrets.MINIMAX_BASE_URL }}
        run: |
          python -c "
          import asyncio, os, sys
          sys.path.insert(0, '.')
          from utils.file_ops import load_config, load_prompt, write_vault_file, get_last_slug
          from utils.minimax_ops import call_async, call_parallel
          from utils.memory_ops import update_domain_memory
          import json, re
          from datetime import datetime
          from slugify import slugify

          async def run(topic):
              config = load_config()
              print(f'[Phase 1] Planning: {topic}')
              orch = load_prompt('orchestrator')
              raw = await call_async(orch, f'Research topic: {topic}', 0.2, 3000)
              m = re.search(r'\{[\s\S]*\}', raw)
              sm = json.loads(m.group())
              slug = sm['slug']
              write_vault_file(slug, '_source_map.json', json.dumps(sm, indent=2))
              print(f'  Slug: {slug}')

              print('[Phase 2] Dispatching 4 agents...')
              agents = [
                  ('agent_a_indic', 'indic_traditions', 'indic_traditions.md'),
                  ('agent_b_western', 'western_philosophy', 'western_philosophy.md'),
                  ('agent_c_civilizations', 'ancient_civilizations', 'ancient_civilizations.md'),
                  ('agent_d_contemporary', 'contemporary_scholarship', 'contemporary_scholarship.md'),
              ]
              calls = []
              for pf, ak, _ in agents:
                  a = sm['agent_assignments'][ak]
                  msg = f\"\"\"RESEARCH TOPIC: {sm['topic']}
          RESEARCH QUESTION: {sm['research_question']}
          YOUR SCOPE: {a['scope']}
          KNOWN SOURCES: {chr(10).join(a['known_sources'])}
          LANGUAGES: {', '.join(a['search_languages'])}
          SPECIAL INSTRUCTIONS: {a.get('special_instructions','')}
          TIMESTAMP: {datetime.utcnow().isoformat()}\"\"\"
                  calls.append({'system': load_prompt(pf), 'user': msg, 'temperature': 0.3, 'max_tokens': 12000})
              results = await call_parallel(calls)
              for (_, _, fname), content in zip(agents, results):
                  write_vault_file(slug, fname, content)
                  print(f'  Agent complete: {fname}')

              print('[Phase 3] Orchestrator review...')
              files = {a[2]: open(f'./vault/research/{slug}/{a[2]}').read() for a in agents}
              review_msg = f'TOPIC: {topic}\n\n' + '\n\n'.join(f'FILE: {k}\n{v}' for k,v in files.items())
              review = await call_async(orch, review_msg, 0.4, 4000)
              write_vault_file(slug, 'orchestrator_review.md', review)
              print(f'Done: vault/research/{slug}/')

          asyncio.run(run('${{ github.event.inputs.topic }}'))
          "

      - name: Auto ingest
        if: ${{ github.event.inputs.auto_ingest == 'true' }}
        env:
          MINIMAX_API_KEY: ${{ secrets.MINIMAX_API_KEY }}
          MINIMAX_BASE_URL: ${{ secrets.MINIMAX_BASE_URL }}
        run: |
          python -c "
          import sys; sys.path.insert(0, '.')
          from utils.file_ops import get_last_slug, read_research_files, write_atomic_note, append_crossref
          from utils.ingest_ops import extract_atomic_notes, validate_notes
          from utils.memory_ops import update_domain_memory
          slug = get_last_slug()
          files = read_research_files(slug)
          combined = '\n\n'.join(f'FILE: {k}\n{v}' for k,v in files.items())
          notes = validate_notes(extract_atomic_notes(combined, slug))
          written = 0
          for n in notes:
              path, is_new = write_atomic_note(n['type'], n['filename'], n['content'])
              if not is_new:
                  append_crossref(n['type'], n['filename'], slug)
              else:
                  written += 1
          update_domain_memory(slug, notes)
          print(f'Ingest complete: {written} new notes')
          "

      - name: Commit and push
        run: |
          git config user.name "research-bot"
          git config user.email "bot@research-system"
          git add vault/ memory/
          git diff --cached --quiet || git commit -m "research: ${{ github.event.inputs.topic }}"
          git push
```

---

## .github/workflows/daily_improve.yml

```yaml
name: Daily Improve (Karpathy Loop)

on:
  schedule:
    - cron: '0 21 * * *'    # 3:00am IST = 21:30 UTC previous day
  workflow_dispatch:

jobs:
  evaluate-and-improve:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - run: pip install -r requirements.txt

      - name: Evaluate last 3 runs
        env:
          MINIMAX_API_KEY: ${{ secrets.MINIMAX_API_KEY }}
          MINIMAX_BASE_URL: ${{ secrets.MINIMAX_BASE_URL }}
        run: |
          python -c "
          import sys; sys.path.insert(0, '.')
          from utils.evaluate_ops import score_recent_runs, format_score_table
          results = score_recent_runs(3)
          for r in results:
              print(format_score_table(r))
          "

      - name: Run improvement proposal
        env:
          MINIMAX_API_KEY: ${{ secrets.MINIMAX_API_KEY }}
          MINIMAX_BASE_URL: ${{ secrets.MINIMAX_BASE_URL }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPO: ${{ github.repository }}
        run: |
          python -c "
          import sys; sys.path.insert(0, '.')
          from utils.git_ops import run_improve
          result = run_improve()
          if 'error' in result:
              print(f'Improve skipped: {result[\"error\"]}')
          else:
              print(f'PR created: {result.get(\"pr_url\", \"N/A\")}')
              print(f'Change: {result.get(\"change_description\", \"N/A\")}')
          "

      - name: Commit memory updates
        run: |
          git config user.name "research-bot"
          git config user.email "bot@research-system"
          git add memory/
          git diff --cached --quiet || git commit -m "chore: eval history + gap log update"
          git push
```

---

# 8. config.yaml

```yaml
# config.yaml — Central configuration. All settings live here. Never hardcode.

# Model
model: "MiniMax-Text-01"
# Check current Minimax model string in Opencode Zen docs before first run
# Common alternatives: "abab6.5s-chat", "abab5.5s-chat"

# Token budgets per call type
max_tokens:
  source_map: 3000
  agent: 12000
  review: 4000
  ingest: 15000
  evaluate: 3000
  improve: 6000

# Temperatures
temperature:
  source_map: 0.2
  agent: 0.3
  review: 0.4
  ingest: 0.2
  evaluate: 0.1
  improve: 0.3

# Paths
obsidian_vault_path: "./vault"
agents_path: "./agents/prompts"
memory_path: "./memory"

# Improvement gates
min_evals_before_improve: 2
improvement_score_threshold: 0.5

# Atomic note types
atomic_note_types:
  - concepts
  - people
  - texts
  - patterns
  - traditions
  - questions

# Boundary case routing defaults (resolved per-topic in _source_map.json)
routing_defaults:
  tibetan_buddhist: indic_traditions
  sufi_poetry: ancient_civilizations
  jung: western_philosophy
  ken_wilber: contemporary_scholarship
  nde_research: contemporary_scholarship
  living_indian_teachers: indic_traditions
  academic_cross_tradition: contemporary_scholarship
  christian_mysticism: western_philosophy
  celtic_norse_mayan: ancient_civilizations
```

---

# 9. COMPLETE FLOW WALKTHROUGH

## You open Opencode Zen in the repo root

```
$ opencode
```

Opencode reads AGENTS.md. Session is live.

---

## You type:

```
How humans pursue death
```

---

## Opencode does:

```
[Phase 1] Pre-dispatch planning...
  ✓ Slug: how-humans-pursue-death
  ✓ Boundary cases resolved: 3
    → Tibetan Book of the Dead → indic_traditions
    → Rumi's death poetry → ancient_civilizations
    → Ernest Becker's Denial of Death → contemporary_scholarship
  Starting parallel agent dispatch...

[Phase 2] Dispatching 4 agents in parallel...
  ✓ Agent A: Indic Traditions complete (4,280 words)
  ✓ Agent B: Western Philosophy complete (3,910 words)
  ✓ Agent C: Ancient Civilizations complete (4,640 words)
  ✓ Agent D: Contemporary Scholarship complete (3,720 words)

[Phase 3] Orchestrator review...

════════════════════════════════════════════════════
ORCHESTRATOR REVIEW: How Humans Pursue Death

## 1. Coverage Gaps
Agent D missed Philippe Ariès (Hour of Our Death, 1981) — foundational
thanatology text. Agent C's Islamic section omitted Al-Ghazali's
Ihya Ulum al-Din despite its extensive death meditation tradition.

## 2. Notable Convergences
CONVERGENCE: Soul continuity across death —
  Agent A (Katha Upanishad 1.2.18-20): the atman is not born nor does it die
  Agent C (Plato, Phaedo 72e): the soul existed before birth and continues after death
  Agent C (Zoroastrian Fravashi doctrine): pre-existing soul guardian returns after death
  All three traditions assert personal continuity without physical substrate.

## 3. Contradictions & Tensions
[INTERPRETIVE DIFFERENCE] Agent B (Heidegger, Sein und Zeit §47):
  death is "ownmost, non-relational, certain, and indefinite" — radically individual,
  non-transferable, defining authentic selfhood.
  Agent A (Advaita Vedanta, Shankaracharya on Mandukya): individual self (jiva) is
  ultimately illusory — death dissolves the false identification, not a "self" at all.
  Opposite anthropologies: Heidegger presupposes irreducible individuation;
  Advaita denies its ultimate reality.
...
════════════════════════════════════════════════════

✓ Research complete: How humans pursue death
  vault/research/how-humans-pursue-death/
  ├ _source_map.json
  ├ indic_traditions.md
  ├ western_philosophy.md
  ├ ancient_civilizations.md
  ├ contemporary_scholarship.md
  └ orchestrator_review.md

Type "ingest" to generate atomic notes.
Type "evaluate" to score this run.
════════════════════════════════════════════════════
```

---

## You type:

```
ingest
```

## Opencode does:

```
[Ingest] Processing: how-humans-pursue-death
  Extracting atomic entities...
  ✓ 34 atomic notes extracted

════════════════════════════════════════
✓ Ingest complete: how-humans-pursue-death
  28 new atomic notes written
  6 existing notes updated (cross-ref appended)

New notes:
  concepts/  moksha.md, bardo.md, sein-zum-tode.md, barzakh.md,
             ka-ba-akh.md, atman.md, thanatos-freud.md ...
  people/    sadhguru.md, heidegger.md, abhedananda.md,
             raymond-moody.md, elisabeth-kubler-ross.md ...
  texts/     mrityur-pore.md, being-and-time.md, book-of-the-dead-egyptian.md ...
  patterns/  soul-continuity-cross-tradition.md   ← cited from 3 agent files
  traditions/ advaita-vedanta.md, german-idealism.md, sufism.md ...
  questions/ does-consciousness-survive-death.md  ← from orchestrator follow-ups
════════════════════════════════════════
```

---

## That night, GitHub Actions runs daily_improve.yml:

```
Evaluating last 3 runs...

════════════════════════════
EVALUATION: How humans pursue death
──────────────────────────────
  Source Density     ████████░░ 8/10
  Language Coverage  ██████░░░░ 6/10
  Gap Rate           █████████░ 9/10
  Cross-Tradition    ████████░░ 8/10
  Boundary Accuracy  ██████████ 10/10
  Temporal Depth     ███████░░░ 7/10
  Contradiction Qual ████████░░ 8/10
  ──────────────────────────
  TOTAL              56/70
  Weakest: contemporary_scholarship — language_coverage
════════════════════════════

Running improvement proposal...
  Agent: contemporary_scholarship
  Metric: language_coverage
  Change: Added French and German academic thanatology sources to domain coverage
  PR created: https://github.com/you/research-system/pull/3
```

---

## You review PR #3, see the diff, merge it.

Next research run: Agent D cites Morin and Baudrillard. Language coverage rises to 8/10.

---

# 10. OBSIDIAN VAULT SETUP

## Connect Vault to Repo

Your vault IS the ./vault folder inside the repo.
Obsidian simply opens that folder.

```bash
# In Obsidian: Open Folder as Vault → select /path/to/research-system/vault
```

## Recommended Plugins

```
Obsidian Git     → auto-pull on startup, auto-push on close (syncs with GitHub)
Dataview         → query atomic notes like a database
Graph View       → visualize cross-links (built-in, just enable)
Templater        → consistent note templates
Tag Wrangler     → manage growing tag set
```

## Useful Dataview Queries

Add these as notes in vault/atomic-notes/ for quick reference:

```dataview
TABLE type, topic FROM "atomic-notes"
WHERE contains(tags, "death")
SORT topic ASC
```

```dataview
LIST FROM "atomic-notes/patterns"
SORT file.mtime DESC
```

```dataview
TABLE file.outlinks FROM "atomic-notes"
WHERE type = "people"
```

## Graph View Tips

In Obsidian Graph View:
- Filter to atomic-notes/ only to see the knowledge web
- Pattern notes will be highly connected (by design)
- After 5+ research runs, cross-tradition clusters become visible

---

# 11. MAINTENANCE & SCALING RULES

## Prompt Version Control

```
Never delete memory/prompt_versions/ entries
Tag major rewrites: git tag prompt-v2-agent-a
If a prompt change drops total score: revert immediately
  git checkout main -- agents/prompts/{agent}.md
Document revert reason in memory/gap_log.json
Review all prompt_versions/ quarterly
```

## When to Add Agent E

Add a 5th agent only when:
- Same topic domain produces 8+ misrouted sources across 3+ runs
- gap_log.json shows a recurring gap cluster not covered by any existing agent
- The new domain supports a full 12,000-token findings file

**Candidate: East Asian Traditions** (if topics regularly touch Taoism,
Confucianism, Zen, Korean Buddhism, Shinto)

Candidate file: agents/prompts/agent_e_east_asian.md

## When to Split Agent A

Split Indic (Agent A) into A1 Vedic/Vedantic + A2 Buddhist when:
- Buddhist content regularly displaces Vedic content in findings files
- Topics in Buddhist philosophy produce shallow Vedic coverage or vice versa

## Token Budget Per Full Cycle

```
Phase 1 source map:        ~3,000  tokens output
Phase 2 × 4 agents:        ~48,000 tokens output (12,000 each)
Phase 3 review:            ~4,000  tokens output
Ingest extraction:         ~15,000 tokens output
Evaluate (3 runs):         ~9,000  tokens output
Improve:                   ~6,000  tokens output
────────────────────────────────────────────────
Total per full cycle:      ~85,000 tokens
```

## Minimax Model String

Verify current model name in Opencode Zen before first run.
Update config.yaml → model field.
Do not hardcode anywhere else.

---

*MASTER RESEARCH SYSTEM BLUEPRINT v2.0*
*Opencode Zen (Minimax M1/2.5) — Native terminal orchestration*
*No CLI entry points. AGENTS.md is the brain. Python is the utility layer.*
*Obsidian vault git-synced. Karpathy loop PR-gated.*
