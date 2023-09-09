__all__ = ["metadata", "database"]

import databases
import sqlalchemy
from decouple import config

DATABASE_URL = f'{config("DB_DRIVER")}://{config("DB_USER")}:{config("DB_PASS")}@localhost:/{config("DB_NAME")}'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
