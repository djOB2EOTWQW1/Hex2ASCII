"""Entry point: pick the GUI backend by platform; --backend overrides."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Hex2ASCII")
    parser.add_argument("--backend", choices=["qt", "ctk"], default=None,
                        help="force a GUI backend")
    args = parser.parse_args()

    backend = args.backend or ("ctk" if sys.platform == "win32" else "qt")
    if backend == "ctk":
        from gui_ctk.app import main as run
    else:
        from gui_qt.app import main as run
    run()


if __name__ == "__main__":
    main()
