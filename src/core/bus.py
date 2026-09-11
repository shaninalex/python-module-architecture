from typing import Callable, Awaitable, cast, get_origin, get_args, Any, get_type_hints

from core.messages import Command, Query
from core.middleware import Invoke, Middleware

type Handler[C, R] = Callable[[C], Awaitable[R]]


class CommandBus:
    def __init__(self, *middleware: Middleware) -> None:
        self._handlers: dict[type, Invoke] = {}
        self._chain = middleware
        self._sealed = False

    def register[R, C: Command[Any]](self, kind: type[C], handler: Handler[C, R]) -> None:
        if self._sealed:
            raise RuntimeError("bus: registration after seal()")
        if kind in self._handlers:
            raise RuntimeError(f"bus: handler for {kind.__name__} already registered")
        _assert_result_type(kind, handler)

        call: Invoke = cast(Invoke, handler)
        for mw in reversed(self._chain):
            call = mw(call)
        self._handlers[kind] = call

    def seal(self) -> None:
        """Close registration new commands after bootstrap"""
        self._sealed = True

    async def execute[R](self, cmd: Command[R]) -> R:
        try:
            call = self._handlers[type(cmd)]
        except KeyError:
            raise LookupError(f"bus: no handler for {type(cmd).__name__}") from None
        return cast(R, await call(cmd))


def _assert_result_type(kind: type, handler: Callable[..., Any]) -> None:
    for base in getattr(kind, "__orig_bases__", ()):
        if get_origin(base) in (Command, Query):
            declared = get_args(base)[0]
            break
    else:
        raise TypeError(f"{kind.__name__} must subclass Command[R] or Query[R]")

    returned = get_type_hints(handler).get("return")
    if (get_origin(returned) or returned) is not (get_origin(declared) or declared):
        raise TypeError(
            f"{kind.__name__} declares -> {declared}, handler returns {returned}"
        )
