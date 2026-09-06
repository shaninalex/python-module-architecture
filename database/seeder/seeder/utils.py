import psycopg2
from psycopg2 import OperationalError

from seeder.config import Config


def create_connection(config: Config):
    try:
        connection = psycopg2.connect(
            database=config.database.database,
            user=config.database.user,
            password=config.database.password,
            host=config.database.host,
            port=config.database.port,
        )
        print("Connection successful")
    except OperationalError as e:
        raise OperationalError(f"The error '{e}' occurred")
    return connection


def execute_raw_sql(connection, sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
