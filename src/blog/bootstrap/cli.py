from argparse import Namespace

from blog.runtime.config import Config


def serve(args: Namespace, cfg: Config) -> int:
    import uvicorn
    uvicorn.run(
        f"blog.asgi.{args.target}:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
    return 0