#!/usr/bin/env python3

import sys
from pathlib import Path
from gui.main import main

print(f"[DEBUG] Arguments reçus : {sys.argv}")

selected_file = None
if len(sys.argv) > 1:
    path = Path(sys.argv[1].strip("'"))  # Retire les quotes si transmises
    if path.exists() and path.suffix == ".AppImage":
        selected_file = path

main(preselected_file=selected_file)
