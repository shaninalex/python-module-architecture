from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from modules.auth.application.ports import AuthCredentials
from modules.customer.infrastructure.schema import CustomerCredentialsORM, CustomerORM


class CustomerAuthReader:
    def __init__(self, db: AsyncEngine):
        self.db = db

    async def get_login_credentials(self, *, email: str, credentials_type: str = "email"):
        async with AsyncSession(self.db) as session:
            stmt = (
                select(CustomerCredentialsORM, CustomerORM.active)
                .join(CustomerORM, CustomerORM.id == CustomerCredentialsORM.customer_id)
                .where(
                    CustomerCredentialsORM.email == email,
                    CustomerCredentialsORM.provider == credentials_type,
                )
            )
            result = await session.execute(stmt)
            row = result.one_or_none()
            if row is None:
                return None

            credentials, active = row
            cm = credentials.to_model()
            return AuthCredentials(
                customer_id=cm.customer_id,
                password_hash=cm.password_hash,
                active=active,
            )
