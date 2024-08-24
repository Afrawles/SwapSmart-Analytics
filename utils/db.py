import os
import psycopg2
import psycopg2.extras
from contextlib import contextmanager


class DBConnection:
    def __init__(self, dsn) -> None:
        self.POSTGRES_URL = dsn

    @contextmanager
    def manage_conn(self):
        self.conn = psycopg2.connect(self.POSTGRES_URL)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            yield self.cursor
        finally:
            self.cursor.close()
            self.conn.close()