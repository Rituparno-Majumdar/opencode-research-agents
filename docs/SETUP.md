# Setup Guide

## Prerequisites

| Requirement | Notes |
|---|---|
| [OpenCode](https://opencode.ai) | The CLI that orchestrates the agents |
| Node.js 18+ | For OpenCode dependencies |
| Gemini API key | Get one free at [aistudio.google.com](https://aistudio.google.com/apikey) |
| GitHub account + personal access token | For the prompt improvement PR workflow |
| [Obsidian](https://obsidian.md) | For reading research output (optional but recommended) |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/opencode-research-agents.git
cd opencode-research-agents
```

### 2. Install OpenCode dependencies

```bash
cd .opencode
npm install
cd ..
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=yourusername/opencode-research-agents
```

**Getting a GitHub token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with `repo` scope
3. Copy it into `.env`

**Optional:** If you want research files synced to a separate Obsidian vault:
```env
OBSIDIAN_SECOND_BRAIN_PATH=/path/to/your/obsidian-vault/raw/research
```

### 4. Set up the agents

The system expects domain agents in `.agents/prompts/`. The repository ships with three core agents already in place:
- `orchestrator.md` — coordinates all phases
- `agent_atomic_notes.md` — extracts atomic notes
- `improvement_agent.md` — generates prompt improvements

For domain research agents, either:

**Option A:** Use the philosophy research example (works out of the box):
```bash
cp examples/philosophy-research/.agents/prompts/*.md .agents/prompts/
```

**Option B:** Build your own domain agents:
```bash
cp templates/.agents/prompts/agent_template.md .agents/prompts/agent_your_domain.md
# Edit the file, then update AGENTS.md Phase 2 to reference it
```

### 5. Open as an Obsidian vault

In Obsidian: **Open folder as vault** → select the `opencode-research-agents` directory.

The vault directory structure is pre-configured. Research output lands in `vault/research/` and atomic notes in `vault/atomic-notes/`.

### 6. Run your first topic

```bash
opencode
```

OpenCode reads `AGENTS.md` automatically. Type any research topic:

```
> consciousness and the hard problem
```

Watch the 4-phase pipeline run. Output files appear in `vault/research/consciousness-and-the-hard-problem/`.

---

## Configuration Reference

All system settings live in `config.yaml`:

| Setting | Default | Description |
|---|---|---|
| `model` | `gemini-2.5-flash` | LLM model for all agents |
| `max_tokens.agent` | `12000` | Token budget per research agent |
| `max_tokens.review` | `4000` | Token budget for orchestrator review |
| `temperature.agent` | `0.3` | Temperature for research agents |
| `temperature.evaluate` | `0.1` | Temperature for evaluation (keep low) |
| `min_evals_before_improve` | `2` | Runs before improvement triggers |
| `improvement_score_threshold` | `0.5` | Score threshold that triggers improvement |
| `routing_defaults` | see file | Boundary case routing rules |

---

## Troubleshooting

**OpenCode doesn't read AGENTS.md**
OpenCode reads `AGENTS.md` or `CLAUDE.md` automatically when present in the working directory. Make sure you're running `opencode` from the repo root.

**Agents produce short or generic output**
Check that `max_tokens.agent` in `config.yaml` is set to at least 8000. Also verify the model name is correct for your API provider.

**GitHub token errors**
The token needs `repo` scope (full control of private repos). Re-generate if unsure.

**Obsidian doesn't show new notes**
Obsidian auto-refreshes. If notes don't appear, click the vault refresh button or restart Obsidian.

**Improvement PRs not creating**
Verify `GITHUB_REPO` in `.env` matches your actual repo in `username/repo-name` format.
