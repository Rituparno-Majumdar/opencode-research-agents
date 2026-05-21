# How to Effectively & Efficiently Use OpenCode

**Executive Summary:** OpenCode is an open-source AI coding agent (160K GitHub stars, 7.5M monthly devs) that runs in terminal, desktop, or IDE. This guide covers installation, daily workflow, agent system, skills/MCP, configuration, and pro tips for power users — tailored to your research orchestration setup.

## 1. What Is OpenCode?

- **Open-source** AI coding agent by Anomaly (formerly Claude Code alternative)
- Runs in **TUI** (terminal), **CLI** (scriptable), **Web**, **Desktop** (beta), or **IDE** extension
- Supports **75+ LLM providers** via Models.dev (Claude, GPT, Gemini, local models, etc.)
- **LSP-enabled** — auto-loads language servers for code intelligence
- **Multi-session** — run parallel agents on the same project
- **Your current setup**: OpenCode Zen (Minimax M1/2.5), configured for research orchestration

## 2. Installation & Setup

```bash
# Quick install (curl)
curl -fsSL https://opencode.ai/install | bash

# Or via npm/brew
npm install -g opencode-ai
brew install anomalyco/tap/opencode

# Start in a project
cd /path/to/project
opencode

# First-run: configure a provider
/connect   # in TUI, or `opencode auth login`
/init      # generates AGENTS.md by scanning your project
```

## 3. TUI Daily Workflow (Core Loop)

| Action | How |
|--------|-----|
| Start session | `opencode` in project root |
| Ask a question | Type naturally. Use `@filename` to reference files |
| Attach images | Drag & drop into terminal |
| **Plan mode** | Press **Tab** — analyzes without making changes |
| **Build mode** | Press **Tab** again — executes changes |
| Undo | `/undo` (can run multiple times) |
| Redo | `/redo` |
| Share session | `/share` → creates a link for team |

**Pro tip**: Always use Plan mode (Tab) before big changes. Iterate on the plan, *then* switch to Build.

## 4. Agent System

OpenCode has two agent types:

### Primary Agents (Tab to cycle)

| Agent | Mode | Description |
|-------|------|-------------|
| **Build** | Primary (default) | Full tool access — writes code, runs commands |
| **Plan** | Primary | Read-only analysis. Use for architecture review, planning |

### Subagents (@mention to invoke)

| Agent | Tool | Best for |
|-------|------|----------|
| `@general` | Full except todo | Multi-step tasks, parallel research |
| `@explore` | Read-only | Fast codebase search & navigation |
| `@scout` | Read-only | External dependency research, docs lookup |

**Usage example:**
```
@explore how is authentication handled in this codebase?
@general find all API endpoints and list them
```

### Creating Custom Agents

```bash
opencode agent create
# Interactive: description → permissions → model → saves as .md
```

Or manually in `opencode.json`:
```json
{
  "agent": {
    "code-reviewer": {
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "permission": { "edit": "deny", "bash": "deny" },
      "prompt": "Review code for security, performance, and maintainability."
    }
  }
}
```

## 5. Skills System (236 installed)

Skills are `SKILL.md` files that OpenCode auto-discovers and loads on-demand.

### Discovery locations (in priority order):
1. `.opencode/skills/<name>/SKILL.md`
2. `~/.config/opencode/skills/<name>/SKILL.md`
3. `.claude/skills/<name>/SKILL.md` (Claude Code compat)
4. `~/.claude/skills/<name>/SKILL.md`

### How skills work:
- Listed in the `skill` tool description with name + description
- Loaded via `skill({ name: "skill-name" })` 
- You don't need to invoke them manually — I recognize intent and load relevant skills

### Top skills for your workflow:

| Skill | What it does | Trigger phrase |
|-------|-------------|---------------|
| `deep-research` | Web search + synthesis with citations | "Research X thoroughly" |
| `content-engine` | Platform-native posts (X, LinkedIn, newsletter) | "Write a post about..." |
| `article-writing` | Long-form guides, blogs in your voice | "Write an article on..." |
| `research-ops` | Current-state evidence gathering | "Get current facts on..." |
| `knowledge-ops` | Save/sync/deduplicate knowledge | "Save this to my vault" |
| `literature-review` | Academic search & synthesis | "Lit review on..." |
| `investor-materials` | Reports, proposals, decks | "Create a proposal for..." |
| `brand-voice` | Capture your writing style | "Learn my voice from these posts" |
| `crosspost` | Multi-platform distribution | "Post this everywhere" |
| `data-scraper-agent` | Automated monitoring | "Scrape prices/jobs from..." |

## 6. Rules System (AGENTS.md)

Your project's `AGENTS.md` (root) + `~/.config/opencode/AGENTS.md` (global) act as persistent instructions.

**Precedence order:**
1. `./AGENTS.md` (project)
2. `./CLAUDE.md` (if no AGENTS.md)
3. `~/.config/opencode/AGENTS.md` (global)
4. `~/.claude/CLAUDE.md` (fallback)

**Your setup**: AGENTS.md defines a multi-agent research orchestrator with intent recognition, 3-phase pipeline, ingest/evaluate/improve cycles, and boundary case routing.

## 7. MCP Servers (External Tools)

MCP servers add external capabilities. Configure in `opencode.json`:

```json
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

**Recommended for your setup:**
- `context7` — Library/framework documentation lookup
- `sentry` — Error monitoring
- `gh_grep` (grep.app) — Search code examples on GitHub

## 8. CLI & Scripting

Run OpenCode non-interactively:

```bash
# One-shot question
opencode run "Explain how async/await works in JS"

# Continue last session
opencode -c

# Use specific model
opencode -m anthropic/claude-sonnet-4-20250514

# Start headless server (for API access)
opencode serve --port 4096

# Web interface
opencode web

# View usage stats
opencode stats

# Export session
opencode export <session-id>
```

**Headless attachment pattern** (faster subsequent runs):
```bash
# Terminal 1: start server
opencode serve

# Terminal 2: attach without cold-boot MCP
opencode run --attach http://localhost:4096 "Your prompt here"
```

## 9. Permissions & Safety

Control what agents can do in `opencode.json`:

```json
{
  "permission": {
    "edit": "ask",     // Ask before file edits
    "bash": "allow",   // Allow all commands
    "webfetch": "allow"
  },
  "agent": {
    "build": {
      "permission": {
        "bash": { "*": "ask", "git status": "allow", "npm test": "allow" }
      }
    }
  }
}
```

Values: `"allow"` | `"ask"` | `"deny"`

## 10. Pro Tips for Efficiency

1. **Use `@file` references** — `@src/index.ts` adds context without copying
2. **Plan before build** — Always Tab to Plan mode for complex changes
3. **Pin key agents** — Create custom agents for frequent tasks (code review, docs)
4. **Use `/undo` fearlessly** — It's reliable; iterate on prompts
5. **Share sessions** — `/share` for debugging with team
6. **Stats tracking** — `opencode stats` shows token usage and costs
7. **Environment shortcuts**:
   - `OPENCODE_ENABLE_EXA=1 opencode` — enables web search
   - `OPENCODE_DISABLE_AUTOCOMPACT=1` — disable context compaction
8. **Multi-session** — Run `opencode` in multiple terminals on same project
9. **Export/import** — `opencode export <id>` → share as JSON or restore with `opencode import`
10. **Custom commands** — Define in `opencode.json` for common tasks

## 11. Your Research System Architecture

```
opencode (TUI)
  ├── AGENTS.md → research orchestrator (intent → pipeline)
  ├── config.yaml → model, tokens, routing defaults
  ├── .agents/prompts/ → 5 agent prompts + orchestrator
  ├── .memory/ → eval history, gap log, domain memory
  ├── vault/research/{slug}/ → output files
  ├── vault/atomic-notes/ → Zettelkasten notes
  └── .opencode/
      ├── opencode.json → skills path, plugins
      └── skills/ui-ux-pro-max/ → custom project skill
```

**Flow**: Intent → Phase 1 (source map) → Phase 2 (5 parallel agents) → Phase 3 (orchestrator review) → Ingest → Atomic notes → Commit

## 12. Cheat Sheet

```bash
opencode                    # Start TUI
opencode run "..."          # One-shot
opencode -c                 # Continue last session
/init                       # Generate/update AGENTS.md
/undo                       # Undo last change
/redo                       # Redo
/share                      # Share session link
Tab                         # Toggle Plan/Build mode
@explore / @general         # Invoke subagents
opencode agent create       # Interactive agent creator
opencode mcp add            # Add MCP server interactively
opencode stats              # View token usage
opencode upgrade            # Update to latest
```

## Review Checklist

- [ ] Installation & provider configuration verified
- [ ] Tab-switching between Plan/Build modes tested
- [ ] At least one custom agent created for frequent task
- [ ] AGENTS.md committed to git
- [ ] MCP servers configured for documentation lookup
- [ ] Permissions set to comfort level (allow/ask/deny)
- [ ] Skills auto-loaded during actual task execution
