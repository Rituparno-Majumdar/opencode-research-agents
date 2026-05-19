import os
from dotenv import load_dotenv
load_dotenv('.env')

import sys
import json
sys.path.insert(0, '.')
from utils.minimax_ops import call_sync, load_config
from utils.file_ops import read_research_files
from utils.memory_ops import load_memory

config = load_config()
slug = "reincarnation"

files = read_research_files(slug, "./vault")
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

system = "You are a research evaluator. Score runs on 7 metrics (0-10 each): source_density, language_coverage, gap_rate, cross_tradition_richness, boundary_accuracy, temporal_depth, contradiction_quality. Return ONLY valid JSON with: run_id, topic, scores (dict with each metric having score and notes), total_score, weakest_agent, improvement_priority."

raw = call_sync(system, eval_input, temperature=0.1, max_tokens=3000)

print("RAW RESPONSE:")
print(raw)
print("---")
print("Length:", len(raw))