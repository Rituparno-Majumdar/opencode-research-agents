# Agent Templates

## How to create a domain agent

1. Copy `agent_template.md` to `.agents/prompts/` with a descriptive name:
   ```bash
   cp templates/.agents/prompts/agent_template.md .agents/prompts/agent_your_domain.md
   ```

2. Fill in every `[placeholder]` section:
   - **SCOPE** — what topics this agent covers and what it excludes
   - **LANGUAGES & SOURCES** — primary languages, scripts, and preferred sources
   - **ABSOLUTE RULES** — keep rules 1-6, add domain-specific ones

3. Update `AGENTS.md` Phase 2 to reference your new file:
   ```
   .agents/prompts/agent_your_domain.md → vault/research/{slug}/your_domain.md
   ```

4. Update `config.yaml` routing defaults if your domain has boundary cases with other agents.

## Tips

- Fewer, well-defined agents produce better results than many overlapping ones.
- Boundary cases (topics that could belong to 2+ agents) must be explicitly routed in `config.yaml`.
- The template's `Cross-Reference Candidates` section helps the orchestrator link findings.
- See `examples/philosophy-research/` for a complete 5-agent setup you can adapt.
