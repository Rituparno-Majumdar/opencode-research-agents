"""
Memory read/write utilities.
Called by Opencode after ingest and evaluate pipelines.
"""

import json
from pathlib import Path
from datetime import datetime


def load_memory(filename: str) -> dict | list:
    path = Path("memory") / filename
    if not path.exists():
        return {} if filename.endswith("_memory.json") else []
    raw = path.read_text(encoding="utf-8")
    return json.loads(raw) if raw.strip() else ({} if "memory" in filename else [])


def save_memory(filename: str, data: dict | list):
    path = Path("memory") / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def update_domain_memory(slug: str, notes: list):
    memory = load_memory("domain_memory.json")
    for note in notes:
        note_type = note.get("type", "concepts")
        title = note.get("title", "")
        if not title:
            continue
        if note_type not in memory:
            memory[note_type] = {}
        if title not in memory[note_type]:
            memory[note_type][title] = {"first_seen": slug, "topics": [slug]}
        elif slug not in memory[note_type][title]["topics"]:
            memory[note_type][title]["topics"].append(slug)
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