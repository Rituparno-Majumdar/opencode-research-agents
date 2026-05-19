import os
from dotenv import load_dotenv
load_dotenv('.env')

import sys
import json
import re
sys.path.insert(0, '.')
from utils.minimax_ops import call_sync, load_config
from utils.file_ops import read_research_files
from utils.memory_ops import load_memory

config = load_config()
slug = "how-humans-pursue-death"

files = read_research_files(slug, "./vault")

eval_input = f"""
SLUG: {slug}

RESEARCH FILES (truncated to first 2000 chars each):
{json.dumps({k: v[:2000] for k, v in files.items()}, indent=2)}

Score this run on all 7 metrics. Return ONLY valid JSON.
"""

system = "You are a research evaluator. Score runs on 7 metrics (0-10 each): source_density, language_coverage, gap_rate, cross_tradition_richness, boundary_accuracy, temporal_depth, contradiction_quality. Return ONLY valid JSON."

raw = call_sync(system, eval_input, temperature=0.1, max_tokens=6000)

print("RAW RESPONSE:")
print(raw[:500])
print("---")
json_match = re.search(r'\{[\s\S]*\}', raw)
if json_match:
    try:
        result = json.loads(json_match.group())
        print("Parsed OK")
    except Exception as e:
        print("Parse error:", e)