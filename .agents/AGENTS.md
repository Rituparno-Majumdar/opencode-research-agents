# LLM Wiki - AGENTS.md

This file instructs OpenCode how to maintain a persistent wiki knowledge base. The wiki sits between you (the user) and your raw sources — it's a structured, interlinked collection of markdown files that accumulates knowledge over time.

## Core Philosophy

- **You** curate sources, ask questions, and think about meaning
- **OpenCode** handles all bookkeeping: summarizing, cross-referencing, updating, maintaining
- The wiki is a **persistent, compounding artifact** — knowledge is compiled once and kept current

---

## Directory Structure

```
.agents/          # This schema file
raw/              # Immutable source documents (never modified)
  sources/        # All input sources (articles, books, research, scans)
  assets/         # Downloaded images & photos of book pages
wiki/             # LLM-generated content (OpenCode writes here)
  index.md       # Content catalog - all pages with links & summaries
  log.md         # Chronological activity log
  entities/      # People, places, things
  concepts/      # Topics, ideas, theories
  sources/       # Source summaries
  synthesis/     # Overviews, analyses, comparisons
outputs/         # Generated artifacts (slides, charts, etc.)
```

---

## Source Ingestion Methods

All sources flow into `raw/sources/` as `.md` files. There are four ways to add sources:

### 1. Book Fetch
- Use the prompt in `templates/book-fetch-prompt.md`
- Trigger: `Fetch book: [Title] by [Author]`
- Output: Chapter-by-chapter summary saved to `raw/sources/[Title].md`

### 2. Research
- Use the prompt in `templates/research-prompt.md`
- Trigger: `Research topic: [Topic]`
- Output: Full scholarly document saved to `raw/sources/YYYY-MM-DD-topic-slug.md`

### 3. Obsidian Web Clipper
- Clip articles via browser extension
- Images auto-download to `raw/assets/` (Ctrl+Shift+D)
- Saved as `.md` to `raw/sources/`

### 4. Photos of Book Pages
- You add photos to `raw/assets/`
- I OCR/extract text and save to `raw/sources/`
- Process during next ingest

---

## Workflows

### Ingest (Adding a Source)

When you drop a new source into `raw/sources/` and request ingest:

1. **Read the source** - Extract key information, claims, and connections
2. **Discuss with you** - Highlight takeaways, what matters
3. **Write source summary** - Create `wiki/sources/<source-title>.md`
4. **Update index** - Add new page to `wiki/index.md` with one-line summary
5. **Update affected pages** - Touch 10-15 wiki pages: entity pages, concept pages, cross-references
6. **Log it** - Append entry to `wiki/log.md`

**Single source flow (recommended):** You add one source, we discuss, I update the wiki together. You'll see changes in real-time in Obsidian.

### Query (Asking Questions)

When you ask a question against the wiki:

1. **Search index** - Read `wiki/index.md` to find relevant pages
2. **Read relevant pages** - Drill into those pages
3. **Synthesize answer** - Generate response with citations `[[page-name]]`
4. **File back (if valuable)** - Good answers become new wiki pages in `wiki/synthesis/`

**Output formats:** Markdown, comparison tables, Marp slides, matplotlib charts. Choose what fits.

### Lint (Health Check)

Periodically, ask me to lint the wiki:

1. **Find contradictions** - Flag claims that newer sources contradict
2. **Find stale content** - Claims superseded by newer sources
3. **Find orphans** - Pages with no inbound links
4. **Find gaps** - Concepts mentioned but lacking pages
5. **Suggest exploration** - New questions to ask, new sources to find

---

## File Conventions

### Naming
- Pages: `kebab-case.md` (e.g., `attention-mechanism.md`)
- Entities: `Entity-Name.md` (e.g., `Andrej-Karpathy.md`)
- Sources: `source-<title>.md` (e.g., `source-llm-wiki-pattern.md`)

### Frontmatter (all wiki pages)
```yaml
---
title: Page Title
created: 2026-05-17
updated: 2026-05-17
tags: [concept, ai]
sources: []
---
```

### Cross-references
- Use Obsidian links: `[[page-name]]`
- Backlinks are automatic in Obsidian

### Index Format
```markdown
# Wiki Index

## Entities
- [[Entity-Name]] - One-line description

## Concepts
- [[concept-name]] - One-line description

## Sources
- [[source-title]] - One-line description
```

### Log Format
```markdown
# Wiki Log

## [2026-05-17] ingest | Source Title
- Action taken

## [2026-05-17] query | Your question
- Answer summary
```

---

## Rules

1. **Never modify raw sources** - Read only, never write to `raw/`
2. **Update comprehensively** - Single ingest touches all affected pages
3. **Link proactively** - Create cross-references, not silos
4. **Flag contradictions** - When sources conflict, note it explicitly
5. **File有价值的内容** - Good answers become permanent wiki pages
6. **Keep index current** - Update on every ingest
7. **Log everything** - Every action goes to `wiki/log.md`

---

## Tips

- Use Obsidian Web Clipper to add sources quickly
- Use Ctrl+Shift+D hotkey to download images locally to `raw/assets/`
- Check Graph View to see wiki structure
- Dataview can query frontmatter for dynamic tables

---

## Agent Tracking

Before invoking any subagent, log the task in `.agents/agent-manifest.md`:

```
### [AGENT_NAME]
- [HH:MM] [task description] | PENDING | [expected output]
- Template: /absolute/path/to/template.md
- Output: /absolute/path/to/output.md
```

**CRITICAL: Always use absolute paths** for both template and output locations when invoking subagents. Relative paths may resolve incorrectly.

After completion, update with:
- STATUS: COMPLETED / FAILED
- OUTPUT: actual file path
- Verified: check file exists at specified path

**Parallel tasks:** List all agents being invoked together for visibility. Max 4-5 simultaneous.

---

## Customization

This schema is a starting point. Evolve it based on what works for your domain. Add conventions, new page types, or workflows as you learn.