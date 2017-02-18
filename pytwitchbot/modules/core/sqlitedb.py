import sqlite3
from pathlib import Path

# Handles SQLite related tasks. ###


class SQLiteDB(object):
    # Loads SQLite information and opens the database file.###
    def __init__(self, conf):
        self.conf = conf
        self.database = self.conf.get_option('sqlite', 'database')
        self.db_file = Path(self.database)
        if self.db_file.is_file():
            self.conn = sqlite3.connect(self.database, check_same_thread=False)
            self.conn.isolation_level = None
            self.cur = self.conn.cursor()
        else:
            self.conn = sqlite3.connect(self.database, check_same_thread=False)
            self.conn.isolation_level = None
            # Populates database with empty tables for modules which require them to function.
            self.conn.execute(open('../sql/py_users.sql').read())
            self.conn.execute(open('../sql/py_quotes.sql').read())
            self.conn.execute(open('../sql/py_facts.sql').read())
            self.cur = self.conn.cursor()

    # Performs an SQL query, passing any
    # arguments if necessary.
    def sql_query(self, query, args=None):
        if args is not None:
            self.cur.execute(query, args)
        else:
            self.cur.execute(query)

    # After a query is performed, fetches
    # all data that matches query. ###
    def fetch_all(self):
        return self.cur.fetchall()

    # After a query is performed, fetches
    # one result of data that matches
    # the query. ###
    def fetch(self):
        return self.cur.fetchone()

