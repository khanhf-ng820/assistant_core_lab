"""Protect the original Week 3 tests while allowing new Week 4 test files."""

import subprocess
from pathlib import Path

BASELINE = "d4b55f5d59a00c975ed42d0d63544c4a8989902d"
ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASELINE, "--", "tests"], cwd=ROOT, text=True
    ).splitlines()
    if not paths:
        raise RuntimeError("Week 3 test baseline is empty")
    result = subprocess.run(["git", "diff", "--exit-code", BASELINE, "--", *paths], cwd=ROOT)
    if result.returncode == 0:
        print(f"All {len(paths)} original Week 3 test files are unchanged.")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
