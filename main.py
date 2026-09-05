"""Run MediaNovaBot from the workspace root."""

import runpy
import sys
from pathlib import Path


def main():
    app_dir = Path(__file__).parent / "MediaNovaBot"
    sys.path.insert(0, str(app_dir))
    runpy.run_path(str(app_dir / "main.py"), run_name="__main__")


if __name__ == "__main__":
    main()
