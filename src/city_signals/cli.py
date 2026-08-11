"""CLI for city-signals — zAx4hub."""
from __future__ import annotations

import argparse
import json
import sys

from .engine import demo, inspect, run


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="city-signals", description="City open-data analysis toolkit")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo")
    run_p = sub.add_parser("run")
    run_p.add_argument("file", nargs="?", help="JSON input file")
    sub.add_parser("inspect")
    args = parser.parse_args(argv)
    if args.cmd == "demo":
        print(json.dumps(demo(), indent=2))
    elif args.cmd == "inspect":
        print(json.dumps(inspect(), indent=2))
    else:
        payload = {}
        if args.file:
            with open(args.file, encoding="utf-8") as f:
                payload = json.load(f)
        print(json.dumps(run(payload), indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
