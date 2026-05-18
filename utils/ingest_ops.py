"""
Atomic note extraction logic.
Reads combined research files, returns structured atomic note objects.
"""

import json
import re
from utils.openrouter_ops import call_sync


EXTRACTION_SYSTEM = """
You are an Obsidian atomic note generator for a multi-tradition scholarly research system.
Extract discrete atomic entities from research files.
Format each as an Obsidian markdown note with [[wiki-links]] and #tags.
Preserve all non-English script, transliteration, and translation blocks exactly as found.

NOTE TYPES:
  concepts/    → Single ideas: moksha, Bardo, Sein-zum-Tode, Barzakh, Ka/Ba
  people/      → Persons: Heidegger, Sadhguru, Swami Abhedananda, Moody
  texts/       → Works: Mrityur Pore, Being and Time, Book of the Dead
  patterns/    → Cross-tradition themes (require evidence from 2+ agent files)
  traditions/  → Traditions: Advaita Vedanta, German Idealism, Sufism
  questions/   → Open questions from orchestrator_review.md follow-ups ONLY

OBSIDIAN LINK RULES:
  [[Note Name]] for every cross-reference — always
  #tag for topics: #death #consciousness #vedanta #german-philosophy etc.
  Link freely across type folders

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

## Original Language
[Include any non-English script, transliteration, and translation blocks
exactly as they appeared in the source research file]

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
- One note per entity. No duplicates.
- Pattern notes need evidence from 2+ agent files — cite both.
- Question notes come ONLY from orchestrator_review.md recommended queries.
- Atomic means ONE THING per note.
- Preserve all original script + transliteration blocks from the research files.

Return ONLY a valid JSON array. No preamble. No markdown fences.
[{"type": "...", "filename": "...", "title": "...", "content": "..."}, ...]
"""

VALID_NOTE_TYPES = {
    "concepts", "people", "texts", "patterns", "traditions", "questions"
}


def extract_atomic_notes(combined_content: str, slug: str) -> list[dict]:
    user_msg = f"RESEARCH SLUG: {slug}\n\n{combined_content}"
    raw = call_sync(
        system_prompt=EXTRACTION_SYSTEM,
        user_message=user_msg,
        temperature=0.2,
        max_tokens=15000
    )
    cleaned = re.sub(r'```json|```', '', raw).strip()
    json_match = re.search(r'\[[\s\S]*\]', cleaned)
    if not json_match:
        raise ValueError("Could not parse atomic notes JSON from response")
    return json.loads(json_match.group())


def validate_notes(notes: list[dict]) -> list[dict]:
    return [
        n for n in notes
        if n.get("type") in VALID_NOTE_TYPES
        and n.get("filename")
        and n.get("content")
    ]