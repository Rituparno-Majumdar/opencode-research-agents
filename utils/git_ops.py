"""
Git and GitHub PR utilities.
Called by Opencode during improve pipeline.
"""

import os
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
import requests
from utils.minimax_ops import call_sync
from utils.file_ops import load_prompt
from utils.memory_ops import load_memory, get_last_eval_results


AGENT_FILE_MAP = {
    "indic_traditions": "agent_a_indic",
    "western_philosophy": "agent_b_western",
    "Western": "agent_b_western",
    "ancient_civilizations": "agent_c_civilizations",
    "Ancient": "agent_c_civilizations",
    "contemporary_scholarship": "agent_d_contemporary",
    "Contemporary": "agent_d_contemporary",
    "Indic": "agent_a_indic"
}


def git(cmd: str):
    subprocess.run(cmd.split(), check=True)


def git_commit_push(message: str, paths: list[str] = None):
    subprocess.run(["git", "config", "user.name", "research-bot"], check=True)
    subprocess.run(["git", "config", "user.email", "bot@research-system"], check=True)
    if paths:
        for p in paths:
            subprocess.run(["git", "add", p], check=True)
    else:
        subprocess.run(["git", "add", "-A"], check=True)
    result = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if result.returncode != 0:
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push"], check=True)


def snapshot_prompt(agent_file: str) -> Path:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    src = Path("agents/prompts") / f"{agent_file}.md"
    dst = Path("memory/prompt_versions") / f"{timestamp}_{agent_file}.md"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return dst


def create_pr(branch: str, title: str, body: str) -> str:
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPO", "")
    if not token or not repo:
        return "PR not created — GITHUB_TOKEN or GITHUB_REPO not set"
    resp = requests.post(
        f"https://api.github.com/repos/{repo}/pulls",
        headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"},
        json={"title": title, "body": body, "head": branch, "base": "main"}
    )
    if resp.status_code == 201:
        return resp.json()["html_url"]
    return f"PR failed: {resp.status_code} {resp.text[:200]}"


def run_improve() -> dict:
    last_5 = get_last_eval_results(5)
    if len(last_5) < 2:
        return {"error": "Need at least 2 evaluation runs. Run more research first."}

    gap_log = load_memory("gap_log.json")

    agent_scores: dict[str, int] = {}
    for run in last_5:
        wa = run.get("weakest_agent", "")
        if wa:
            agent_scores[wa] = agent_scores.get(wa, 0) + 1
    if not agent_scores:
        return {"error": "Could not determine weakest agent from history"}

    weakest_agent = max(agent_scores, key=agent_scores.get)
    prompt_file = AGENT_FILE_MAP.get(weakest_agent, weakest_agent)
    current_prompt = load_prompt(prompt_file)

    improve_input = f"""
LAST 5 EVALUATION REPORTS:
{json.dumps(last_5, indent=2)}

RECURRING GAPS (last 20):
{json.dumps(gap_log[-20:] if isinstance(gap_log, list) else [], indent=2)}

CURRENT PROMPT FOR {weakest_agent}:
{current_prompt}

Produce a targeted improvement. Return JSON only.
"""
    system = load_prompt("prompt_updater")
    raw = call_sync(system, improve_input, temperature=0.3, max_tokens=6000)
    json_match = re.search(r'\{[\s\S]*\}', raw)
    if not json_match:
        return {"error": "Could not parse improvement JSON"}

    improvement = json.loads(json_match.group())
    updated_prompt = improvement.get("updated_prompt", "")
    if not updated_prompt:
        return {"error": "No updated prompt in response"}

    snapshot_prompt(prompt_file)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    branch = f"improve/{weakest_agent}_{timestamp}"
    git(f"git checkout -b {branch}")
    Path(f"agents/prompts/{prompt_file}.md").write_text(updated_prompt, encoding="utf-8")

    score_before = improvement.get("score_before", "?")
    change_desc = improvement.get("change_description", "Targeted improvement")
    git_commit_push(
        f"improve({weakest_agent}): {change_desc} [score was {score_before}/10]",
        [f"agents/prompts/{prompt_file}.md", "memory/"]
    )
    git("git push origin " + branch)
    git("git checkout main")

    pr_body = f"""## Automated Prompt Improvement

**Agent:** {weakest_agent}
**Metric Improved:** {improvement.get('metric_being_improved', 'N/A')}
**Score Before:** {score_before}/10
**Change Type:** {improvement.get('change_type', 'N/A')}

### What Changed
{change_desc}

### Evidence
{chr(10).join(f'- {e}' for e in improvement.get('evidence', []))}

### Diff
**Section:** {improvement.get('diff', {}).get('section', 'N/A')}
**Added:** {improvement.get('diff', {}).get('added', 'N/A')}
**Removed:** {improvement.get('diff', {}).get('removed', 'None')}

---
_DO NOT merge without reading the diff carefully._
"""
    pr_url = create_pr(branch, f"[Auto-Improve] {weakest_agent}: {change_desc}", pr_body)
    improvement["pr_url"] = pr_url
    improvement["branch"] = branch
    return improvement