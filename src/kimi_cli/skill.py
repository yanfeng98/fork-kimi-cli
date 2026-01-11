from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from loguru import logger
from pydantic import BaseModel, ConfigDict

from kimi_cli.share import get_share_dir
from kimi_cli.utils.frontmatter import read_frontmatter


def get_skills_dir() -> Path:
    return get_share_dir() / "skills"


def get_claude_skills_dir() -> Path:
    return Path.home() / ".claude" / "skills"


def normalize_skill_name(name: str) -> str:
    return name.casefold()


def index_skills(skills: Iterable[Skill]) -> dict[str, Skill]:
    return {normalize_skill_name(skill.name): skill for skill in skills}


def read_skill_text(skill: Skill) -> str | None:
    try:
        return skill.skill_md_file.read_text(encoding="utf-8").strip()
    except OSError as exc:
        logger.warning(
            "Failed to read skill file {path}: {error}",
            path=skill.skill_md_file,
            error=exc,
        )
        return None


class Skill(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    description: str
    dir: Path

    @property
    def skill_md_file(self) -> Path:
        return self.dir / "SKILL.md"


def discover_skills(skills_dir: Path) -> list[Skill]:
    if not skills_dir.is_dir():
        return []

    skills: list[Skill] = []

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue

        try:
            skills.append(parse_skill_md(skill_md))
        except Exception as e:
            logger.info("Skipping invalid skill at {}: {}", skill_md, e)
            continue

    return sorted(skills, key=lambda s: s.name)


def parse_skill_md(skill_md_file: Path) -> Skill:
    frontmatter = read_frontmatter(skill_md_file) or {}

    if "name" not in frontmatter:
        frontmatter["name"] = skill_md_file.parent.name
    if "description" not in frontmatter:
        frontmatter["description"] = "No description provided."

    return Skill.model_validate(
        {
            **frontmatter,
            "dir": skill_md_file.parent.absolute(),
        }
    )
