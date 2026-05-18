"""
Memory read/write utilities.
domain_memory.json — Zettels by research run
gap_log.json       — recurring gaps across runs
eval_history.json  — all evaluation scores
"""

import json
from pathlib import Path
from datetime import datetime


def load_memory(filename: str) -> dict | list:
    path = Path("memory") / filename
    if not path.exists():
        return {} if "memory" in filename else []
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return {} if "memory" in filename else []
    return json.loads(raw)


def save_memory(filename: str, data: dict | list):
    path = Path("memory") / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def update_domain_memory(slug: str, zettels: list):
    """
    Track Zettels per research run.
    zettels: list of {"id": "1a", "title": "Atman", "topic": slug}
    """
    memory = load_memory("domain_memory.json")
    if "zettels" not in memory:
        memory["zettels"] = {}
    if slug not in memory["zettels"]:
        memory["zettels"][slug] = []
    for z in zettels:
        zettel_record = {
            "zettel_id": z.get("id"),
            "title": z.get("title", ""),
            "linked_to": z.get("linked_to", []),
            "created_at": datetime.utcnow().isoformat()
        }
        existing_ids = [x["zettel_id"] for x in memory["zettels"][slug]]
        if z.get("id") not in existing_ids:
            memory["zettels"][slug].append(zettel_record)
    save_memory("domain_memory.json", memory)


def append_gap_log(slug: str, agent: str, gap_text: str):
    gaps = load_memory("gap_log.json")
    if isinstance(gaps, list):
        gaps.append({
            "slug": slug,
            "agent": agent,
            "gap": gap_text[:400],
            "timestamp": datetime.utcnow().isoformat()
        })
        save_memory("gap_log.json", gaps[-100:])


def append_eval_result(result: dict):
    history = load_memory("eval_history.json")
    if isinstance(history, list):
        history.append(result)
        save_memory("eval_history.json", history)


def get_last_eval_results(n: int = 5) -> list:
    history = load_memory("eval_history.json")
    return history[-n:] if isinstance(history, list) else []


def get_zettel_map(slug: str = None) -> dict:
    """Return all Zettels, optionally filtered by slug."""
    memory = load_memory("domain_memory.json")
    zettels = memory.get("zettels", {})
    if slug:
        return zettels.get(slug, [])
    return zettels