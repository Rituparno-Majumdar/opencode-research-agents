"""
Research run scoring utilities.
Called by Opencode during evaluate pipeline.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from utils.minimax_ops import call_sync, load_config
from utils.file_ops import load_prompt, read_research_files, get_recent_slugs
from utils.memory_ops import load_memory, append_gap_log, append_eval_result


def try_parse_json(text: str) -> dict | None:
    """Try to parse JSON, return None if fails."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None


def normalize_eval_result(result: dict, slug: str) -> dict:
    """Normalize evaluation result to required format."""
    # Check if already in correct format
    if "total_score" in result and "scores" in result:
        # Has nested scores format - verify it has weakest_agent
        if "weakest_agent" not in result:
            scores = result.get("scores", {})
            if scores:
                result["weakest_agent"] = min(scores.keys(), key=lambda k: scores[k].get("score", 10))
                result["weakest_metric"] = result["weakest_agent"]
                result["improvement_priority"] = result["weakest_agent"]
        return result
    
    # Flat format like {"source_density": 5, "language_coverage": 6, ...}
    metrics = ["source_density", "language_coverage", "gap_rate", "cross_tradition_richness", 
               "boundary_accuracy", "temporal_depth", "contradiction_quality"]
    
    scores = {}
    for m in metrics:
        if m in result:
            scores[m] = {"score": result[m], "justification": ""}
    
    # Calculate total
    total = sum(v.get("score", 0) for v in scores.values())
    
    # Find weakest
    weakest = min(scores.keys(), key=lambda k: scores[k]["score"]) if scores else "unknown"
    
    return {
        "run_id": f"{slug}_run_1",
        "topic": slug,
        "scores": scores,
        "total_score": total,
        "weakest_agent": weakest,
        "weakest_metric": weakest,
        "improvement_priority": weakest
    }


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
    config = load_config()
    system = load_prompt("evaluator")
    raw = call_sync(system, eval_input, temperature=0.1, max_tokens=config["max_tokens"]["evaluate"])

    # Robust JSON extraction - try multiple patterns
    result = None
    result = try_parse_json(raw)
    if result is None:
        # Try extracting just the JSON portion
        json_match = re.search(r'\{[\s\S]*\}', raw)
        if json_match:
            result = try_parse_json(json_match.group())
    
    if result is None:
        raise ValueError("Could not parse evaluation JSON")

    # Normalize to required format
    result = normalize_eval_result(result, slug)

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