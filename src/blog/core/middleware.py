from collections.abc import Awaitable, Callable
from typing import Any

type Invoke = Callable[[Any], Awaitable[Any]]
type Middleware = Callable[[Invoke], Invoke]
