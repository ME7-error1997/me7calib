"""Run the ME7 Calib desktop app: ``python -m me7calib`` or the ``me7calib`` script."""

from __future__ import annotations

import sys


def main() -> int:
    from .families.bosch_me7 import BOSCH_ME7
    from .gui.app import run

    return run(BOSCH_ME7)


if __name__ == "__main__":
    sys.exit(main())
