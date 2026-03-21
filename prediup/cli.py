from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

REPO_URL = "https://github.com/nativ3ai/hermes-geopolitical-market-sim.git"
DEFAULT_REPO_ROOT = Path.home() / "src" / "hermes-geopolitical-market-sim"
DEFAULT_STACK_HOME = Path.home() / "predihermes"
DEFAULT_HERMES_HOME = Path.home() / ".hermes"


def say(message: str) -> None:
    print(f"[prediup] {message}")


def run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    say("$ " + " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=env, check=True)


def capture(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return proc.stdout.strip()


def ensure_repo(repo_root: Path) -> None:
    if (repo_root / ".git").is_dir():
        say(f"Reusing repo at {repo_root}")
        return
    if repo_root.exists():
        raise SystemExit(f"Target exists but is not a git repo: {repo_root}")
    repo_root.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", "--depth", "1", REPO_URL, str(repo_root)])


def hermes_installed(hermes_home: Path) -> bool:
    return shutil.which("hermes") is not None or hermes_home.exists()


def doctor(args: argparse.Namespace) -> int:
    commands = ["git", "python3", "npm", "node", "hermes"]
    optional = ["uv", "ollama"]
    missing = False
    for name in commands:
        if shutil.which(name):
            print(f"OK   {name}")
        else:
            print(f"MISS {name}")
            missing = True
    for name in optional:
        if shutil.which(name):
            print(f"OK   {name}")
        else:
            print(f"WARN {name}")
    print(f"INFO repo_root {args.repo_root}")
    print(f"INFO stack_home {args.stack_home}")
    print(f"INFO hermes_home {args.hermes_home}")
    return 1 if missing else 0


def install(args: argparse.Namespace) -> int:
    repo_root = args.repo_root.expanduser().resolve()
    stack_home = args.stack_home.expanduser().resolve()
    hermes_home = args.hermes_home.expanduser().resolve()

    if not hermes_installed(hermes_home):
        raise SystemExit("Hermes Agent is not installed. Install Hermes first, then rerun prediup install.")

    ensure_repo(repo_root)

    install_cmd = [
        "bash",
        "install.sh",
        "--bootstrap-local",
        "--ollama-model",
        args.ollama_model,
        "--ollama-base-url",
        args.ollama_base_url,
    ]
    if args.with_video_transcriber:
        install_cmd.append("--with-video-transcriber")
    if args.skip_ollama_install:
        install_cmd.append("--skip-ollama-install")
    if args.skip_ollama_pull:
        install_cmd.append("--skip-ollama-pull")
    if args.skip_hermes_env:
        install_cmd.append("--skip-hermes-env")
    if args.skip_worldosint_install:
        install_cmd.append("--skip-worldosint-install")
    if args.skip_mirofish_install:
        install_cmd.append("--skip-mirofish-install")

    env = os.environ.copy()
    env["PREDIHERMES_HOME"] = str(stack_home)
    env["HERMES_HOME"] = str(hermes_home)
    run(install_cmd, cwd=repo_root, env=env)
    return 0


def verify(args: argparse.Namespace) -> int:
    stack_home = args.stack_home.expanduser().resolve()
    hermes_home = args.hermes_home.expanduser().resolve()
    checks = {
        "skill": hermes_home / "skills" / "research" / "geopolitical-market-sim" / "SKILL.md",
        "helper": stack_home / "bin" / "predihermes-local-up",
        "health": stack_home / "bin" / "predihermes-local-health",
        "mirofish_env": stack_home / "companions" / "MiroFish" / ".env",
    }
    failed = False
    for label, path in checks.items():
        if path.exists():
            print(f"OK   {label} {path}")
        else:
            print(f"MISS {label} {path}")
            failed = True
    return 1 if failed else 0


def status(args: argparse.Namespace) -> int:
    stack_home = args.stack_home.expanduser().resolve()
    hermes_home = args.hermes_home.expanduser().resolve()
    print(f"repo_root={args.repo_root.expanduser().resolve()}")
    print(f"stack_home={stack_home}")
    print(f"hermes_home={hermes_home}")
    env_path = stack_home / "companions" / "MiroFish" / ".env"
    if env_path.exists():
        text = env_path.read_text(encoding="utf-8", errors="ignore")
        for key in ("LLM_BASE_URL", "LLM_MODEL_NAME", "GRAPH_BACKEND"):
            for line in text.splitlines():
                if line.startswith(f"{key}="):
                    print(line)
                    break
    else:
        print("mirofish_env=missing")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Installer for the PrediHermes local edition")
    parser.add_argument("command", choices=["doctor", "install", "verify", "status"])
    parser.add_argument("--repo-root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--stack-home", type=Path, default=DEFAULT_STACK_HOME)
    parser.add_argument("--hermes-home", type=Path, default=DEFAULT_HERMES_HOME)
    parser.add_argument("--ollama-model", default="qwen2.5:7b")
    parser.add_argument("--ollama-base-url", default="http://127.0.0.1:11434/v1")
    parser.add_argument("--with-video-transcriber", action="store_true")
    parser.add_argument("--skip-ollama-install", action="store_true")
    parser.add_argument("--skip-ollama-pull", action="store_true")
    parser.add_argument("--skip-hermes-env", action="store_true")
    parser.add_argument("--skip-worldosint-install", action="store_true")
    parser.add_argument("--skip-mirofish-install", action="store_true")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.command == "doctor":
        return doctor(args)
    if args.command == "install":
        return install(args)
    if args.command == "verify":
        return verify(args)
    if args.command == "status":
        return status(args)
    raise SystemExit(f"unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
