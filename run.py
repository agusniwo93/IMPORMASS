"""Punto de entrada para ejecutar IMPORMASS.

Uso:
    .venv\\Scripts\\python.exe run.py
"""
import sys
from pathlib import Path

# Asegurar que src/ esté en el path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from impormass.app import main

if __name__ == "__main__":
    main()
