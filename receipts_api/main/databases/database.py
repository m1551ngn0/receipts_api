from time import sleep

from contextvars import ContextVar
from peewee import _ConnectionState, PostgresqlDatabase
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DATABASE_NAME = "receipts"

server_started = False
while not server_started:
    try:
        server_started = True
        con = psycopg2.connect(
            dbname='postgres',
            user="ofd-db",
            password="spam",
            host="ofd-db",
            port='5432'
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute(
            sql.SQL('CREATE DATABASE {}').format(sql.Identifier(DATABASE_NAME))
        )
    except psycopg2.errors.DuplicateDatabase:
        print('Database already exists!')
    except psycopg2.errors.OperationalError:
        server_started = False
        sleep(7)


db_state_default = {
    "closed": None,
    "conn": None,
    "ctx": None,
    "transactions": None
}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(_ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = PostgresqlDatabase(
    DATABASE_NAME,
    user="ofd-db",
    password="spam",
    host='ofd-db',
    port='5432'
)

db._state = PeeweeConnectionState()
