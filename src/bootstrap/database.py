import os

import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine

_db_url = os.getenv("APP_DB")
if _db_url is None:
    raise Exception("Database url is not defined")


debug = False
if os.getenv("APP_MARKET_ENV") is not None and os.getenv("APP_MARKET_ENV") == "development":
    debug = True

metadata = sqlalchemy.MetaData()
db_engine = create_async_engine(_db_url, echo=debug, connect_args={"ssl": False})