class Secret:
    """Represents sensitive string data that should never be logged or printed."""

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        self._value = str(value)

    def reveal(self) -> str:
        return self._value

    def __str__(self) -> str:
        return "[REDACTED]"

    def __repr__(self) -> str:
        return "Secret('[REDACTED]')"
