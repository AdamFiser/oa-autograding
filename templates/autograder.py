#!/usr/bin/env python3
"""oa-autograding: nainstaluje knihovnu v pinované verzi a spustí kontroly
z checks.json, který leží vedle tohoto souboru (bundle classroom50).

Zvýšení verze = změna VERSION + commit + regrade (viz skill classroom50-provoz)."""
import pathlib
import subprocess
import sys

VERSION = "v1-rc"

subprocess.run(
    [sys.executable, "-m", "pip", "install", "--quiet", "--user",
     f"git+https://github.com/adamfiser/oa-autograding@{VERSION}"],
    check=True,
)

from oa_autograding.runner import main  # noqa: E402  (až po instalaci)

sys.exit(main(pathlib.Path(__file__).resolve().parent))
