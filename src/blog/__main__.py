import asyncio
import sys
from argparse import Namespace

from blog.bootstrap.app import build_app

from blog.adapters.cli.parser import build_parser
from blog.bootstrap.cli import dispatch

from blog.core.actor import Actor, acting_as
from blog.runtime.config import config_path, load, Config


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    cfg = load(config_path(args.config))
    return asyncio.run(_run(cfg, args))


async def _run(cfg: Config, args: Namespace) -> int:
    app = await build_app(cfg)
    try:
        with acting_as(Actor.system()):
            return await dispatch(app, args)
    finally:
        await app.aclose()


if __name__ == "__main__":
    raise SystemExit(main())
