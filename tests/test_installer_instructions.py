from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
START = "<!-- plan-tree:instructions:start -->"
END = "<!-- plan-tree:instructions:end -->"
INSTALLERS = ("python", "node")
PROVIDERS = ("claude", "opencode", "codex")


def provider_paths(home: Path, provider: str) -> tuple[Path, Path]:
    if provider == "claude":
        return home / ".claude" / "skills" / "plan-tree", home / ".claude" / "CLAUDE.md"
    if provider == "opencode":
        return (
            home / ".config" / "opencode" / "skill" / "plan-tree",
            home / ".config" / "opencode" / "AGENTS.md",
        )
    codex_home = home / "codex-home"
    return codex_home / "skills" / "plan-tree", codex_home / "AGENTS.md"


class InstallerInstructionTests(unittest.TestCase):
    maxDiff = None

    def run_installer(
        self,
        installer: str,
        home: Path,
        provider: str,
        *extra: str,
        source: Path = ROOT,
        expect_success: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        if installer == "python":
            command = [sys.executable, "-m", "plan_tree_installer.cli"]
        else:
            command = ["node", str(ROOT / "bin" / "plan-tree.js")]
        command.extend(("install", provider, "--source", str(source), *extra))

        env = os.environ.copy()
        env.update(
            {
                "HOME": str(home),
                "CODEX_HOME": str(home / "codex-home"),
                "PYTHONPATH": str(ROOT / "src"),
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        if expect_success:
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        else:
            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        return result

    def test_default_install_injects_all_provider_prompts_for_both_clis(self) -> None:
        for installer in INSTALLERS:
            with self.subTest(installer=installer), tempfile.TemporaryDirectory() as temporary:
                home = Path(temporary)
                self.run_installer(installer, home, "all")

                for provider in PROVIDERS:
                    skill, instructions = provider_paths(home, provider)
                    self.assertTrue((skill / "SKILL.md").is_file())
                    self.assertTrue((skill / "prompts" / f"{provider}.md").is_file())
                    content = instructions.read_text(encoding="utf-8")
                    prompt = (ROOT / "prompts" / f"{provider}.md").read_text(encoding="utf-8").strip()
                    self.assertEqual(1, content.count(START))
                    self.assertEqual(1, content.count(END))
                    self.assertIn(f"{START}\n{prompt}\n{END}", content)

    def test_reinstall_is_idempotent_and_preserves_user_content_and_mode(self) -> None:
        for installer in INSTALLERS:
            with self.subTest(installer=installer), tempfile.TemporaryDirectory() as temporary:
                home = Path(temporary)
                _, instructions = provider_paths(home, "codex")
                instructions.parent.mkdir(parents=True)
                user_content = "\ufeff## User Rules\n\nKeep this exact text.\n"
                instructions.write_text(user_content, encoding="utf-8")
                instructions.chmod(0o640)

                self.run_installer(installer, home, "codex")
                first = instructions.read_text(encoding="utf-8")
                self.run_installer(installer, home, "codex", "--force")
                second = instructions.read_text(encoding="utf-8")

                self.assertEqual(first, second)
                self.assertTrue(second.startswith(f"{user_content}\n"))
                self.assertEqual(1, second.count(START))
                self.assertEqual(1, second.count(END))
                if os.name != "nt":
                    self.assertEqual(0o640, stat.S_IMODE(instructions.stat().st_mode))

    def test_no_instructions_leaves_all_provider_files_absent(self) -> None:
        for installer in INSTALLERS:
            with self.subTest(installer=installer), tempfile.TemporaryDirectory() as temporary:
                home = Path(temporary)
                self.run_installer(installer, home, "all", "--no-instructions")
                for provider in PROVIDERS:
                    skill, instructions = provider_paths(home, provider)
                    self.assertTrue((skill / "SKILL.md").is_file())
                    self.assertFalse(instructions.exists())

    def test_dry_run_reports_instruction_targets_without_writing(self) -> None:
        for installer in INSTALLERS:
            with self.subTest(installer=installer), tempfile.TemporaryDirectory() as temporary:
                home = Path(temporary)
                result = self.run_installer(installer, home, "all", "--dry-run")
                self.assertIn("would create managed Plan Tree block", result.stdout)
                self.assertEqual([], list(home.iterdir()))

    def test_malformed_markers_fail_before_forced_skill_replacement(self) -> None:
        for installer in INSTALLERS:
            with self.subTest(installer=installer), tempfile.TemporaryDirectory() as temporary:
                home = Path(temporary)
                skill, instructions = provider_paths(home, "codex")
                skill.mkdir(parents=True)
                sentinel = skill / "user-sentinel.txt"
                sentinel.write_text("preserve", encoding="utf-8")
                instructions.parent.mkdir(parents=True, exist_ok=True)
                instructions.write_text(f"{START}\nunterminated\n", encoding="utf-8")

                result = self.run_installer(
                    installer,
                    home,
                    "codex",
                    "--force",
                    expect_success=False,
                )

                self.assertTrue(sentinel.is_file())
                self.assertIn("ambiguous Plan Tree instruction markers", result.stderr)

    def test_empty_prompt_fails_before_forced_skill_replacement(self) -> None:
        for installer in INSTALLERS:
            with self.subTest(installer=installer), tempfile.TemporaryDirectory() as temporary:
                home = Path(temporary)
                source = home / "source"
                source.mkdir()
                for filename in ("SKILL.md", "VERSION", "README.md", "README.zh-CN.md"):
                    shutil.copy2(ROOT / filename, source / filename)
                for directory in ("references", "assets", "prompts"):
                    shutil.copytree(ROOT / directory, source / directory)
                (source / "prompts" / "codex.md").write_text("", encoding="utf-8")

                skill, _ = provider_paths(home, "codex")
                skill.mkdir(parents=True)
                sentinel = skill / "user-sentinel.txt"
                sentinel.write_text("preserve", encoding="utf-8")

                result = self.run_installer(
                    installer,
                    home,
                    "codex",
                    "--force",
                    source=source,
                    expect_success=False,
                )

                self.assertTrue(sentinel.is_file())
                self.assertIn("empty provider prompts: prompts/codex.md", result.stderr)

    def test_non_utf8_instructions_fail_before_forced_skill_replacement(self) -> None:
        for installer in INSTALLERS:
            with self.subTest(installer=installer), tempfile.TemporaryDirectory() as temporary:
                home = Path(temporary)
                skill, instructions = provider_paths(home, "codex")
                skill.mkdir(parents=True)
                sentinel = skill / "user-sentinel.txt"
                sentinel.write_text("preserve", encoding="utf-8")
                instructions.parent.mkdir(parents=True, exist_ok=True)
                instructions.write_bytes(b"\xff\xfe")

                result = self.run_installer(
                    installer,
                    home,
                    "codex",
                    "--force",
                    expect_success=False,
                )

                self.assertTrue(sentinel.is_file())
                self.assertIn("is not valid UTF-8", result.stderr)

    def test_custom_skill_target_keeps_official_instruction_scope(self) -> None:
        for installer in INSTALLERS:
            with self.subTest(installer=installer), tempfile.TemporaryDirectory() as temporary:
                home = Path(temporary)
                custom_skill = home / "custom" / "plan-tree"
                _, instructions = provider_paths(home, "codex")
                self.run_installer(installer, home, "codex", "--target", str(custom_skill))

                self.assertTrue((custom_skill / "SKILL.md").is_file())
                self.assertTrue(instructions.is_file())
                self.assertFalse((custom_skill.parent / "AGENTS.md").exists())

    @unittest.skipIf(os.name == "nt", "symlink behavior requires platform privileges on Windows")
    def test_instruction_symlink_is_preserved_and_target_is_updated(self) -> None:
        for installer in INSTALLERS:
            with self.subTest(installer=installer), tempfile.TemporaryDirectory() as temporary:
                home = Path(temporary)
                _, instructions = provider_paths(home, "codex")
                dotfiles_target = home / "dotfiles" / "codex-agents.md"
                dotfiles_target.parent.mkdir(parents=True)
                dotfiles_target.write_text("## Shared dotfiles\n", encoding="utf-8")
                instructions.parent.mkdir(parents=True)
                instructions.symlink_to(dotfiles_target)

                self.run_installer(installer, home, "codex")

                self.assertTrue(instructions.is_symlink())
                content = dotfiles_target.read_text(encoding="utf-8")
                self.assertTrue(content.startswith("## Shared dotfiles\n\n"))
                self.assertEqual(1, content.count(START))


if __name__ == "__main__":
    unittest.main()
