import os
from dotenv import load_dotenv
load_dotenv('.env')

import sys
import re
import json
sys.path.insert(0, '.')
from utils.minimax_ops import call_sync, load_config

config = load_config()

EXTRACTION_SYSTEM = '''
You are an Obsidian atomic note generator. Return ONLY a valid JSON array.
'''

# Read smaller samples
with open('/Users/pari/Library/Mobile Documents/iCloud~md~obsidian/Documents/my-third-brain/vault/research/reincarnation/indic_traditions.md', 'r') as f:
    indic = f.read()[:4000]

raw = call_sync(
    system_prompt=EXTRACTION_SYSTEM,
    user_message=f'RESEARCH SLUG: reincarnation\nExtract 3 concepts from this text:\n\n{indic}',
    temperature=0.2,
    max_tokens=config['max_tokens']['ingest']
)

print('RAW OUTPUT:')
print(raw)
print('---')
print('Length:', len(raw))

# Try different parsing approaches
cleaned = re.sub(r'```json|```', '', raw).strip()
print('CLEANED:', cleaned[:500])