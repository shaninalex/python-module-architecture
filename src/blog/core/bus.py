from logging import Logger
from typing import Callable, Any, get_origin, get_args, get_type_hints, cast, Awaitable
from blog.core.messages import Command, Query, Event
from blog.core.middleware import Invoke, Middleware

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
        self._sealed = True

    async def execute[R](self, cmd: Command[R]) -> R:
        try:
            call = self._handlers[type(cmd)]
        except KeyError:
            raise LookupError(f"bus: no handler for {type(cmd).__name__}") from None
        return cast(R, await call(cmd))


class QueryBus:
    def __init__(self, *middleware: Middleware) -> None:
        self._handlers: dict[type, Invoke] = {}
        self._chain: tuple[Middleware, ...] = middleware
        self._sealed: bool = False

    def register[R, Q: Query[Any]](self, kind: type[Q], handler: Handler[Q, R]) -> None:
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
        self._sealed = True

    async def ask[R](self, query: Query[R]) -> R:
        try:
            call = self._handlers[type(query)]
        except KeyError:
            raise LookupError(f"bus: no handler for {type(query).__name__}") from None
        res = await call(query)
        return cast(R, res)


class EventBus:
    def __init__(self, log: Logger) -> None:
        self._subs: dict[type, list[Invoke]] = {}
        self._log = log

    def subscribe[E: Event](self, kind: type[E], handler: Handler[E, None]) -> None:
        self._subs.setdefault(kind, []).append(cast(Invoke, handler))

    async def publish(self, event: Event) -> None:
        failures: list[Exception] = []
        for handler in self._subs.get(type(event), ()):
            try:
                await handler(event)
            except Exception as exc:
                self._log.exception("event handler failed", extra={
                    "event": event.event_name,
                    "handler": getattr(handler, "__qualname__", repr(handler)),
                })
                failures.append(exc)
        if failures:
            raise ExceptionGroup(f"{event.event_name}: subscribers failed", failures)


def _assert_result_type(kind: type, handler: Callable[..., Any]) -> None:
    for base in getattr(kind, "__orig_bases__", ()):
        if get_origin(base) in (Command, Query):
            declared = get_args(base)[0]
            break
    else:
        raise TypeError(f"{kind.__name__} must subclass Command[R] or Query[R]")

    returned = get_type_hints(handler).get("return")
    if (get_origin(returned) or returned) is not (get_origin(declared) or declared):
        raise TypeError(f"{kind.__name__} declares -> {declared}, handler returns {returned}")
