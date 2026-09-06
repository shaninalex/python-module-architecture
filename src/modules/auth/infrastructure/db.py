from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from modules.auth.infrastructure.schema import CustomerLoginHistoryORM


class AuthDB:
    def __init__(self, db: AsyncEngine):
        self.db = db

    async def set_last_login(self, *, customer_id: int):
        async with AsyncSession(self.db) as session:
            customer_login = CustomerLoginHistoryORM(customer_id=customer_id)
            session.add(customer_login)
            await session.commit()
