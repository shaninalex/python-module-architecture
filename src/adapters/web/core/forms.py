import re
from dataclasses import dataclass, field, fields
from email.utils import parseaddr
from typing import Self

from starlette.requests import Request

_EMAIL_RE = re.compile(r"[^@\s]+@[^@\s.]+(\.[^@\s.]+)+")


@dataclass
class Form:
    """Base form: parses ``request.form()`` and holds ``{field: message}``."""

    errors: dict[str, str] = field(default_factory=dict, init=False)

    @classmethod
    async def from_request(cls, request: Request) -> Self:
        form = await request.form()
        submitted = cls(**{
            f.name: str(form.get(f.name, "")).strip()
            for f in fields(cls) if f.init
        })
        submitted.validate()
        return submitted

    def validate(self) -> None:
        """Override: call the checks below, in order."""

    @property
    def valid(self) -> bool:
        return not self.errors

    def required(self, *names: str) -> None:
        for name in names:
            if not getattr(self, name):
                self._fail(name, "This field is required.")

    def valid_email(self, name: str) -> None:
        _, address = parseaddr(getattr(self, name))
        if not _EMAIL_RE.fullmatch(address):
            return self._fail(name, "Enter a valid email address.")
        setattr(self, name, address.lower())

    def min_length(self, name: str, length: int) -> None:
        if len(getattr(self, name)) < length:
            self._fail(name, f"Must be at least {length} characters long.")

    def same_as(self, name: str, other: str) -> None:
        if getattr(self, name) != getattr(self, other):
            self._fail(name, "Values do not match.")

    def checked(self, name: str) -> None:
        if not getattr(self, name):
            self._fail(name, "This box must be checked.")

    def _fail(self, name: str, message: str) -> None:
        self.errors.setdefault(name, message)
