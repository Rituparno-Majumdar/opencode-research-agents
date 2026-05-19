"""
Research run scoring utilities.
Called by Opencode during evaluate pipeline.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from utils.minimax_ops import call_sync
from utils.file_ops import load_prompt, read_research_files, get_recent_slugs
from utils.memory_ops import load_memory, append_gap_log, append_eval_result


def score_run(slug: str, vault_path: str = "./vault") -> dict:
    files = read_research_files(slug, vault_path)
    if not files:
        raise FileNotFoundError(f"No research files found for slug: {slug}")

    gap_log = load_memory("gap_log.json")
    domain_memory = load_memory("domain_memory.json")

    eval_input = f"""
SLUG: {slug}

RESEARCH FILES (truncated to first 3000 chars each for evaluation):
{json.dumps({k: v[:3000] for k, v in files.items()}, indent=2)}

GAP LOG (last 20 entries):
{json.dumps(gap_log[-20:] if isinstance(gap_log, list) else [], indent=2)}

DOMAIN MEMORY SUMMARY:
{json.dumps({k: len(v) if hasattr(v, '__len__') else v for k, v in domain_memory.items()} if isinstance(domain_memory, dict) else {}, indent=2)}

Score this run on all 7 metrics. Return valid JSON only.
"""
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
    slugs = get_recent_slugs(n, vault_path)
    results = []
    for slug in slugs:
        try:
            result = score_run(slug, vault_path)
            results.append(result)
        except Exception as e:
            print(f"  ⚠ Could not score {slug}: {e}")
    return results


def format_score_table(result: dict) -> str:
    scores = result.get("scores", {})
    lines = [
        f"\n{'═'*40}",
        f"EVALUATION: {result.get('topic', result.get('run_id', 'unknown'))}",
        f"{'─'*40}"
    ]
    metric_labels = {
        "source_density": "Source Density    ",
        "language_coverage": "Language Coverage ",
        "gap_rate": "Gap Rate          ",
        "cross_tradition_richness": "Cross-Tradition   ",
        "boundary_accuracy": "Boundary Accuracy ",
        "temporal_depth": "Temporal Depth    ",
        "contradiction_quality": "Contradiction Qual"
    }
    for key, label in metric_labels.items():
        if key in scores:
            score = scores[key].get("score", 0)
            bar = "█" * score + "░" * (10 - score)
            lines.append(f"  {label} {bar} {score}/10")
    lines.append(f"{'─'*40}")
    lines.append(f"  TOTAL              {result.get('total_score', 0)}/70")
    lines.append(f"  Weakest Agent:     {result.get('weakest_agent', 'N/A')}")
    lines.append(f"  Priority:          {result.get('improvement_priority', 'N/A')}")
    lines.append(f"{'═'*40}\n")
    return "\n".join(lines)