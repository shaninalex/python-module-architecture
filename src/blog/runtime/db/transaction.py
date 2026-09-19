from blog.core.middleware import Middleware, Invoke
from blog.runtime.db.session import Database


def transactional(db: Database) -> Middleware:
    def middleware(next_: Invoke) -> Invoke:
        async def call(msg: object) -> object:
            async with db.transaction():
                return await next_(msg)

        return call

    return middleware
