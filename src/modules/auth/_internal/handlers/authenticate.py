from modules.auth import contract
from modules.auth._internal.domain import errors, ports


class AuthenticateByEmail:
    def __init__(
        self,
        credentials: contract.CredentialsReader,   # чужа реалізація, свій порт
        hasher: ports.Hasher,
        log: ports.LoginLog,
        clock: Clock,
    ) -> None:
        self._credentials = credentials
        self._hasher = hasher
        self._log = log
        self._clock = clock

    async def __call__(self, cmd: contract.AuthenticateByEmail) -> contract.SessionView:
        found = await self._credentials.by_email(email=cmd.email, provider="email")

        # ⚠️ Порівнюємо хеш ЗАВЖДИ, навіть якщо користувача немає, — інакше
        # різниця в часі відповіді дає оракул перебору акаунтів (§13.6).
        stored = found.password_hash if found else self._hasher.dummy_hash()
        matched = self._hasher.verify(stored, cmd.password.reveal())

        if found is None or not matched:
            raise errors.INVALID_CREDENTIALS      # одна помилка на обидва випадки
        if not found.active:
            raise errors.ACCOUNT_NOT_ACTIVE

        # Та сама транзакція, що й уся команда — відкрита middleware (§9.1).
        await self._log.record(customer_id=found.customer_id, at=self._clock.now())

        return contract.SessionView(
            customer_id=found.customer_id,
            issued_at=self._clock.now(),
        )