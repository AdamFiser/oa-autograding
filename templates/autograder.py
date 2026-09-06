#!/usr/bin/env python3
"""oa-autograding: nainstaluje knihovnu v pinované verzi a spustí kontroly
z checks.json, který leží vedle tohoto souboru (bundle classroom50).

Zvýšení verze = změna VERSION + commit + regrade (viz skill classroom50-provoz)."""
import importlib
import pathlib
import site
import subprocess
import sys

VERSION = "v1-rc"

PACKAGE = f"git+https://github.com/adamfiser/oa-autograding@{VERSION}"
PIP = [sys.executable, "-m", "pip", "install", "--quiet"]

# Ve virtualenvu `--user` selže, jinde je naopak jediná zapisovatelná cesta.
if subprocess.run([*PIP, "--user", PACKAGE]).returncode != 0:
    subprocess.run([*PIP, PACKAGE], check=True)

# Pokud adresář user site-packages při startu interpretu neexistoval, není v sys.path
# (site.addusersitepackages ho přidává jen když existuje) — čerstvě nainstalovaný balík
# by proto nešel naimportovat.
usersite = site.getusersitepackages()
if isinstance(usersite, str) and usersite not in sys.path:
    sys.path.insert(0, usersite)
importlib.invalidate_caches()

from oa_autograding.runner import main  # noqa: E402  (až po instalaci)

sys.exit(main(pathlib.Path(__file__).resolve().parent))
