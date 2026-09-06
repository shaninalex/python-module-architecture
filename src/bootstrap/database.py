import os

import databases
import sqlalchemy

_db_url = os.getenv("APP_DB")
if _db_url is None:
    raise Exception("Database url is not defined")

metadata = sqlalchemy.MetaData()
db = databases.Database(_db_url)
