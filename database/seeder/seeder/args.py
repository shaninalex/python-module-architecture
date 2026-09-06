import argparse
from pathlib import Path

from seeder import seeder


def seeder_arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seeder",
        description=(
            "Database mock data generator for the shoe store.\n\n"
            "This tool populates the database with realistic mock data "
            "for development and testing environments."
        ),
        epilog=(
            "Usage:\n"
            "  seeder --config=./path/for/seed/config.yaml start\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to YAML configuration file containing database and seeding settings.",
    )

    subparsers = parser.add_subparsers(title="commands", dest="command", required=True, metavar="<command>")

    start_cmd = subparsers.add_parser(
        "start",
        help="Execute seeder.",
        description="Execute seeder. First it clears the current data, then generates new one",
    )
    start_cmd.set_defaults(func=seeder.start)

    return parser
