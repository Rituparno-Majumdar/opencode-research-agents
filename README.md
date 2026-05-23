# OpenCode Research Agents

A multi-agent research orchestration system that runs inside [OpenCode](https://opencode.ai) and saves findings to an [Obsidian](https://obsidian.md) vault.

Type a research topic. Five specialized agents research it in parallel from their assigned domains. An orchestrator synthesizes their findings, identifies gaps, and automatically improves the weakest agent over time through a GitHub PR workflow.

---

## Quick Start

For Obsidian users who want to run the system with minimal setup:

**Prerequisites:** [OpenCode](https://opencode.ai), a Gemini API key, a GitHub account

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/opencode-research-agents.git
cd opencode-research-agents

# 2. Configure your credentials
cp .env.example .env
# Edit .env: add your GEMINI_API_KEY, GITHUB_TOKEN, and GITHUB_REPO

# 3. Install OpenCode dependencies
cd .opencode && npm install && cd ..

# 4. Open this folder as your Obsidian vault
# In Obsidian: Open folder as vault → select this directory

# 5. Start OpenCode and run your first research topic
opencode
> What is the relationship between consciousness and matter?
```

Research files appear in `vault/research/{topic-slug}/` and open as Obsidian notes.

---

## What Happens When You Run a Topic

The system runs a 4-phase pipeline:

```
Phase 1 → Orchestrator creates a source map: who researches what
Phase 2 → 5 agents run in parallel, each writing a research file
Phase 3 → Orchestrator synthesizes findings, scores quality, flags gaps
Phase 4 → (Optional) Sync research files to a second Obsidian vault
```

After each run, the system automatically evaluates itself on 7 metrics (source density, language coverage, cross-tradition richness, and more) and creates a GitHub PR to improve the weakest agent. You review the PR, merge it, and the next run is better.

---

## Commands

| Type this | What happens |
|---|---|
| Any topic or question | Runs the full research pipeline |
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

`examples/philosophy-research/` contains a fully configured 5-agent setup for comparative philosophy and religious studies:

| Agent | Domain |
|---|---|
| Agent A | Indic traditions — Vedic, Buddhist, Jain, Tantric, Sikh |
| Agent B | Western philosophy — German idealism, Greek, existentialism, Christian mysticism |
| Agent C | Ancient civilizations — Egyptian, Mesopotamian, Norse, Celtic, Mayan |
| Agent D | Contemporary scholarship — cross-tradition academic research |
| Agent E | Science & technology — consciousness science, quantum physics, AI |

Copy these agents into `.agents/prompts/` to run the philosophy system out of the box, or use them as reference when building your own domain set.

---

## Building Your Own Domain Set

1. Copy `templates/.agents/prompts/agent_template.md` to `.agents/prompts/`
2. Fill in the domain, language, and source sections
3. Update the Phase 2 agent mapping in `AGENTS.md`
4. Add boundary case routing in `config.yaml`

See `docs/CUSTOMIZATION.md` for a step-by-step walkthrough.

---

## Architecture Overview

For a detailed explanation of the 3-phase pipeline, evaluation system, and prompt improvement loop — see `docs/ARCHITECTURE.md`.

---

## License

MIT
