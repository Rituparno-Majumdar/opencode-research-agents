"""
Research run scoring utilities.
Scores on 7 metrics including quote_quality.
"""

import json
import re
from pathlib import Path
from utils.openrouter_ops import call_sync
from utils.file_ops import load_prompt, read_research_files, get_recent_slugs
from utils.memory_ops import load_memory, append_gap_log, append_eval_result


def score_run(slug: str, vault_path: str = "./vault") -> dict:
    files = read_research_files(slug, vault_path)
    if not files:
        raise FileNotFoundError("No research files found for: " + slug)

    gap_log = load_memory("gap_log.json")
    domain_memory = load_memory("domain_memory.json")

    files_preview = {}
    for k, v in files.items():
        files_preview[k] = v[:3000]

    gap_data = gap_log[-20:] if isinstance(gap_log, list) else []
    domain_data = {k: len(v) for k, v in domain_memory.items()} if isinstance(domain_memory, dict) else {}

    eval_input = """
SLUG: %s

RESEARCH FILES (first 3000 chars each):
%s

GAP LOG (last 20):
%s

DOMAIN MEMORY:
%s

Score on all 7 metrics including quote_quality. Return JSON only.
""" % (
        slug,
        json.dumps(files_preview, indent=2),
        json.dumps(gap_data, indent=2),
        json.dumps(domain_data, indent=2),
    )

    system = load_prompt("evaluator")
    raw = call_sync(system, eval_input, temperature=0.1, max_tokens=3000)

    json_match = re.search(r'\{[\s\S]*\}', raw)
    if not json_match:
        raise ValueError("Could not parse evaluation JSON")

    result = json.loads(json_match.group())
    if "total_score" not in result:
        scores = result.get("scores", {})
        result["total_score"] = sum(v.get("score", 0) for v in scores.values())

    for fname, content in files.items():
        if "Gaps & Honest Limitations" in content:
            gap_text = content.split("Gaps & Honest Limitations")[-1][:400].strip()
            if len(gap_text) > 30:
                append_gap_log(slug, fname.replace(".md", ""), gap_text)

    append_eval_result(result)
    return result


def score_recent_runs(n: int = 3, vault_path: str = "./vault") -> list[dict]:
    results = []
    for slug in get_recent_slugs(n, vault_path):
        try:
            results.append(score_run(slug, vault_path))
        except Exception as e:
            print("  Warning: Could not score " + slug + ": " + str(e))
    return results


def format_score_table(result: dict) -> str:
    scores = result.get("scores", {})
    sep = "=" * 42
    dash = "-" * 42
    topic = result.get("topic", result.get("run_id", "?"))
    lines = [
        sep,
        "EVALUATION: " + topic,
        dash,
    ]
    labels = {
        "source_density":           "Source Density     ",
        "language_coverage":        "Language Coverage  ",
        "quote_quality":            "Quote Quality      ",
        "cross_tradition_richness": "Cross-Tradition    ",
        "boundary_accuracy":        "Boundary Accuracy  ",
        "temporal_depth":           "Temporal Depth     ",
        "contradiction_quality":    "Contradiction Qual ",
    }
    for key, label in labels.items():
        if key in scores:
            s = scores[key].get("score", 0)
            bar = chr(9608) * s + chr(9617) * (10 - s)
            lines.append("  " + label + " " + bar + " " + str(s) + "/10")
    lines.append(dash)
    lines.append("  TOTAL               " + str(result.get("total_score", 0)) + "/70")
    lines.append("  Weakest Agent:      " + str(result.get("weakest_agent", "N/A")))
    lines.append("  Priority:           " + str(result.get("improvement_priority", "N/A")))
    lines.append(sep + "\n")
    return "\n".join(lines)