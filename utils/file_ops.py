"""
File read/write utilities for vault operations.
All paths resolved relative to repo root.
Zettelkasten version — Luhmann sequential IDs per research run.
Python 3.11 compatible — no f-strings with complex expressions.
"""

import json
from pathlib import Path
import yaml


def load_config() -> dict:
    return yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))


def load_prompt(name: str) -> str:
    return (Path("agents/prompts") / (name + ".md")).read_text(encoding="utf-8")


def write_vault_file(slug: str, filename: str, content: str,
                     vault_path: str = "./vault") -> Path:
    out = Path(vault_path) / "research" / slug / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out


def write_zettel(zettel_id: str, content: str, vault_path: str = "./vault") -> tuple:
    out = Path(vault_path) / "zettel" / (zettel_id + ".md")
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        existing = out.read_text(encoding="utf-8")
        if "## Backlinks" not in existing:
            with open(out, "a", encoding="utf-8") as fh:
                fh.write("\n\n## Backlinks\n")
            existing = out.read_text(encoding="utf-8")
        if ("<- [[") not in existing and ("Backlinks" in existing):
            first_line = content.split("\n")[0].replace("# ", "")
            with open(out, "a", encoding="utf-8") as fh:
                fh.write("<- " + first_line + "\n")
        return out, False
    out.write_text(content, encoding="utf-8")
    return out, True


def write_structure_note(slug: str, content: str, vault_path: str = "./vault") -> Path:
    out = Path(vault_path) / "structure" / (slug + ".md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out


def write_register_entry(slug: str, content: str, vault_path: str = "./vault") -> Path:
    out = Path(vault_path) / "register" / (slug + ".md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out


def read_research_files(slug: str, vault_path: str = "./vault") -> dict:
    research_dir = Path(vault_path) / "research" / slug
    if not research_dir.exists():
        return {}
    return {
        f.name: f.read_text(encoding="utf-8")
        for f in research_dir.glob("*.md")
    }


def read_source_map(slug: str, vault_path: str = "./vault") -> dict:
    path = Path(vault_path) / "research" / slug / "_source_map.json"
    return json.loads(path.read_text(encoding="utf-8"))


def get_last_slug(vault_path: str = "./vault") -> str:
    research_dir = Path(vault_path) / "research"
    if not research_dir.exists():
        return None
    slugs = sorted(
        [d for d in research_dir.iterdir() if d.is_dir()],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    return slugs[0].name if slugs else None


def get_recent_slugs(n: int = 3, vault_path: str = "./vault") -> list:
    research_dir = Path(vault_path) / "research"
    if not research_dir.exists():
        return []
    slugs = sorted(
        [d for d in research_dir.iterdir() if d.is_dir()],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    return [s.name for s in slugs[:n]]


def get_existing_zettel_ids(vault_path: str = "./vault") -> set:
    zettel_dir = Path(vault_path) / "zettel"
    if not zettel_dir.exists():
        return set()
    return {f.stem for f in zettel_dir.glob("*.md")}


def read_zettel(zettel_id: str, vault_path: str = "./vault") -> str:
    path = Path(vault_path) / "zettel" / (zettel_id + ".md")
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def list_zettels_by_slug(slug: str, vault_path: str = "./vault") -> list:
    zettel_dir = Path(vault_path) / "zettel"
    if not zettel_dir.exists():
        return []
    results = []
    for f in zettel_dir.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        if ("topic: " + slug) in content or ("topic: " + slug.replace("-", " ")) in content.lower():
            title = content.split("\n")[0].replace("# ", "") if content.startswith("# ") else ""
            results.append({"id": f.stem, "title": title, "path": str(f)})
    return sorted(results, key=lambda x: x["id"])