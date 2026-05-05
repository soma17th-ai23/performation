#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_SKILLS = (
  "performation-orchestrator",
  "performation-venue-data",
  "performation-source-research",
  "performation-trust-review",
  "performation-demo-qa",
)
REQUIRED_FILES = (
  "AGENTS.md",
  "README.md",
  "docs/project-brief.md",
  "docs/harness/performation/team-spec.md",
  "docs/harness/performation/output-contract.md",
  "docs/harness/performation/scenario-matrix.md",
  "docs/harness/performation/git-policy.md",
  ".agents/skills/harness/SKILL.md",
  ".codex/skills/harness/SKILL.md",
  ".claude/agents/performation-supervisor.md",
  ".claude/agents/performation-source-researcher.md",
  ".claude/agents/performation-trust-reviewer.md",
)


def fail(message: str) -> None:
  print(f"FAIL: {message}")
  raise SystemExit(1)


def read(path: Path) -> str:
  return path.read_text(encoding="utf-8")


def assert_file(relative: str) -> Path:
  path = ROOT / relative
  if not path.exists():
    fail(f"missing required file: {relative}")
  if not path.is_file():
    fail(f"required path is not a file: {relative}")
  return path


def assert_skill_frontmatter(relative: str) -> None:
  path = assert_file(relative)
  content = read(path).lstrip("\ufeff")
  normalized = content.replace("\r\n", "\n").replace("\r", "\n")
  if not normalized.startswith("---\n"):
    fail(f"missing YAML frontmatter: {relative}")
  try:
    _, frontmatter, _ = normalized.split("---", 2)
  except ValueError:
    fail(f"malformed YAML frontmatter: {relative}")
  if "name:" not in frontmatter:
    fail(f"frontmatter missing name: {relative}")
  if "description:" not in frontmatter:
    fail(f"frontmatter missing description: {relative}")


def assert_mentions(path: Path, required_terms: tuple[str, ...]) -> None:
  content = read(path)
  for term in required_terms:
    if term not in content:
      fail(f"{path.relative_to(ROOT)} does not mention required term: {term}")


def main() -> int:
  for relative in REQUIRED_FILES:
    assert_file(relative)

  for skill in PROJECT_SKILLS:
    assert_skill_frontmatter(f".agents/skills/{skill}/SKILL.md")
    codex_path = ROOT / ".codex" / "skills" / skill
    if not codex_path.exists():
      fail(f"missing Codex skill mirror: .codex/skills/{skill}")
    assert_skill_frontmatter(f".codex/skills/{skill}/SKILL.md")

  team_spec = assert_file("docs/harness/performation/team-spec.md")
  assert_mentions(
    team_spec,
    (
      "Supervisor",
      "Producer-Reviewer",
      "official_confirmed",
      "public_review_reference",
      "latest_official_check_required",
      "uncertain",
    ),
  )

  brief = assert_file("docs/project-brief.md")
  assert_mentions(
    brief,
    (
      "KSPO DOME",
      "Blue Square",
      "YES24 Live Hall",
      "FastAPI",
      "Gradio",
      "LangGraph",
    ),
  )

  git_policy = assert_file("docs/harness/performation/git-policy.md")
  assert_mentions(
    git_policy,
    (
      "feat",
      "fix",
      "test",
      "docs",
      "chore",
      "python3 scripts/validate_harness.py",
      "<type>: <한글 요약>",
    ),
  )

  print("PASS: Performation harness structure is valid.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
