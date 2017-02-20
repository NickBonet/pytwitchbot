import hashlib


# Handles loading and checking user permissions. ###


class UserPermission:
    def __init__(self, sql, conf):
        self.sql = sql
        self.conf = conf
        self.users = {}
        self.levels = {'BotAdmin': 3, 'BotOp': 2, 'Mod': 1}

    # Adds a user to the database. ###
    # TODO: Remember what my intended purpose was for user passwords
    def add_user(self, userinfo, passwd, level):
        if level in self.levels:
            self.sql.query('INSERT INTO py_users VALUES (?, ?, ?, ?, ?)',
                           (userinfo[0], userinfo[1], userinfo[2], passwd, self.levels[level]),)
            self.users = {}
            self.load_users()
            self.load_bot_master()
            return True
        else:
            return False

    # Deletes a user from the database. ###
    def del_user(self, user):
        try:
            self.sql.query('DELETE FROM py_users WHERE nick=?', (user,))
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
        masterhost = masternick + '.tmi.twitch.tv'
        masterpass = hashlib.sha1(str(self.conf.get_option('botmaster', 'pass')).encode('utf-8')).hexdigest()
        infodict = {'ident': masternick, 'host': masterhost, 'level': self.levels['BotAdmin'], 'pass': masterpass}
        self.users.update({masternick: infodict})

    # Loads users from SQLite and stores them into a local dictionary. ###
    def load_users(self):
        self.sql.query('SELECT * FROM py_users')
        for nick, ident, host, passwd, level in self.sql.fetch_all():
            infodict = {'ident': ident, 'host': host, 'level': level, 'pass': passwd}
            self.users.update({nick: infodict})

    # Actually checks if user has permission to run a command. ###
    def check_perm(self, userinfo, required_perm):
        if userinfo[0] in self.users:
            userprop = self.users[userinfo[0]]
            if userprop['ident'] == userinfo[1]:
                if userprop['host'] == userinfo[2]:
                    if userprop['level'] >= self.levels[required_perm]:
                        return True
            else:
                return False
        return False

    # Check if a user exists in the database
    def check_user_exists(self, user):
        try:
            self.sql.query('SELECT * FROM py_users WHERE nick=?', (user,))
            nick, ident, host, passwd, level = self.sql.fetch()
            if nick == user:
                return True
        except TypeError:
            return False
