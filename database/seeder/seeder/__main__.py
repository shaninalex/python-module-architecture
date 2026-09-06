from seeder.args import seeder_arguments
from seeder.config import read_config


def main():
    parser = seeder_arguments()
    args = parser.parse_args()

    if not args.config.exists():
        parser.error(f"Config file not found: {args.config}")

    conf = read_config(args.config)

    args.func(conf)


if __name__ == "__main__":
    main()
