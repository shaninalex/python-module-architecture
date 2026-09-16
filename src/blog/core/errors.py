import enum


class Kind(enum.Enum):
    INTERNAL = enum.auto()
    VALIDATION = enum.auto()
    NOT_FOUND = enum.auto()
    CONFLICT = enum.auto()
    FORBIDDEN = enum.auto()
    UNAUTHENTICATED = enum.auto()
    RATE_LIMITED = enum.auto()


class AppError(Exception):
    def __init__(
            self,
            kind: Kind,
            code: str,
            message: str,
            *,
            fields: dict[str, str] | None = None,
            cause: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.kind = kind
        self.code = code
        self.message = message
        self.fields = fields or {}
        self.__cause__ = cause


def not_found(code: str, message: str) -> AppError: ...


def conflict(code: str, message: str) -> AppError: ...


def forbidden(code: str, message: str) -> AppError: ...


def validation(code: str, message: str, **fields: str) -> AppError: ...
