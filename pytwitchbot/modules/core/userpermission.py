import hashlib


# Handles loading and checking user permissions. ###


class UserPermission:
    def __init__(self, sql, conf):
        self.sql = sql
        self.conf = conf
        self.users = {}

    # Adds a user to the database. ###
    def add_user(self, userinfo, passwd, level):
        if level <= 3:
            self.sql.query('INSERT INTO py_users VALUES (?, ?, ?, ?, ?)', (userinfo[0], userinfo[1], userinfo[2], passwd, int(level),))
            self.users = {}
            self.load_users()
            self.load_bot_master()
            return True
        else:
            return False

    # Deletes a user from the database. ###
    def del_user(self, user):
        try:
            self.sql.query('DELETE FROM py_users WHERE nick=?' % (user,))
            self.users = {}
            self.load_users()
            self.load_bot_master()
            return True
        except Exception as err:
            self.conf.log.info('Error while deleting user: %s' % err)
            return False

    # Loads the main bot master from configuration. ###
    def load_bot_master(self):
        masternick = self.conf.get_option('botmaster', 'nick')
        masterident = self.conf.get_option('botmaster', 'ident')
        masterhost = self.conf.get_option('botmaster', 'host')
        masterpass = hashlib.sha1(str(self.conf.get_option('botmaster', 'pass')).encode('utf-8')).hexdigest()
        infodict = {'ident': masterident, 'host':masterhost, 'level': 3, 'pass': masterpass}
        self.users.update({masternick: infodict})

    # Loads users from SQLite and stores them into a local dictionary. ###
    def load_users(self):
        self.sql.query('SELECT * FROM py_users')
        for nick, ident, host, passwd, level in self.sql.fetch_all():
            infodict = {'ident': ident, 'host':host, 'level': level, 'pass': passwd}
            self.users.update({nick: infodict})

    # Actually checks if user has permission to run a command. ###
    def check_perm(self, user, perm):
        if user in self.users:
            userprop = self.users[user]
            if userprop['level'] >= perm:
                return True
            else:
                return False
        return False
