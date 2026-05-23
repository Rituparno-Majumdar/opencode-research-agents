# Customization Guide

## Changing the Research Domain

The philosophy research example ships in `examples/philosophy-research/`. To replace it with your own domain set:

### Step 1 — Design your agent set

Decide how many agents you need and how to divide the domain. Aim for:
- Clear, non-overlapping scopes
- Explicit boundary cases where two agents might claim the same topic
- Between 3 and 7 agents (fewer = faster, more = deeper coverage)

Examples of domain sets you might build:
- **Business research:** Markets, Regulation, Technology, Sociology, History
- **Medical research:** Biomedical, Clinical, Epidemiology, Psychology, Policy
- **Literary research:** English, European, Asian, African, Contemporary

### Step 2 — Create your agent prompts

For each domain agent:

```bash
cp templates/.agents/prompts/agent_template.md .agents/prompts/agent_your_domain.md
```

Fill in every `[placeholder]`:
- **SCOPE** — what this agent covers and what it explicitly excludes
- **LANGUAGES & SOURCES** — primary languages and preferred source types
- The structural output format can stay as-is or be adapted to your domain

### Step 3 — Update AGENTS.md Phase 2

In `AGENTS.md`, find the Phase 2 agent mapping and update it to reference your files:

```markdown
Agent mapping:
- .agents/prompts/agent_your_domain_1.md → vault/research/{slug}/domain_1.md
- .agents/prompts/agent_your_domain_2.md → vault/research/{slug}/domain_2.md
...
```

Also update the Phase 3 completion message to list your new filenames.

### Step 4 — Define boundary case routing

In `config.yaml`, add routing rules for topics that could belong to multiple agents:

```yaml
routing_defaults:
  your_boundary_topic: your_agent_name
  another_boundary_topic: another_agent_name
```

The orchestrator uses these defaults when a topic is ambiguous. Rules are applied in order — more specific rules should come before more general ones.

---

## Changing the Model

Update `model` in `config.yaml`:

```yaml
model: "gemini-2.5-flash"  # default
# or: "gemini-2.5-pro", "minimax-m1", etc.
```

OpenCode supports multiple model providers. Check OpenCode documentation for supported model IDs.

---

## Adjusting Token Budgets

Each call type has its own budget in `config.yaml`:

```yaml
max_tokens:
  source_map: 3000    # Phase 1 planning
  agent: 12000        # Each domain agent (most important to tune)
  review: 4000        # Orchestrator synthesis
  ingest: 15000       # Atomic note extraction
  evaluate: 6000      # Scoring
  improve: 6000       # Prompt generation
```

**If agents produce thin output:** Increase `agent` to 16000-20000.
**If costs are high:** Reduce `agent` to 8000 (quality will drop for complex topics).

---

## Adjusting the Improvement Threshold

Two settings control when the auto-improvement loop triggers:

```yaml
min_evals_before_improve: 2      # Minimum runs before improvement triggers
improvement_score_threshold: 0.5  # Agent must be below 60% of max to trigger
```

Increase `improvement_score_threshold` to 0.7 if you want more aggressive improvement. Decrease to 0.4 to only improve severe underperformance.

---

## Disabling the Improvement Loop

If you don't use GitHub or don't want automatic PR creation, remove Steps C and D from Phase 3 in `AGENTS.md`. The evaluation (Step A) and gap logging (Step B) are independent and can be kept.

---

## Atomic Note Types

The default note types are defined in `config.yaml`:

```yaml
atomic_note_types:
  - concepts
  - people
  - texts
  - patterns
  - traditions
  - questions
```

Add or remove types here. Each type gets its own subdirectory under `vault/atomic-notes/`. The ingest agent will sort notes into these categories automatically.

---

## Using a Different Obsidian Vault

By default the Obsidian vault IS this repository (the `vault/` subdirectory is inside it). To use a separate Obsidian vault for reading output:

1. Set `OBSIDIAN_SECOND_BRAIN_PATH` in `.env` to a path inside your main vault
2. After each research run, files are copied there automatically (Phase 4)
3. The source repo vault still receives the files — the sync is a copy, not a move

---

## Disabling the Script Triad System

If your domain doesn't involve non-English scripts, simplify the output format by editing the agent prompts. Remove the "SCRIPT TRIAD SYSTEM" section from each agent and replace with a simpler citation format.
