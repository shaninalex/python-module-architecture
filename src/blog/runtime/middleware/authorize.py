from blog.core import errors
from blog.core.actor import current_actor
from blog.core.middleware import Middleware, Invoke
from blog.runtime.permissions import Guard


def authorize(guard: Guard) -> Middleware:
    def middleware(next_: Invoke) -> Invoke:
        async def call(msg: object) -> object:
            check = getattr(msg, "permission", None)
            if check is None:
                raise TypeError(f"authorize: {type(msg).__name__} has no permission()")

            action = check()
            if action is None:
                return await next_(msg)

            actor = current_actor()
            if actor.is_system:
                return await next_(msg)
            if actor.user_id is None:
                raise errors.unauthenticated("auth.required", "Authentication required")

            guard.check(actor, action)
            return await next_(msg)

        return call

    return middleware
