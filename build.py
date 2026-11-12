"""Build both plugins' skills from plugins/skills/ (the only place skills are edited).

  python plugins/build.py          write the generated files
  python plugins/build.py --check  exit 1 if any generated file is missing or differs

Every SKILL.md also gets skills/ANSWERING.md (how to answer a coach) appended, so the house style lives in one
place while each shipped skill stays self-contained.

Claude Code (claude/agents4-coach/skills/): a copy of each skill.
Codex / ChatGPT (openai/agents4-coach/): the same skills, plus what the Codex app shows for them, as in
github.com/openai/plugins:
  - skills/<name>/agents/openai.yaml   display name, short description, starter prompt (SKILL.md `metadata`)
  - skills/<name>/assets/              the plugin's icons, which each skill's yaml points at
  - agents/openai.yaml                 the plugin's own card, from .codex-plugin/plugin.json `interface`
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "skills"
ANSWERING = SOURCE / "ANSWERING.md"
CLAUDE = ROOT / "claude" / "agents4-coach"
OPENAI = ROOT / "openai" / "agents4-coach"
ICON_SMALL, ICON_LARGE = "agents4-fitness-small.svg", "agents4-fitness.png"


def frontmatter(skill_md: str) -> dict:
    """The flat `key: value` and one-level `metadata:` block of a SKILL.md."""
    head = skill_md.split("---\n", 2)[1]
    out, block = {}, None
    for line in head.splitlines():
        if not line.strip():
            continue
        key, _, value = line.strip().partition(":")
        value = value.strip().strip('"')
        if not line.startswith(" "):
            block = key if not value else None
            out[key] = value if value else {}
        elif block:
            out[block][key] = value
    return out


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)  # a JSON string is a valid YAML scalar


def interface_yaml(display, short, prompt, icons=True) -> str:
    lines = ["interface:", f"  display_name: {yaml_quote(display)}", f"  short_description: {yaml_quote(short)}"]
    if icons:
        lines += [f'  icon_small: "./assets/{ICON_SMALL}"', f'  icon_large: "./assets/{ICON_LARGE}"']
    lines.append(f"  default_prompt: {yaml_quote(prompt)}")
    return "\n".join(lines) + "\n"


def expected() -> dict:
    """Every generated file: {path: bytes}."""
    files = {}
    for skill in sorted(p for p in SOURCE.iterdir() if p.is_dir()):
        for src in sorted(p for p in skill.rglob("*") if p.is_file()):
            rel = src.relative_to(SOURCE)
            data = src.read_bytes()
            if src.name == "SKILL.md":
                data = data.rstrip(b"\n") + b"\n\n" + ANSWERING.read_bytes()
            for plugin in (CLAUDE, OPENAI):
                files[plugin / "skills" / rel] = data
        meta = frontmatter((skill / "SKILL.md").read_text(encoding="utf-8")).get("metadata") or {}
        missing = {"display-name", "short-description", "default-prompt"} - set(meta)
        if missing:
            raise SystemExit(f"{skill.name}/SKILL.md metadata lacks {sorted(missing)}")
        files[OPENAI / "skills" / skill.name / "agents" / "openai.yaml"] = interface_yaml(
            meta["display-name"], meta["short-description"], meta["default-prompt"]).encode()
        for icon in (ICON_SMALL, ICON_LARGE):
            files[OPENAI / "skills" / skill.name / "assets" / icon] = (OPENAI / "assets" / icon).read_bytes()
    ui = json.loads((OPENAI / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))["interface"]
    files[OPENAI / "agents" / "openai.yaml"] = interface_yaml(
        ui["displayName"], ui["shortDescription"], ui["defaultPrompt"][0]).encode()
    return files


def stale(files: dict) -> list:
    """Generated-tree files the build would not write (e.g. a deleted skill)."""
    roots = [CLAUDE / "skills", OPENAI / "skills"]
    return [p for r in roots if r.exists() for p in r.rglob("*") if p.is_file() and p not in files]


if __name__ == "__main__":
    files = expected()
    if "--check" in sys.argv:
        drift = [str(p.relative_to(ROOT)) for p, data in files.items() if not p.exists() or p.read_bytes() != data]
        drift += [f"{p.relative_to(ROOT)} (not generated)" for p in stale(files)]
        print("\n".join(drift) if drift else f"build in sync ({len(files)} generated files)")
        sys.exit(1 if drift else 0)
    for p in stale(files):
        p.unlink()
    for p, data in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    print(f"wrote {len(files)} files")
