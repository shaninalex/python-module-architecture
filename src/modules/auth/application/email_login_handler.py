from dataclasses import dataclass

from argon2 import PasswordHasher

from modules.auth.application.commands import EmailAuthenticationCommand
from modules.auth.application.ports import AuthCredentialsReaderPort
from modules.auth.domain.exceptions import AuthUserNotActiveError, AuthPasswordNotMatchError, \
    AuthCredentialsNotFoundError
from modules.auth.domain.port import AuthPort


@dataclass(frozen=True)
class AuthenticatedUser:
    customer_id: int


class EmailAuthenticationHandler:

    def __init__(self, auth_reader: AuthCredentialsReaderPort, auth_port: AuthPort):
        self.auth_reader = auth_reader
        self.auth_port = auth_port

    async def __call__(self, cmd: EmailAuthenticationCommand) -> AuthenticatedUser:
        """
            We return user id if success or none if not.
        """
        credentials = await self.auth_reader.get_login_credentials(email=cmd.email, credentials_type="email")
        if credentials is None:
            raise AuthCredentialsNotFoundError

        if not credentials.active:
            raise AuthUserNotActiveError

        try:
            ph = PasswordHasher()
            ph.verify(credentials.password_hash, cmd.raw_password)
        except Exception:
            raise AuthPasswordNotMatchError

        await self.auth_port.set_last_login(customer_id=credentials.customer_id)
        return AuthenticatedUser(credentials.customer_id)
