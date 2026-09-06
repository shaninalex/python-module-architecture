from sqlalchemy.ext.asyncio import AsyncEngine

from bootstrap.abstract import Module
from bootstrap.container import Container
from core.command_bus import CommandBus
from modules.auth.application.commands import EmailAuthenticationCommand
from modules.auth.application.email_login_handler import EmailAuthenticationHandler
from modules.auth.application.ports import AuthCredentialsReaderPort
from modules.auth.infrastructure.db import AuthDB


class AuthModule(Module):
    def configure(self, container: Container):
        auth_reader: AuthCredentialsReaderPort = container.resolve(AuthCredentialsReaderPort)
        db = container.resolve(AsyncEngine)
        auth_internal_port = AuthDB(db)

        cmd = container.resolve(CommandBus)
        cmd.register(EmailAuthenticationCommand, EmailAuthenticationHandler(auth_reader, auth_internal_port))