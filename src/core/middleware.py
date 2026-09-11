from typing import Awaitable, Callable

# A type-erased handler call: message in, result out.
type Invoke = Callable[[object], Awaitable[object]]

# Wraps every message passing through a bus.
type Middleware = Callable[[Invoke], Invoke]
