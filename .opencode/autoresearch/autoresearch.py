"""
OpenCode Autoresearch - Command Reference
==========================================

This module provides commands for the Autoresearch system.
Import this into your workflow to enable autonomous agent improvement.

Author: Rituparno Majumdar
"""

from pathlib import Path
from datetime import datetime
import json

AUTORESEARCH_DIR = Path(".opencode/autoresearch")
SPECIALISTS = ["ceo", "nexus", "flux", "vector", "cipher", "stage", "orbit", "sync", "brief", "prism", "pulse"]


# === COMMANDS FOR AXIOM ===

def status():
    """Show Autoresearch system status for all specialists."""
    print("\n" + "="*50)
    print("AUTORESEARCH SYSTEM STATUS")
    print("="*50)

    results_file = AUTORESEARCH_DIR / "results.tsv"
    if not results_file.exists():
        print("No experiments run yet.")
        return

    lines = results_file.read_text().strip().split("\n")
    # Skip header
    data = [l for l in lines if l and not l.startswith("#")]

    print(f"\nTotal experiments: {len(data)}")

    # Count by specialist
    spec_counts = {}
    for line in data:
        parts = line.split("\t")
        if len(parts) >= 2:
            spec = parts[1]
            spec_counts[spec] = spec_counts.get(spec, 0) + 1

    print("\nBy Specialist:")
    for spec, count in sorted(spec_counts.items()):
        print(f"  {spec}: {count} experiments")

    print()


def run_experiment(specialist: str, change_description: str):
    """
    Run ONE experiment for a specialist.

    Args:
        specialist: Name of specialist (nexus, flux, vector, cipher, etc.)
        change_description: What change is being tested

    The specialist should:
    1. Read their program.md
    2. Make ONE change to their workspace
    3. Test on a task
    4. Report results

    Then log the results using log_result()
    """
    print(f"\n>>> Experiment: {specialist}")
    print(f"    Change: {change_description}")
    print(f"    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Get specialist's current state
    program_path = AUTORESEARCH_DIR / "specialists" / specialist / "program.md"
    if program_path.exists():
        print(f"    Program: {program_path.read_text()[:100]}...")


def log_result(specialist: str, change: str, metric: str, before: float, after: float, outcome: str):
    """Log an experiment result."""
    results_file = AUTORESEARCH_DIR / "results.tsv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    delta = after - before

    line = f"{timestamp}\t{specialist}\t{change}\t{metric}\t{before:.4f}\t{after:.4f}\t{delta:+.4f}\t{outcome}"
    with open(results_file, "a") as f:
        f.write(line + "\n")

    print(f"    Result: {metric} {before:.4f} -> {after:.4f} ({delta:+.4f}) [{outcome}]")


def show_specialist(specialist: str):
    """Show Autoresearch state for one specialist."""
    print(f"\n{'='*40}")
    print(f"SPECIALIST: {specialist.upper()}")
    print(f"{'='*40}")

    # Program
    program_path = AUTORESEARCH_DIR / "specialists" / specialist / "program.md"
    if program_path.exists():
        print("\nProgram:")
        print(program_path.read_text()[:500])

    # Memory
    memory_path = AUTORESEARCH_DIR / "specialists" / specialist / "memory" / "episodic.md"
    if memory_path.exists():
        print("\n\nRecent Memory:")
        print(memory_path.read_text()[:300])


def improve(specialist: str):
    """
    Trigger a specialist to attempt improvement.

    Usage: improve("nexus")
    """
    print(f"\n>>> Triggering Autoresearch for {specialist}")
    show_specialist(specialist)
    print("\n[Ready for specialist to propose improvement]")


def start_overnight():
    """Start overnight autonomous research for all specialists."""
    print("\n" + "*"*50)
    print("STARTING OVERNIGHT AUTORESEARCH")
    print("*"*50)
    print("\nEach specialist will:")
    print("1. Read their program.md for current priorities")
    print("2. Propose and test workspace improvements")
    print("3. Log results to results.tsv")
    print("4. Keep improvements that work, revert those that don't")
    print("\nRunning for 8 hours or until manually stopped...")
    print()

    for spec in SPECIALISTS:
        print(f"--- {spec} cycle ---")
        print("Ready for experiments")


# === QUICK REFERENCE ===

"""
AXIOM'S AUTORESEARCH COMMANDS:

1. Check status:
   status()

2. Run experiment for a specialist:
   run_experiment("nexus", "improved query formulation")
   run_experiment("flux", "better error handling")

3. Log result:
   log_result("nexus", "query_v2", "val_accuracy", 0.85, 0.88, "KEEP")

4. See specialist state:
   show_specialist("nexus")

5. Trigger improvement:
   improve("flux")

6. Start overnight run:
   start_overnight()

FILES YOU CAN MODIFY (by specialists):

nexus/workspace/prompts/
  - query_formulator.md    # How to interpret research queries
  - source_evaluator.md   # How to assess source quality
  - synthesizer.md        # How to combine sources

flux/workspace/prompts/
  - code_generator.md    # How to generate code
  - debugger.md          # How to diagnose errors

vector/workspace/prompts/
  - drafter.md           # How to create drafts
  - style_guide.md       # Writing style rules

cipher/workspace/prompts/
  - pattern_finder.md    # How to find data patterns
  - inferrer.md          # How to draw conclusions
"""

if __name__ == "__main__":
    print(__doc__)
    status()