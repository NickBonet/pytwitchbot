import pymysql


# Handles MySQL related tasks. ###


class MySQL(object):
    # Loads MySQL information and connects to the server.###
    def __init__(self, conf):
        self.conf = conf
        self.host = self.conf.get_option('mysql', 'host')
        self.port = self.conf.get_int('mysql', 'port')
        self.user = self.conf.get_option('mysql', 'user')
        self.password = self.conf.get_option('mysql', 'pass')
        self.database = self.conf.get_option('mysql', 'database')
        self.conn = pymysql.connect(
            host=self.host, port=self.port,
            user=self.user, passwd=self.password, db=self.database, autocommit=True)
        self.cur = self.conn.cursor()

    # Performs an SQL query, but pings
    # the server first to make sure connection
    # is alive, if not, reconnect and query. ###
    def sql_query(self, query):
        self.conn.ping(True)
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

    # Used for sanitizing import for
    # SQL queries. ###
    def escape(self, string):
        return self.conn.escape(string)
