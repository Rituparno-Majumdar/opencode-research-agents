"""
File read/write utilities for vault operations.
All paths resolved relative to repo root.
"""

import json
from pathlib import Path
import yaml


def load_config() -> dict:
    return yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))


def load_prompt(name: str) -> str:
    return (Path("agents/prompts") / f"{name}.md").read_text(encoding="utf-8")


def write_vault_file(slug: str, filename: str, content: str,
                     vault_path: str = "./vault") -> Path:
    out = Path(vault_path) / "research" / slug / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out


def write_atomic_note(note_type: str, filename: str, content: str,
                      vault_path: str = "./vault") -> tuple[Path, bool]:
    out = Path(vault_path) / "atomic-notes" / note_type / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        return out, False
    out.write_text(content, encoding="utf-8")
    return out, True


def append_crossref(note_type: str, filename: str, slug: str,
                    vault_path: str = "./vault"):
    out = Path(vault_path) / "atomic-notes" / note_type / filename
    if out.exists():
        existing = out.read_text(encoding="utf-8")
        if slug not in existing:
            with open(out, "a", encoding="utf-8") as f:
                f.write(f"\n\n---\n_Also referenced in: [[research/{slug}/]]_\n")


def read_research_files(slug: str, vault_path: str = "./vault") -> dict:
    research_dir = Path(vault_path) / "research" / slug
    return {
        f.name: f.read_text(encoding="utf-8")
        for f in research_dir.glob("*.md")
    }


def read_source_map(slug: str, vault_path: str = "./vault") -> dict:
    path = Path(vault_path) / "research" / slug / "_source_map.json"
    return json.loads(path.read_text(encoding="utf-8"))


def get_last_slug(vault_path: str = "./vault") -> str | None:
    research_dir = Path(vault_path) / "research"
    if not research_dir.exists():
        return None
    slugs = sorted(
        [d for d in research_dir.iterdir() if d.is_dir()],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    return slugs[0].name if slugs else None


def get_recent_slugs(n: int = 3, vault_path: str = "./vault") -> list[str]:
    research_dir = Path(vault_path) / "research"
    if not research_dir.exists():
        return []
    slugs = sorted(
        [d for d in research_dir.iterdir() if d.is_dir()],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    return [s.name for s in slugs[:n]]