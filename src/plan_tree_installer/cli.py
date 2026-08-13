from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

PACKAGE_VERSION = "0.4.0"
REPO_ZIP_URL = "https://github.com/SeemSeam/plan-tree/archive/refs/tags/v{version}.zip"
README_URL = "https://github.com/SeemSeam/plan-tree#readme"
SKILL_NAME = "plan-tree"

CORE_FILES = [
    "SKILL.md",
    "VERSION",
    "README.md",
    "README.zh-CN.md",
]

CORE_DIRS = [
    "references",
    "assets",
    "prompts",
]

PROVIDER_DIRS = {
    "claude": lambda: Path.home() / ".claude" / "skills" / SKILL_NAME,
    "opencode": lambda: Path.home() / ".config" / "opencode" / "skill" / SKILL_NAME,
    "codex": lambda: Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills" / SKILL_NAME,
}
PROVIDER_INSTRUCTION_FILES = {
    "claude": lambda: Path.home() / ".claude" / "CLAUDE.md",
    "opencode": lambda: Path.home() / ".config" / "opencode" / "AGENTS.md",
    "codex": lambda: Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "AGENTS.md",
}
INSTRUCTION_START = "<!-- plan-tree:instructions:start -->"
INSTRUCTION_END = "<!-- plan-tree:instructions:end -->"
SUPPORTED_PROVIDERS = [*PROVIDER_DIRS.keys(), "all"]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="plan-tree",
        description="Install the plan-tree AI planning skill for Claude, opencode, or Codex.",
        epilog=f"README: {README_URL}",
    )
    subparsers = parser.add_subparsers(dest="command")

    install = subparsers.add_parser("install", help="Install the plan-tree skill")
    install.add_argument(
        "provider_arg",
        nargs="?",
        choices=SUPPORTED_PROVIDERS,
        metavar="provider",
        help="Provider install target. Default: claude.",
    )
    install.add_argument(
        "--provider",
        dest="provider_opt",
        choices=SUPPORTED_PROVIDERS,
        help="Backward-compatible provider target option.",
    )
    install.add_argument(
        "--target",
        type=Path,
        help="Explicit install directory. Cannot be used with provider all.",
    )
    install.add_argument(
        "--source",
        type=Path,
        help="Use a local plan-tree repository path instead of downloading the GitHub tag.",
    )
    install.add_argument(
        "--version",
        default=PACKAGE_VERSION,
        help=f"GitHub tag version to install. Default: {PACKAGE_VERSION}.",
    )
    install.add_argument("--force", action="store_true", help="Replace an existing install directory.")
    install.add_argument("--dry-run", action="store_true", help="Print planned actions without writing files.")
    install.add_argument(
        "--no-instructions",
        action="store_true",
        help="Install only the skill and leave the provider's persistent instruction file unchanged.",
    )

    subparsers.add_parser("version", help="Print the installer version")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "version":
        print(PACKAGE_VERSION)
        return 0
    if args.command == "install":
        try:
            args.provider = normalize_provider(args)
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        try:
            return install(args)
        except (OSError, RuntimeError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
    print("Use `plan-tree install claude|opencode|codex|all`.")
    print(f"README: {README_URL}")
    return 2


def normalize_provider(args: argparse.Namespace) -> str:
    provider_arg = args.provider_arg
    provider_opt = args.provider_opt
    if provider_arg and provider_opt and provider_arg != provider_opt:
        raise RuntimeError("provider specified twice with different values")
    return provider_arg or provider_opt or "claude"


def install(args: argparse.Namespace) -> int:
    if args.target and args.provider == "all":
        print("--target cannot be combined with provider all", file=sys.stderr)
        return 2

    providers = list(PROVIDER_DIRS) if args.provider == "all" else [args.provider]
    targets = [(provider, args.target or PROVIDER_DIRS[provider]()) for provider in providers]

    source = args.source.resolve() if args.source else None
    temp_dir: tempfile.TemporaryDirectory[str] | None = None
    if source is None:
        temp_dir = tempfile.TemporaryDirectory(prefix="plan-tree-")
        source = download_source(args.version, Path(temp_dir.name))

    try:
        validate_source(source)
        if not args.dry_run:
            for provider, target in targets:
                preflight_skill_target(target.expanduser(), args.force)
                if not args.no_instructions:
                    preflight_instruction_target(PROVIDER_INSTRUCTION_FILES[provider]().expanduser())
        for provider, target in targets:
            install_to_provider(source, target.expanduser(), provider, args.force, args.dry_run)
            if not args.no_instructions:
                install_provider_instructions(
                    source,
                    PROVIDER_INSTRUCTION_FILES[provider]().expanduser(),
                    provider,
                    args.dry_run,
                )
        if not args.dry_run:
            print(f"Read the README: {README_URL}")
    finally:
        if temp_dir is not None:
            temp_dir.cleanup()

    return 0


def download_source(version: str, temp_root: Path) -> Path:
    url = REPO_ZIP_URL.format(version=version)
    archive_path = temp_root / f"plan-tree-{version}.zip"
    print(f"Downloading {url}")
    urllib.request.urlretrieve(url, archive_path)

    with zipfile.ZipFile(archive_path) as archive:
        archive.extractall(temp_root)

    candidates = [path for path in temp_root.iterdir() if path.is_dir() and path.name.startswith("plan-tree-")]
    if not candidates:
        raise RuntimeError(f"Could not locate extracted plan-tree source in {temp_root}")
    return candidates[0]


def validate_source(source: Path) -> None:
    missing = [name for name in CORE_FILES if not (source / name).is_file()]
    missing += [name for name in CORE_DIRS if not (source / name).is_dir()]
    missing += [
        f"prompts/{provider}.md"
        for provider in PROVIDER_DIRS
        if not (source / "prompts" / f"{provider}.md").is_file()
    ]
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(f"{source} is not a valid plan-tree source; missing: {joined}")
    empty_prompts = [
        f"prompts/{provider}.md"
        for provider in PROVIDER_DIRS
        if not read_utf8(source / "prompts" / f"{provider}.md").strip()
    ]
    if empty_prompts:
        joined = ", ".join(empty_prompts)
        raise RuntimeError(f"{source} is not a valid plan-tree source; empty provider prompts: {joined}")


def preflight_skill_target(target: Path, force: bool) -> None:
    if target.exists() and not force:
        raise RuntimeError(f"{target} already exists. Use --force to replace it.")


def preflight_instruction_target(target: Path) -> None:
    resolved = resolve_instruction_target(target)
    if resolved.exists() and not resolved.is_file():
        raise RuntimeError(f"{target} is not a regular provider instruction file.")
    if resolved.is_file():
        managed_block_span(read_utf8(resolved, display=target), target)


def install_to_provider(source: Path, target: Path, provider: str, force: bool, dry_run: bool) -> None:
    include_agents = provider == "codex"
    planned = [*CORE_FILES, *CORE_DIRS]
    if include_agents and (source / "agents").is_dir():
        planned.append("agents")

    print(f"Installing plan-tree for {provider} -> {target}")
    if dry_run:
        for item in planned:
            print(f"  would copy {item}")
        return

    if target.exists():
        if not force:
            raise RuntimeError(f"{target} already exists. Use --force to replace it.")
        shutil.rmtree(target)

    target.mkdir(parents=True, exist_ok=True)
    for item in planned:
        src = source / item
        dst = target / item
        if src.is_dir():
            shutil.copytree(src, dst)
        elif src.is_file():
            shutil.copy2(src, dst)

    print(f"Installed plan-tree {read_version(target)}")


def install_provider_instructions(source: Path, target: Path, provider: str, dry_run: bool) -> None:
    prompt = read_utf8(source / "prompts" / f"{provider}.md").strip()
    if not prompt:
        raise RuntimeError(f"Provider prompt is empty: prompts/{provider}.md")

    resolved = resolve_instruction_target(target)
    action = "update" if resolved.is_file() else "create"
    print(f"Persistent instructions for {provider} -> {target}")
    if dry_run:
        print(f"  would {action} managed Plan Tree block")
        return

    existing = read_utf8(resolved, display=target) if resolved.is_file() else ""
    updated = merge_managed_instructions(existing, prompt, target)
    if updated == existing:
        print("Persistent instructions already current")
        return

    atomic_write_text(resolved, updated)
    print(f"{action.capitalize()}d persistent instructions")


def resolve_instruction_target(target: Path) -> Path:
    if not target.is_symlink():
        return target
    try:
        return target.resolve(strict=True)
    except FileNotFoundError as exc:
        raise RuntimeError(f"{target} is a dangling symbolic link; repair it before installing.") from exc


def read_utf8(path: Path, display: Path | None = None) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"{display or path} is not valid UTF-8; convert it before installing.") from exc


def managed_block_span(content: str, target: Path) -> tuple[int, int] | None:
    starts = content.count(INSTRUCTION_START)
    ends = content.count(INSTRUCTION_END)
    if starts == 0 and ends == 0:
        return None
    if starts != 1 or ends != 1:
        raise RuntimeError(
            f"{target} has ambiguous Plan Tree instruction markers; repair them manually before installing."
        )

    start = content.index(INSTRUCTION_START)
    end_start = content.index(INSTRUCTION_END)
    if end_start < start:
        raise RuntimeError(
            f"{target} has reversed Plan Tree instruction markers; repair them manually before installing."
        )
    return start, end_start + len(INSTRUCTION_END)


def merge_managed_instructions(existing: str, prompt: str, target: Path) -> str:
    newline = "\r\n" if "\r\n" in existing else "\n"
    normalized_prompt = newline.join(prompt.splitlines())
    block = newline.join((INSTRUCTION_START, normalized_prompt, INSTRUCTION_END))
    span = managed_block_span(existing, target)
    if span is not None:
        start, end = span
        return f"{existing[:start]}{block}{existing[end:]}"
    if not existing:
        return f"{block}{newline}"

    if existing.endswith(newline * 2):
        separator = ""
    elif existing.endswith(newline):
        separator = newline
    else:
        separator = newline * 2
    return f"{existing}{separator}{block}{newline}"


def atomic_write_text(target: Path, content: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    existing_mode = target.stat().st_mode if target.exists() else None
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.plan-tree-",
        dir=target.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
        if existing_mode is not None:
            os.chmod(temporary, existing_mode)
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()


def read_version(target: Path) -> str:
    version_file = target / "VERSION"
    if version_file.is_file():
        return f"v{version_file.read_text(encoding='utf-8').strip()}"
    return "unknown version"


if __name__ == "__main__":
    raise SystemExit(main())
