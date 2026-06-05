from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

PACKAGE_VERSION = "0.2.1"
REPO_ZIP_URL = "https://github.com/SeemSeam/plan-tree/archive/refs/tags/v{version}.zip"
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
]

PROVIDER_DIRS = {
    "claude": lambda: Path.home() / ".claude" / "skills" / SKILL_NAME,
    "opencode": lambda: Path.home() / ".config" / "opencode" / "skill" / SKILL_NAME,
    "codex": lambda: Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills" / SKILL_NAME,
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="plan-tree",
        description="Install the plan-tree AI planning skill for Claude, opencode, or Codex.",
    )
    subparsers = parser.add_subparsers(dest="command")

    install = subparsers.add_parser("install", help="Install the plan-tree skill")
    install.add_argument(
        "--provider",
        choices=[*PROVIDER_DIRS.keys(), "all"],
        default="claude",
        help="Provider install target. Default: claude.",
    )
    install.add_argument(
        "--target",
        type=Path,
        help="Explicit install directory. Cannot be used with --provider all.",
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

    subparsers.add_parser("version", help="Print the installer version")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "version":
        print(PACKAGE_VERSION)
        return 0
    if args.command == "install":
        return install(args)
    print("Use `plan-tree install --provider claude|opencode|codex`.")
    return 2


def install(args: argparse.Namespace) -> int:
    if args.target and args.provider == "all":
        print("--target cannot be combined with --provider all", file=sys.stderr)
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
        for provider, target in targets:
            install_to_provider(source, target.expanduser(), provider, args.force, args.dry_run)
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
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(f"{source} is not a valid plan-tree source; missing: {joined}")


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


def read_version(target: Path) -> str:
    version_file = target / "VERSION"
    if version_file.is_file():
        return f"v{version_file.read_text(encoding='utf-8').strip()}"
    return "unknown version"


if __name__ == "__main__":
    raise SystemExit(main())
