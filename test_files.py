import sys
sys.path.insert(0, '/Users/pari/Library/Mobile Documents/iCloud~md~obsidian/Documents/my-third-brain')
from utils.file_ops import read_research_files, get_recent_slugs

print("Recent slugs:", get_recent_slugs(3))
print("---")
files = read_research_files("reincarnation")
print("Files found:", list(files.keys()) if files else "None")