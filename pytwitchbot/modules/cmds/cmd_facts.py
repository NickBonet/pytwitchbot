from modules.cmds.cmdmodule import *


# Module that allows for users to add and remove facts. ###


class CmdModuleFacts(CmdModule):
    def __init__(self, log, irc):
        super().__init__(log, irc)
        self.cmd_dict = {
            'fadd': {'function': self.add_fact, 'help':
                     'fadd <factname> <facttext> - Adds a fact to the fact database.'},
            'fread': {'function': self.read_fact, 'help':
                      'fread <factname> - Displays a fact from the database.'},
            'fdel': {'function': self.del_fact, 'help':
                     'fdel <factname> - Deletes a fact from the database.'},
            'flock': {'function': self.lock_fact, 'help':
                      'flock <factname> - Locks a fact so it cannot be changed.'},
            'funlock': {'function': self.unlock_fact, 'help':
                        'funlock <factname> - Unlocks a fact so it can be changed.'},
            'finfo': {'function': self.info_fact, 'help':
                      'finfo <factname> - Displays information about a fact.'},
            'fchange': {'function': self.change_fact, 'help': 'fchange <factname> <facttext> -'
                                                               ' Changes the text of a fact if it\'s not locked.'}}
        self.mod_type = 'chan'

    def add_fact(self, userinfo, dest, args):
        if len(args) > 2 and args[1] != '' and args[2] != '':
            try:
                facttext = " ".join(args[2:])
                date = self.irc.get_local_time
                self.irc.sql.sql_query('INSERT INTO py_facts VALUES (?, ?, 0, ?, ?, ?)', (args[1], userinfo[0], date, dest, facttext,))
                self.irc.msg(dest, 'Fact %s has been added to the database.' % (args[1]))
            except Exception as err:
                self.log.warning('Error while adding fact to the database: %s' % err)
                self.irc.msg(dest, 'Couldn\'t add %s to the fact database.' % args[1])
        else:
            self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))

    def del_fact(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo[0], 1):
            if len(args) > 1 and args[1] != '':
                self.irc.sql.sql_query('DELETE FROM py_facts WHERE factname=?', (args[1],))
                self.irc.msg(dest, 'Fact %s has been deleted.' % (args[1]))
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(dest, 'You don\'t have permission to run that command!')

    def read_fact(self, userinfo, dest, args):
        if len(args) > 1 and args[1] != '':
            try:
                self.irc.sql.sql_query('SELECT * FROM py_facts WHERE factname=?', (args[1],))
                factname, factauthor, lockstatus, date, channel, facttext = self.irc.sql.fetch()
                self.irc.msg(dest, 'Fact %s by %s: %s' % (factname, factauthor, facttext))
            except Exception as err:
                self.log.warning('Error grabbing fact from database: %s' % err)
                self.irc.msg(dest, 'That fact does not exist in the database!')
        else:
            self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))

    def lock_fact(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo[0], 1):
            if len(args) > 1 and args[1] != '':
                self.irc.sql.sql_query('UPDATE py_facts SET factlock=1 WHERE factname=?', (args[1],))
                self.irc.msg(dest, 'Fact %s is now locked.' % (args[1]))
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(dest, 'You don\'t have permission to run that command!')

    def unlock_fact(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo[0], 1):
            if len(args) > 1 and args[1] != '':
                self.irc.sql.sql_query('UPDATE py_facts SET factlock=0 WHERE factname=?', (args[1],))
                self.irc.msg(dest, 'Fact %s is now unlocked.' % (args[1]))
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(dest, 'You don\'t have permission to run that command!')

    def info_fact(self, userinfo, dest, args):
        if len(args) > 1 and args[1] != '':
            try:
                self.irc.sql.sql_query('SELECT * FROM py_facts WHERE factname=?', (args[1],))
                factname, factauthor, lockstatus, date, channel, facttext = self.irc.sql.fetch()
                self.irc.msg(dest, 'Fact info for %s:' % factname)
                self.irc.msg(dest, 'Fact author: %s | Fact lock status: %i | Date of when fact was added: %s | '
                                   'Channel fact was added in: %s' % (factauthor, int(lockstatus), date, channel))
            except TypeError:
                self.irc.msg(dest, 'That fact doesn\'t exist!')
        else:
            self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))

    def change_fact(self, userinfo, dest, args):
        if len(args) > 2 and args[1] != '' and args[2] != '':
            try:
                self.irc.sql.sql_query('SELECT * FROM py_facts WHERE factname=?', (args[1],))
                lockstatus = int(self.irc.sql.fetch()[2])
                newtext = " ".join(args[2:])
                if lockstatus == 0:
                    self.irc.sql.sql_query('UPDATE py_facts SET fact=?, factauthor=? WHERE factname=?', (newtext, userinfo[0], args[1],))
                    self.irc.msg(dest, 'Fact has been changed.')
                else:
                    self.irc.msg(dest, 'The fact you\'re trying to change is locked.')
            except TypeError:
                self.irc.msg(dest, 'That fact doesn\'t exist!')
        else:
            self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))

