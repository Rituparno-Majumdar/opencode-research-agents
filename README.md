# OpenCode Research Agents

A multi-agent research orchestration system that runs inside [OpenCode](https://opencode.ai) and saves findings to an [Obsidian](https://obsidian.md) vault.

Type a research topic. Five specialized agents research it in parallel, each from a distinct epistemic lens. An orchestrator synthesizes findings, evaluates quality, and improves the weakest agent over time — automatically.

---

## The System

This is not a wrapper around a single LLM call. It is a research pipeline built around three core ideas:

### 1. Epistemic Parallelism

Most multi-agent systems parallelize for speed. This system parallelizes for *perspective*. Each agent represents a non-overlapping epistemic domain — a tradition, discipline, or era — with its own source base and language set. Before any agent runs, the orchestrator builds a source map that explicitly assigns every aspect of the topic to the right agent and resolves boundary ambiguities. Agents never see each other's output. Cross-tradition synthesis happens only in Phase 3, after all agents complete, in the orchestrator's hands.

The result: each agent goes deep into its domain rather than producing a generic survey. The orchestrator's job is to find the surprising connections that a single-agent system would never surface.

### 2. Luhmann Linkage — A Digital Zettelkasten

After each research run, the ingest pipeline extracts atomic notes and builds a directional knowledge graph inspired by Niklas Luhmann's Zettelkasten. Luhmann's insight was that knowledge grows not from accumulation but from *connection* — each slip connects forward, backward, and laterally to other slips, creating emergent structure that no single note contains.

This system implements that principle digitally, across traditions:

| Link type | Syntax | Meaning |
|---|---|---|
| Causal | `A → B` | A causes or produces B |
| Effect | `A ← B` | A is produced by or results from B |
| Convergence | `A ↔ B` | A and B are parallel concepts across traditions |

The orchestrator's Phase 3 convergence map drives the cross-tradition `↔` links. A note on *saṃskāra* (Indic) automatically links to *automaticity* (cognitive science) and *Verdrängung* (Freudian) because the orchestrator identified that convergence. No manual curation needed.

Over time, the vault becomes a navigable knowledge graph — not a flat archive.

### 3. Self-Improving Agents

After every run, the system evaluates its own output on seven metrics: source density, language coverage, gap rate, cross-tradition richness, boundary accuracy, temporal depth, and contradiction quality. It logs specific gaps, identifies the weakest agent, generates a targeted prompt improvement, and opens a GitHub PR for your review. You approve the PR. The next run is measurably better.

This is the system's memory. It accumulates evidence of what it missed and repairs itself through each cycle.

---

## Quick Start

**Prerequisites:** [OpenCode](https://opencode.ai), a Gemini API key, a GitHub account

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/opencode-research-agents.git
cd opencode-research-agents

# 2. Configure credentials
cp .env.example .env
# Edit .env: add GEMINI_API_KEY, GITHUB_TOKEN, GITHUB_REPO

# 3. Install OpenCode dependencies
cd .opencode && npm install && cd ..

# 4. Copy the example agents (philosophy/comparative religion domain set)
cp examples/philosophy-research/.agents/prompts/*.md .agents/prompts/

# 5. Open this folder as your Obsidian vault
# In Obsidian: Open folder as vault → select this directory

# 6. Start OpenCode
opencode
> What is the relationship between consciousness and matter?
```

Research files appear in `vault/research/{topic-slug}/` and open as Obsidian notes.

---

## Commands

| Type this | What happens |
|---|---|
| Any topic or question | Runs the full 4-phase research pipeline |
| `ingest` | Extracts atomic notes from the last run into `vault/atomic-notes/` |
| `evaluate` | Scores the last 3 runs and identifies the weakest component |
| `improve` | Generates a prompt improvement and opens a GitHub PR |
| `status` | Shows a summary of the last run |
| `memory` | Prints domain memory (research history, key concepts) |
| `merge` | Merges an approved improvement PR into main |

---

## What's Included

```
.agents/prompts/          Core agents (orchestrator, atomic notes, improvement)
examples/
  philosophy-research/    Complete 5-agent example: comparative philosophy across traditions
templates/
  .agents/prompts/        Blank agent template — start here for custom domains
docs/
  SETUP.md                Full installation and configuration guide
  ARCHITECTURE.md         How the pipeline works under the hood
  CUSTOMIZATION.md        How to define your own research domains
vault/                    Obsidian vault — research output and atomic notes land here
.memory/                  Evaluation history, gap log, amendment tracking
config.yaml               All system settings (model, token budgets, routing rules)
AGENTS.md                 Behavioral spec read by OpenCode on every run
AGENTS_REFERENCE.md       Reference manual for scripts, routing, and token budgets
```

---

## The Philosophy Research Example

`examples/philosophy-research/` contains a fully configured 5-agent setup for comparative philosophy and religious studies — chosen because it stress-tests all three innovations simultaneously: maximum epistemic diversity, maximum cross-tradition convergence potential, and the highest density of boundary cases.

| Agent | Domain |
|---|---|
| Agent A | Indic traditions — Vedic, Buddhist, Jain, Tantric, Sikh |
| Agent B | Western philosophy — German idealism, Greek, existentialism, Christian mysticism |
| Agent C | Ancient civilizations — Egyptian, Mesopotamian, Norse, Celtic, Mayan |
| Agent D | Contemporary scholarship — cross-tradition academic research, African philosophy |
| Agent E | Science & technology — consciousness science, quantum physics, AI |

Copy into `.agents/prompts/` to run out of the box, or use as reference when building your own domain set.

---

## Building Your Own Domain Set

1. Copy `templates/.agents/prompts/agent_template.md` to `.agents/prompts/`
2. Fill in domain, language, and source sections
3. Update the Phase 2 agent mapping in `AGENTS.md`
4. Add boundary case routing in `config.yaml`

See `docs/CUSTOMIZATION.md` for a step-by-step walkthrough.

---

## Roadmap

- **NVIDIA NIM integration** — run the pipeline on 50+ open models (Llama, Mistral, DeepSeek, Qwen) using the NVIDIA API Catalog. Free tier available. Add `NVIDIA_API_KEY` to `.env` and set the model in `config.yaml`.
- **OpenRouter support** — single API key for 200+ models as an alternative provider.
- **Web UI** — a lightweight dashboard for browsing research runs and the atomic notes graph.

---

## Architecture

For a detailed explanation of the 3-phase pipeline, evaluation system, and prompt improvement loop — see `docs/ARCHITECTURE.md`.

---

## License

MIT
