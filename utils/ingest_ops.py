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
    from utils.minimax_ops import load_config
    config = load_config()
    user_msg = f"RESEARCH SLUG: {slug}\n\n{combined_content}"
    raw = call_sync(
        system_prompt=EXTRACTION_SYSTEM,
        user_message=user_msg,
        temperature=0.2,
        max_tokens=config["max_tokens"]["ingest"]
    )
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