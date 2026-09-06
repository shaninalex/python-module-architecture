class AuthUserNotActiveError(Exception):
    """Exception raised for if user not active and try to log in."""

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class AuthPasswordNotMatchError(Exception):
    """Exception raised if passwords don't match."""

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


class AuthCredentialsNotFoundError(Exception):
    """Exception raised if credentials was not found."""

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)
