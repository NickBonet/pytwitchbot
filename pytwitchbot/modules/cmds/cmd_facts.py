from modules.cmds.cmdmodule import *


# Module that allows for users to add and remove facts. ###


class CmdModuleFacts(CmdModule):
    def __init__(self, log, irc):
        super().__init__(log, irc)
        self.cmd_dict = {
            'factadd': {'function': self.add_fact, 'help':
                        'factadd <factname> <facttext> - Adds a fact to the fact database.'},
            'fact': {'function': self.read_fact, 'help':
                     'fact <factname> - Displays a fact from the database.'},
            'factdel': {'function': self.del_fact, 'help':
                        'factdel <factname> - Deletes a fact from the database.'},
            'factlock': {'function': self.lock_fact, 'help':
                         'factlock <factname> - Locks a fact so it cannot be changed.'},
            'factunlock': {'function': self.unlock_fact, 'help':
                           'factunlock <factname> - Unlocks a fact so it can be changed.'},
            'factinfo': {'function': self.info_fact, 'help':
                         'factinfo <factname> - Displays information about a fact.'},
            'factchange': {'function': self.change_fact, 'help': 'factchange <factname> <facttext> -'
                           ' Changes the text of a fact if it\'s not locked.'}}
        self.mod_type = 'chan'
        self.mod_perm_level = 'Mod'

    def add_fact(self, userinfo, dest, args):
        if len(args) > 2 and args[1] != '' and args[2] != '':
            try:
                facttext = " ".join(args[2:])
                self.irc.sql.query('INSERT INTO py_facts VALUES (?, ?, 0, ?, ?, ?)',
                                   (args[1], userinfo[0], self.irc.get_local_time, dest, facttext,))
                self.irc.msg(dest, 'Fact %s has been added to the database.' % (args[1]))
            except Exception as err:
                self.log.warning('Error while adding fact: %s' % err)
                self.irc.msg(dest, 'Couldn\'t add %s to the fact database.' % args[1])
        else:
            self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))

    def del_fact(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo, self.get_perm_level()):
            if len(args) > 1 and args[1] != '':
                try:
                    self.irc.sql.query('SELECT * FROM py_facts WHERE factname=?', (args[1],))
                    lockstatus = self.irc.sql.fetch()[2]
                    if lockstatus == 0:
                        self.irc.sql.query('DELETE FROM py_facts WHERE factname=?', (args[1],))
                        self.irc.msg(dest, 'Fact %s has been deleted.' % (args[1]))
                    else:
                        self.irc.msg(dest, 'Can\'t delete fact %s as it\'s a locked fact.' % args[1])
                except TypeError:
                    self.irc.msg(dest, 'That fact does not exist in the database!')
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(dest, 'You don\'t have permission to run that command!')

    def read_fact(self, userinfo, dest, args):
        if len(args) > 1 and args[1] != '':
            try:
                self.irc.sql.query('SELECT * FROM py_facts WHERE factname=?', (args[1],))
                factname, factauthor, lockstatus, date, channel, facttext = self.irc.sql.fetch()
                self.irc.msg(dest, 'Fact %s by %s: %s' % (factname, factauthor, facttext))
            except TypeError:
                self.irc.msg(dest, 'That fact does not exist in the database!')
        else:
            self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))

    def lock_fact(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo, self.get_perm_level()):
            if len(args) > 1 and args[1] != '':
                try:
                    self.irc.sql.query('SELECT * FROM py_facts WHERE factname=?', (args[1],))
                    lockstatus = self.irc.sql.fetch()[2]
                    if lockstatus == 0:
                        self.irc.sql.query('UPDATE py_facts SET factlock=1 WHERE factname=?', (args[1],))
                        self.irc.msg(dest, 'Fact %s is now locked.' % (args[1]))
                    else:
                        self.irc.msg(dest, 'Fact %s is already locked!' % args[1])
                except TypeError:
                    self.irc.msg(dest, 'That fact doesn\'t exist!')
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(dest, 'You don\'t have permission to run that command!')

    def unlock_fact(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo, self.get_perm_level()):
            if len(args) > 1 and args[1] != '':
                try:
                    self.irc.sql.query('SELECT * FROM py_facts WHERE factname=?', (args[1],))
                    lockstatus = self.irc.sql.fetch()[2]
                    if lockstatus == 1:
                        self.irc.sql.query('UPDATE py_facts SET factlock=0 WHERE factname=?', (args[1],))
                        self.irc.msg(dest, 'Fact %s is now unlocked.' % (args[1]))
                    else:
                        self.irc.msg(dest, 'Fact %s is already unlocked!' % args[1])
                except TypeError:
                    self.irc.msg(dest, 'That fact doesn\'t exist!')
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(dest, 'You don\'t have permission to run that command!')

    def info_fact(self, userinfo, dest, args):
        if len(args) > 1 and args[1] != '':
            try:
                self.irc.sql.query('SELECT * FROM py_facts WHERE factname=?', (args[1],))
                factname, factauthor, lockstatus, date, channel, facttext = self.irc.sql.fetch()
                if lockstatus == 0:
                    lockstatus = "Unlocked"
                else:
                    lockstatus = "Locked"
                self.irc.msg(dest, 'Fact info for %s:' % factname)
                self.irc.msg(dest, 'Fact author: %s | Fact lock status: %s | '
                                   'Date of when fact was added/modified: %s | Channel fact was added in: %s'
                             % (factauthor, lockstatus, date, channel))
            except TypeError:
                self.irc.msg(dest, 'That fact doesn\'t exist!')
        else:
            self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))

    def change_fact(self, userinfo, dest, args):
        if len(args) > 2 and args[1] != '' and args[2] != '':
            try:
                self.irc.sql.query('SELECT * FROM py_facts WHERE factname=?', (args[1],))
                lockstatus = int(self.irc.sql.fetch()[2])
                newtext = " ".join(args[2:])
                if lockstatus == 0:
                    self.irc.sql.query('UPDATE py_facts SET fact=?, factauthor=?, date=? WHERE factname=?',
                                       (newtext, userinfo[0], self.irc.get_local_time, args[1],))
                    self.irc.msg(dest, 'Fact has been changed.')
                else:
                    self.irc.msg(dest, 'The fact you\'re trying to change is locked.')
            except TypeError:
                self.irc.msg(dest, 'That fact doesn\'t exist!')
        else:
            self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))

