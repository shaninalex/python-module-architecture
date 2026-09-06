from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from modules.customer.domain.customer import CustomerModel, CustomerCreate, CustomerUpdate
from modules.customer.domain.exceptions import CustomerAlreadyExistsException
from modules.customer.infrastructure.schema import CustomerORM, CustomerCredentialsORM


class CustomerDB:
    def __init__(self, db: AsyncEngine):
        self.db = db

    async def get(self, *, customer_id: int) -> CustomerModel | None:
        async with AsyncSession(self.db) as session:
            stmt = (
                select(CustomerORM)
                .options(
                    selectinload(CustomerORM.credentials),
                    selectinload(CustomerORM.login_history),
                )
                .where(CustomerORM.id == customer_id)
            )
            result: CustomerORM | None = await session.scalar(stmt)
            if result is None:
                return None

            return result.to_model()

    async def create(self, *, payload: CustomerCreate) -> CustomerModel:
        async with AsyncSession(self.db, expire_on_commit=False) as session:
            customer = CustomerORM(
                email=payload.email,
                full_name=payload.full_name,
                active=payload.active,
                credentials=[
                    CustomerCredentialsORM(
                        provider="email",
                        email=payload.email,
                        password_hash=payload.password,
                    ),
                ],
            )
            session.add(customer)
            try:
                await session.commit()
            except IntegrityError:
                raise CustomerAlreadyExistsException(message="Customer already exists")
            return customer.to_model()

    async def update(self, *, payload: CustomerUpdate) -> CustomerModel:
        raise Exception("not implemented")
