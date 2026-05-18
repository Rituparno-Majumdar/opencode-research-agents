"""
Git operations and improvement proposal utilities.
Supports both GitHub PR mode (GitHub Actions) and local pending file mode (cron).
Auto-detects which mode based on GITHUB_TOKEN and GITHUB_REPO env vars.
"""

import os
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
import requests
from utils.openrouter_ops import call_sync
from utils.file_ops import load_prompt
from utils.memory_ops import load_memory, get_last_eval_results


AGENT_FILE_MAP = {
    "indic_traditions":         "agent_a_indic",
    "western_philosophy":       "agent_b_western",
    "ancient_civilizations":    "agent_c_civilizations",
    "contemporary_scholarship": "agent_d_contemporary"
}


def git(cmd: list[str]):
    subprocess.run(cmd, check=True)


def git_commit_push(message: str, paths: list = None):
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
    src = Path("agents/prompts") / (agent_file + ".md")
    dst = Path("memory/prompt_versions") / (timestamp + "_" + agent_file + ".md")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return dst


def create_github_pr(branch: str, title: str, body: str) -> str:
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPO", "")
    if not token or not repo:
        return ""
    resp = requests.post(
        "https://api.github.com/repos/" + repo + "/pulls",
        headers={
            "Authorization": "token " + token,
            "Accept": "application/vnd.github.v3+json"
        },
        json={"title": title, "body": body, "head": branch, "base": "main"}
    )
    if resp.status_code == 201:
        return resp.json()["html_url"]
    return ""


def write_pending_file(timestamp: str, weakest_agent: str,
                       branch: str, improvement: dict) -> Path:
    pending_dir = Path("logs/pending_improvements")
    pending_dir.mkdir(parents=True, exist_ok=True)
    path = pending_dir / (timestamp + "_" + weakest_agent + ".md")
    score_before = improvement.get("score_before", "?")
    change_desc = improvement.get("change_description", "improvement")
    diff_info = improvement.get("diff", {})
    evidence = improvement.get("evidence", [])
    evidence_lines = "\n".join("- " + e for e in evidence)
    path.write_text(
        "# Pending Improvement: " + weakest_agent + "\n"
        "Generated: " + timestamp + "\n"
        "Branch: " + branch + "\n\n"
        "## What Changed\n"
        + change_desc + "\n\n"
        "## Metric Improved\n"
        + str(improvement.get("metric_being_improved", "N/A"))
        + " — was " + str(score_before) + "/10\n\n"
        "## Evidence\n"
        + evidence_lines + "\n\n"
        "## Diff\n"
        "Section: " + str(diff_info.get("section", "N/A")) + "\n"
        "Added: " + str(diff_info.get("added", "N/A")) + "\n"
        "Removed: " + str(diff_info.get("removed", "None")) + "\n\n"
        "## To Apply\n"
        "git merge " + branch + "\n\n"
        "## To Reject\n"
        "git branch -D " + branch + "\n",
        encoding="utf-8"
    )
    return path


def run_improve() -> dict:
    last_5 = get_last_eval_results(5)
    if len(last_5) < 2:
        return {"error": "Need at least 2 evaluation runs. Run more research first."}

    gap_log = load_memory("gap_log.json")

    agent_scores = {}
    for run in last_5:
        wa = run.get("weakest_agent", "")
        if wa:
            agent_scores[wa] = agent_scores.get(wa, 0) + 1
    if not agent_scores:
        return {"error": "Could not determine weakest agent from history"}

    weakest_agent = max(agent_scores, key=agent_scores.get)
    prompt_file = AGENT_FILE_MAP.get(weakest_agent, weakest_agent)
    current_prompt = load_prompt(prompt_file)

    gap_data = gap_log[-20:] if isinstance(gap_log, list) else []
    improve_input = (
        "LAST 5 EVALUATION REPORTS:\n"
        + json.dumps(last_5, indent=2)
        + "\n\nRECURRING GAPS (last 20):\n"
        + json.dumps(gap_data, indent=2)
        + "\n\nCURRENT PROMPT FOR " + weakest_agent + ":\n"
        + current_prompt
        + "\n\nProduce a targeted improvement. Return JSON only."
    )
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
    branch = "improve/" + weakest_agent + "_" + timestamp
    score_before = improvement.get("score_before", "?")
    change_desc = improvement.get("change_description", "targeted improvement")
    commit_msg = "improve(" + weakest_agent + "): " + change_desc + " [score was " + str(score_before) + "/10]"

    git(["git", "checkout", "-b", branch])
    prompt_path = Path("agents/prompts/" + prompt_file + ".md")
    prompt_path.write_text(updated_prompt, encoding="utf-8")
    git_commit_push(commit_msg, ["agents/prompts/" + prompt_file + ".md", "memory/"])
    git(["git", "push", "origin", branch])
    git(["git", "checkout", "main"])

    improvement["branch"] = branch

    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPO", "")
    if token and repo:
        evidence_lines = "\n".join("- " + e for e in improvement.get("evidence", []))
        diff_info = improvement.get("diff", {})
        pr_title = "[Auto-Improve] " + weakest_agent + ": " + change_desc
        pr_body = (
            "## Automated Prompt Improvement\n\n"
            "**Agent:** " + weakest_agent + "\n"
            "**Metric Improved:** " + str(improvement.get("metric_being_improved", "N/A")) + "\n"
            "**Score Before:** " + str(score_before) + "/10\n"
            "**Change Type:** " + str(improvement.get("change_type", "N/A")) + "\n\n"
            "### What Changed\n"
            + change_desc + "\n\n"
            "### Evidence\n"
            + evidence_lines + "\n\n"
            "### Diff\n"
            "**Section:** " + str(diff_info.get("section", "N/A")) + "\n"
            "**Added:** " + str(diff_info.get("added", "N/A")) + "\n"
            "**Removed:** " + str(diff_info.get("removed", "None")) + "\n\n"
            "---\n"
            "_DO NOT merge without reading the diff carefully._\n"
            "_If this improvement looks wrong: close PR, run `git branch -D " + branch + "`_\n"
        )
        pr_url = create_github_pr(branch, pr_title, pr_body)
        if pr_url:
            improvement["pr_url"] = pr_url
            return improvement

    pending_path = write_pending_file(timestamp, weakest_agent, branch, improvement)
    improvement["pending_file"] = str(pending_path)
    return improvement