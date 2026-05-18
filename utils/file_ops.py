"""
File read/write utilities for vault operations.
All paths resolved relative to repo root.
Zettelkasten version — Luhmann sequential IDs per research run.
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
    """Write to vault/research/{slug}/{filename} — used for research pipeline only."""
    out = Path(vault_path) / "research" / slug / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out


def write_zettel(zettel_id: str, content: str, vault_path: str = "./vault") -> tuple[Path, bool]:
    """
    Write a Zettel to vault/zettel/.
    Returns (path, was_new). If Zettel exists, append backlink only.
    """
    out = Path(vault_path) / "zettel" / f"{zettel_id}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        existing = out.read_text(encoding="utf-8")
        if "backlinks" in existing.lower() and "backlinks" not in content.lower():
            return out, False
        if f"← [[{zettel_id}" not in existing:
            with open(out, "a", encoding="utf-8") as f:
                if "## Backlinks" not in existing:
                    f.write("\n\n## Backlinks\n")
                f.write(f"← {content.split('\\n')[0].replace('# ', '')}\n")
        return out, False
    out.write_text(content, encoding="utf-8")
    return out, True


def write_structure_note(slug: str, content: str, vault_path: str = "./vault") -> Path:
    """Write Structure Note to vault/structure/{slug}.md"""
    out = Path(vault_path) / "structure" / f"{slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out


def write_register_entry(slug: str, content: str, vault_path: str = "./vault") -> Path:
    """Write Register Entry to vault/register/{slug}.md"""
    out = Path(vault_path) / "register" / f"{slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out


def append_crossref(zettel_id: str, slug: str, vault_path: str = "./vault"):
    """Legacy function — kept for backward compat during migration."""
    out = Path(vault_path) / "zettel" / f"{zettel_id}.md"
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


def get_existing_zettel_ids(vault_path: str = "./vault") -> set[str]:
    """Return set of all existing Zettel IDs (e.g. {1, 1a, 1a1, 2, 3, ...})"""
    zettel_dir = Path(vault_path) / "zettel"
    if not zettel_dir.exists():
        return set()
    ids = set()
    for f in zettel_dir.glob("*.md"):
        ids.add(f.stem)
    return ids


def read_zettel(zettel_id: str, vault_path: str = "./vault") -> str | None:
    """Read a specific Zettel by ID. Returns None if not found."""
    path = Path(vault_path) / "zettel" / f"{zettel_id}.md"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def list_zettels_by_slug(slug: str, vault_path: str = "./vault") -> list[dict]:
    """
    List all Zettels associated with a research slug.
    Matches by topic field in frontmatter.
    """
    zettel_dir = Path(vault_path) / "zettel"
    if not zettel_dir.exists():
        return []
    results = []
    for f in zettel_dir.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        if f"topic: {slug}" in content or f"topic: {slug.replace('-', ' ')}" in content.lower():
            title = ""
            if content.startswith("# "):
                title = content.split("\n")[0].replace("# ", "")
            results.append({"id": f.stem, "title": title, "path": str(f)})
    return sorted(results, key=lambda x: x["id"])