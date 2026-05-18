# OpenCode Autoresearch System

## Overview

This is the autonomous research system for your team of specialist agents. Each specialist can experiment, learn, and improve over time without retraining the underlying LLM.

## Core Concept

Inspired by Andrej Karpathy's AutoResearch (https://github.com/karpathy/autoresearch), we use a **ratchet mechanism**: successful improvements get committed while failures get reverted, ensuring monotonic progress.

## System Architecture

```
.autoresearch/
├── program.md              # This file - defines research priorities (you edit)
├── results.tsv             # Experiment log (auto-generated)
├── specialists/
│   ├── nexus/              # Research specialist
│   │   ├── program.md      # Research instructions (agent modifies)
│   │   ├── workspace/      # Research patterns, prompts, frameworks
│   │   └── memory/        # Nexus's learned experiences
│   ├── flux/               # Coder specialist
│   ├── vector/             # Writer specialist
│   ├── cipher/             # Analyst specialist
│   └── ...other specialists
```

## The Experiment Cycle

Each specialist follows this loop:

1. Read their `program.md` to understand current priorities
2. Examine their `workspace/` and recent results in `results.tsv`
3. Propose a hypothesis: a change to prompts, patterns, or approaches
4. Modify their workspace files to implement the change
5. Run a test task (limited scope)
6. Evaluate the result using domain-specific metrics
7. If improvement: keep the change; if not: revert

## Evaluation Metrics by Specialist

| Specialist | Metric | Lower is Better |
|------------|--------|-----------------|
| CEO (Axiom) | `val_delegation` - task-specialist matching | No |
| CEO (Axiom) | `val_coordination` - workflow efficiency | No |
| CEO (Axiom) | `val_outcome` - final quality rating | No |
| Nexus (Research) | `val_accuracy` - citation/source quality | No |
| Flux (Coder) | `val_passrate` - test pass rate | No |
| Vector (Writer) | `val_coherence` - style consistency score | Yes |
| Cipher (Analyst) | `val_error_rate` - inference error rate | Yes |
| Stage (Presenter) | `val_clarity` - audience comprehension score | Yes |
| Orbit (Planner) | `val_completion` - task completion rate | No |
| Sync (Organizer) | `val_organization` - file/tag consistency | Yes |
| Brief (Summarizer) | `val_retention` - key info preservation | No |
| Prism (Reviewer) | `val_recall` - error detection rate | No |
| Pulse (Coordinator) | `val_efficiency` - workflow overhead | Yes |

## Time Budget

Each experiment runs for a **fixed 1-minute time budget** (excluding startup). This ensures fair comparison across different approaches.

## Memory Architecture

Each specialist maintains three memory layers:

- **Episodic**: Recent task-specific experiences (last 10 interactions)
- **Semantic**: Generalized principles extracted from experiences
- **Skills**: Reusable, composable behaviors specific to their domain

## Customization

Edit `program.md` to change research priorities. The specialists read this file to understand what to optimize for.

---

*AutoResearch System v1.0 - Inspired by karpathy/autoresearch*