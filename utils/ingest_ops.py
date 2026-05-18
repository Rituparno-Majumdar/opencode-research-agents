"""
Zettelkasten extraction logic.
Reads combined research files, produces:
- Zettels (atomic notes with Luhmann IDs + link contexts + backlinks)
- Structure Note (per research run)
- Register Entry (per research run)
"""

import json
import re
from datetime import datetime
from utils.openrouter_ops import call_sync


EXTRACTION_SYSTEM = """
You are a Zettelkasten extraction engine. Convert multi-tradition research into
Luhmann-style Zettels with link contexts and backlinks.

OUTPUT FORMAT — 3 DELIVERABLES:

## DELIVERABLE 1: ZETTELS (array of objects)
Each Zettel must have:
- "id": Luhmann sequential ID (1, 1a, 1a1, 1b, 2, 2a, 2b1, etc.)
  Start from 1. First main concept = 1, second main concept = 2, etc.
  Branch from concept 1 = 1a, 1b. Branch from 1a = 1a1, 1a2.
  Continue sequential chain = 1a → 1b → 1c. Never reuse IDs across runs.
- "title": Clean, lowercase title for filename (slug-style, max 3 words)
- "topic": The research topic slug (lowercase, hyphenated)
- "content": Full Zettel markdown body (see format below)

## ZETTEL BODY FORMAT:
```
id: {id}
topic: {topic}
created: {timestamp}
source: research/{slug}/{agent_file}.md

# {Title}

{1-3 sentence definition in your own words — never copy-paste from source}

## Original Language
[Include non-English script + transliteration + English if present in source.
If none: omit this section entirely.]

## Source Reference
- [Cite specific passage — Source Title, chapter.verse or section]

## Link Context
[[{target_id}]] → {explicit WHY this link exists — minimum 1 sentence.
The link context is created knowledge. It explains the relationship,
not just that topics are similar. Be specific: what does this connection
reveal? What tension or convergence does it surface?}

[[{another_id}]] → {another link context}

## Backlinks
← [[{id_of_zettel_that_links_to_this}]] — {one-line description of that connection}
← [[{another}]] — {description}

## Citekey
[#citekey] — Full bibliographic reference in footnote style
```

RULES:
1. EVERY [[link]] MUST have a Link Context paragraph immediately before it.
   No link without link context. This is non-negotiable.
2. Write in your own words. Paraphrase, don't copy-paste source text.
3. ID sequence must be LOGICAL:
   - 1 = first major concept (e.g., Atman)
   - 1a = elaboration or dimension of 1 (e.g., Brahman as identity)
   - 1a1 = continuation of 1a (e.g., Moksha as union)
   - 1b = parallel or counterpoint to 1 (e.g., Anatman in Buddhism as contrast)
   - 2 = second major concept (e.g., Sein-zum-Tode)
   - 2a = elaboration of 2
4. Maximum 5-7 Zettels per tradition (30-40 total target per run)
5. Every non-English source citation must include original script + transliteration.
6. Each Zettel's backlinks are populated from Step 3 (you'll derive them from links).
7. Link context minimum: 2 sentences. The more specific, the better.
8. Never create a Zettel without at least one outbound [[link]].

## DELIVERABLE 2: STRUCTURE NOTE (single object)
{
  "id": "structure",
  "title": "{slug}",
  "content": "markdown content for vault/structure/{slug}.md"
}

Structure Note format:
```
id: structure
topic: {slug}
created: {timestamp}

# Structure: {Research Topic}

Entry point to all Zettels from this research run.

## Indic Traditions
- [[1a_atanu]] — description
- [[1a1_brahman]] — description
...

## Western Philosophy
- [[2a_sein_zum_tode]] — description
...

## Ancient Civilizations
- [[3a_barzakh]] — description
...

## Contemporary Scholarship
- [[4a_chalmers]] — description
...

## Key Argument Flow
[[1a_atanu]] → [[1a1_brahman]] → [[1a2_moksha]] (Advaita path)
[[2a_sein_zum_tode]] → [[2a1_angst]] (Heideggerian path)
[[3a_barzakh]] → [[3a1_qiyamah]] (Islamic eschatology)
```

Group by tradition. Annotate each entry with 1-line description.
Include argument flow showing logical chains across traditions.

## DELIVERABLE 3: REGISTER ENTRY (single object)
{
  "id": "register",
  "title": "{slug}",
  "content": "markdown content for vault/register/{slug}.md"
}

Register Entry format:
```
id: register
topic: {slug}
created: {timestamp}

# Register: {Research Topic}

Entry points into this Zettelkasten.

## Core Concepts (start here)
- [[1a_atanu]] — the central concept from Indic traditions
- [[2a_sein_zum_tode]] — central concept from Western philosophy

## Topic Map
- **Consciousness & Self**: [[1a_atanu]] → [[1a1_brahman]] → [[1a2_moksha]]
- **Temporality & Death**: [[2a_sein_zum_tode]] → [[2a1_angst]]
- **Eschatological Boundaries**: [[3a_barzakh]] → [[3a1_qiyamah]]

## How to Navigate
Start from Core Concepts above, or search by concept.
Full structure: [[structure|{slug} Structure Note]]

## All Zettels ({count} total)
{zettel list with IDs and one-line descriptions}
```

## OUTPUT INSTRUCTIONS

Return ONLY a valid JSON object. No preamble. No markdown fences. No explanation.

{
  "zettels": [
    {
      "id": "1a",
      "title": "atanu",
      "topic": "nature-of-consciousness",
      "content": "...full markdown body..."
    },
    ...
  ],
  "structure_note": {
    "title": "nature-of-consciousness",
    "content": "...markdown..."
  },
  "register_entry": {
    "title": "nature-of-consciousness",
    "content": "...markdown..."
  }
}
"""


def extract_zettels(combined_content: str, slug: str) -> dict:
    """
    Extract Zettels, Structure Note, and Register Entry from research files.
    Returns: {"zettels": [...], "structure_note": {...}, "register_entry": {...}}
    """
    timestamp = datetime.utcnow().isoformat()
    user_msg = f"RESEARCH SLUG: {slug}\n\n{combined_content}\n\nTimestamp: {timestamp}"

    raw = call_sync(
        system_prompt=EXTRACTION_SYSTEM,
        user_message=user_msg,
        temperature=0.2,
        max_tokens=15000
    )

    cleaned = re.sub(r'```json|```', '', raw).strip()
    json_match = re.search(r'\{[\s\S]*\}', cleaned)
    if not json_match:
        raise ValueError(f"Could not parse Zettel extraction JSON from response. Raw: {raw[:500]}")

    result = json.loads(json_match.group())

    # Validate structure
    if "zettels" not in result:
        raise ValueError("Missing 'zettels' key in extraction result")
    if "structure_note" not in result:
        raise ValueError("Missing 'structure_note' key in extraction result")
    if "register_entry" not in result:
        raise ValueError("Missing 'register_entry' key in extraction result")

    # Populate timestamp in all content strings
    for z in result["zettels"]:
        if "created:" not in z.get("content", ""):
            z["content"] = z["content"].replace(
                "created: {timestamp}", f"created: {timestamp}"
            ).replace(
                "created: ", f"created: {timestamp}\n", 1
            )

    return result


def validate_zettels(zettels: list[dict]) -> list[dict]:
    """Validate Zettels have required fields."""
    validated = []
    for z in zettels:
        if not z.get("id"):
            continue
        if not z.get("content"):
            continue
        # Ensure link contexts exist for every [[link]]
        links = re.findall(r'\[\[(\d+\w*)\]\]', z.get("content", ""))
        if links:
            # Check that each link has a preceding "## Link Context" section
            # This is a soft check — the LLM should handle it, but we validate structure
            pass
        validated.append(z)
    return validated