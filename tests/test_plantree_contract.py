from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANTREE = ROOT / "docs" / "plantree"
PLANS = PLANTREE / "plans"

PLAN_DIR_RE = re.compile(r"^(?P<number>\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*$")
PLAN_ID_RE = re.compile(r"^Plan ID:\s*(P\d{3})\s*$", re.MULTILINE)
STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$", re.MULTILINE)
MODULES_RE = re.compile(r"^Affected Modules:\s*(.*?)\s*$", re.MULTILINE)
TASK_TOKEN_RE = re.compile(r"\bT\d+\b")
TASK_ID_RE = re.compile(r"\bT\d{3}\b")
DECISION_ID_RE = re.compile(r"^Decision ID:\s*(P\d{3})-D(\d{3})\s*$", re.MULTILINE)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def backtick_values(value: str) -> set[str]:
    return set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)*)`", value))


def without_fenced_code(content: str) -> str:
    visible: list[str] = []
    in_fence = False
    for line in content.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            visible.append(line)
    return "\n".join(visible)


def plan_registry() -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    for line in read(PLANTREE / "README.md").splitlines():
        if not re.match(r"^\| P\d{3} \|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 7:
            raise AssertionError(f"malformed Plan registry row: {line}")
        plan_id, plan_cell, modules, status, phase, landed, target = cells
        link = re.search(r"\[[^\]]+\]\(([^)]+)\)", plan_cell)
        if link is None:
            raise AssertionError(f"Plan registry entry has no link: {line}")
        rows[plan_id] = {
            "path": (PLANTREE / link.group(1)).resolve(),
            "modules": backtick_values(modules),
            "status": status,
            "phase": phase,
            "landed": landed,
            "target": target,
        }
    return rows


class PlanTreeContractTests(unittest.TestCase):
    def test_release_version_surfaces_are_synchronized(self) -> None:
        version = read(ROOT / "VERSION").strip()
        package = json.loads(read(ROOT / "package.json"))
        surfaces = {
            "package.json": package["version"],
            "pyproject.toml": re.search(r'^version = "([^"]+)"$', read(ROOT / "pyproject.toml"), re.MULTILINE).group(1),
            "package __init__": re.search(
                r'^__version__ = "([^"]+)"$',
                read(ROOT / "src" / "plan_tree_installer" / "__init__.py"),
                re.MULTILINE,
            ).group(1),
            "Python CLI": re.search(
                r'^PACKAGE_VERSION = "([^"]+)"$',
                read(ROOT / "src" / "plan_tree_installer" / "cli.py"),
                re.MULTILINE,
            ).group(1),
            "Node CLI": re.search(
                r'^const PACKAGE_VERSION = "([^"]+)";$',
                read(ROOT / "bin" / "plan-tree.js"),
                re.MULTILINE,
            ).group(1),
        }
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        self.assertEqual({version}, set(surfaces.values()), f"version drift: {surfaces}")

    def test_release_workflow_stages_github_before_registries(self) -> None:
        workflow = read(ROOT / ".github" / "workflows" / "release.yml")

        def needs(job: str) -> str:
            match = re.search(
                rf"(?ms)^  {re.escape(job)}:\n(?P<body>.*?)(?=^  [a-z][a-z0-9-]*:\n|\Z)",
                workflow,
            )
            self.assertIsNotNone(match, f"missing release job: {job}")
            dependency = re.search(r"(?m)^    needs:\s*(\S+)\s*$", match.group("body"))
            self.assertIsNotNone(dependency, f"missing release dependency: {job}")
            return dependency.group(1)

        self.assertEqual("validate", needs("github-release"))
        self.assertEqual("github-release", needs("npm"))
        self.assertEqual("npm", needs("pypi"))
        self.assertIn("GitHub Release already exists and contains bilingual notes.", workflow)

    def test_plan_directories_are_flat_numbered_and_registered(self) -> None:
        registry = plan_registry()
        seen: dict[str, Path] = {}

        for plan_dir in sorted(path for path in PLANS.iterdir() if path.is_dir()):
            match = PLAN_DIR_RE.fullmatch(plan_dir.name)
            self.assertIsNotNone(match, f"unexpected non-numbered Plan directory: {plan_dir}")
            plan_id = f"P{match.group('number')}"
            self.assertNotIn(plan_id, seen, f"duplicate Plan ID {plan_id}")
            seen[plan_id] = plan_dir

            plan_readme = plan_dir / "README.md"
            self.assertTrue(plan_readme.is_file(), f"missing Plan README: {plan_readme}")
            metadata = PLAN_ID_RE.search(read(plan_readme))
            self.assertIsNotNone(metadata, f"missing Plan ID metadata: {plan_readme}")
            self.assertEqual(plan_id, metadata.group(1), f"directory/metadata mismatch: {plan_dir}")

        self.assertEqual(set(seen), set(registry), "root registry and Plan directories differ")
        for plan_id, plan_dir in seen.items():
            self.assertEqual(
                (plan_dir / "README.md").resolve(),
                registry[plan_id]["path"],
                f"registry path mismatch for {plan_id}",
            )

    def test_plan_status_and_modules_match_registry(self) -> None:
        allowed_modules = {
            match.group(1)
            for line in read(PLANTREE / "baseline" / "module-map.md").splitlines()
            if (match := re.match(r"^\| `([^`]+)` \|", line))
        }
        self.assertTrue(allowed_modules, "baseline module map defines no module keys")

        for plan_id, row in plan_registry().items():
            plan_readme = Path(row["path"])
            content = read(plan_readme)
            modules = MODULES_RE.search(content)
            status = STATUS_RE.search(content)
            self.assertIsNotNone(modules, f"missing Affected Modules: {plan_readme}")
            self.assertIsNotNone(status, f"missing Status: {plan_readme}")
            declared = backtick_values(modules.group(1))
            self.assertEqual(declared, row["modules"], f"registry module drift for {plan_id}")
            self.assertEqual(status.group(1), row["status"], f"registry status drift for {plan_id}")
            self.assertFalse(declared - allowed_modules, f"unknown module keys for {plan_id}")

    def test_optional_task_ids_are_roadmap_owned_and_unique(self) -> None:
        active_task_registries = list(PLANS.glob("*/indexes/task-registry.md"))
        self.assertEqual([], active_task_registries, "roadmap tasks have a competing active registry")

        for roadmap in PLANS.glob("*/roadmap.md"):
            content = read(roadmap)
            tokens = TASK_TOKEN_RE.findall(content)
            self.assertTrue(tokens, f"maintained example roadmap has no task IDs: {roadmap}")
            self.assertTrue(all(TASK_ID_RE.fullmatch(token) for token in tokens), f"malformed task ID: {roadmap}")
            self.assertEqual(len(tokens), len(set(tokens)), f"duplicate task ID: {roadmap}")

    def test_decision_ids_match_plan_and_filename(self) -> None:
        for plan_dir in sorted(path for path in PLANS.iterdir() if path.is_dir()):
            plan_id = f"P{plan_dir.name[:3]}"
            for decision in (plan_dir / "decisions").glob("*.md"):
                match = re.fullmatch(r"(\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md", decision.name)
                self.assertIsNotNone(match, f"malformed decision filename: {decision}")
                metadata = DECISION_ID_RE.search(read(decision))
                self.assertIsNotNone(metadata, f"missing Decision ID: {decision}")
                self.assertEqual(plan_id, metadata.group(1), f"decision belongs to wrong Plan: {decision}")
                self.assertEqual(match.group(1), metadata.group(2), f"decision filename/ID mismatch: {decision}")

    def test_local_markdown_links_resolve(self) -> None:
        maintained = [ROOT / "SKILL.md", ROOT / "README.md", ROOT / "README.zh-CN.md"]
        maintained.extend(sorted((ROOT / "references").glob("*.md")))
        maintained.extend(sorted((ROOT / "prompts").glob("*.md")))
        maintained.extend(sorted((ROOT / "docs" / "releases").glob("*.md")))
        maintained.extend(sorted(PLANTREE.rglob("*.md")))

        failures: list[str] = []
        for source in maintained:
            for raw_target in MARKDOWN_LINK_RE.findall(without_fenced_code(read(source))):
                target = raw_target.strip().strip("<>").split("#", 1)[0]
                if not target or "://" in target or target.startswith(("mailto:", "#")):
                    continue
                if any(marker in target for marker in ("<", ">", "{", "}")):
                    continue
                resolved = (source.parent / target).resolve()
                if not resolved.exists():
                    failures.append(f"{source.relative_to(ROOT)} -> {raw_target}")
        self.assertEqual([], failures, "broken local Markdown links:\n" + "\n".join(failures))

    def test_public_numbering_contract_is_consistent(self) -> None:
        skill = read(ROOT / "SKILL.md")
        english = read(ROOT / "README.md")
        chinese = read(ROOT / "README.zh-CN.md")

        self.assertIn("plans/<NNN>-<plan-name>/", skill)
        for public_readme in (english, chinese):
            self.assertIn("plans/001-<plan-name>/", public_readme)
            self.assertIn("P001", public_readme)
            self.assertIn("T001", public_readme)
            self.assertIn("Affected Modules", public_readme)

        self.assertIn("roadmap.md` is the sole active authority", skill)
        self.assertIn("Keep Plan roots flat by default", skill)
        self.assertIn("Prefer read-only drift detection over automatic repair", skill)

    def test_public_provider_instruction_contract_is_consistent(self) -> None:
        for public_readme in (read(ROOT / "README.md"), read(ROOT / "README.zh-CN.md")):
            self.assertIn("~/.claude/CLAUDE.md", public_readme)
            self.assertIn("~/.config/opencode/AGENTS.md", public_readme)
            self.assertIn("$CODEX_HOME/AGENTS.md", public_readme)
            self.assertIn("<!-- plan-tree:instructions:start -->", public_readme)
            self.assertIn("<!-- plan-tree:instructions:end -->", public_readme)
            self.assertIn("--no-instructions", public_readme)
            self.assertIn("--dry-run", public_readme)

        prompts = {
            provider: read(ROOT / "prompts" / f"{provider}.md")
            for provider in ("claude", "opencode", "codex")
        }
        for provider, prompt in prompts.items():
            self.assertIn("Plan Tree Long-Term Project Management", prompt, provider)
            self.assertIn("docs/plantree/README.md", prompt, provider)
            self.assertIn("does not grant permission", prompt, provider)

    def test_normalization_map_has_no_unfinished_rows(self) -> None:
        migration_map = PLANS / "001-numbering-system" / "indexes" / "migration-map.md"
        unfinished = [
            line
            for line in read(migration_map).splitlines()
            if line.startswith("|") and "| planned |" in line
        ]
        self.assertEqual([], unfinished, "normalization map still has planned rows")

    def test_maintained_markdown_has_no_trailing_whitespace(self) -> None:
        files = [ROOT / "SKILL.md", ROOT / "README.md", ROOT / "README.zh-CN.md"]
        files.extend(sorted((ROOT / "references").glob("*.md")))
        files.extend(sorted((ROOT / "prompts").glob("*.md")))
        files.extend(sorted((ROOT / "docs" / "releases").glob("*.md")))
        files.extend(sorted(PLANTREE.rglob("*.md")))
        failures = [
            f"{path.relative_to(ROOT)}:{line_number}"
            for path in files
            for line_number, line in enumerate(read(path).splitlines(), start=1)
            if line.rstrip() != line
        ]
        self.assertEqual([], failures, "trailing whitespace:\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
