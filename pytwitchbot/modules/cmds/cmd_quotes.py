from modules.cmds.cmdmodule import *


# Module to allow quotes to be stored and read using SQlite. ###


class CmdModuleQuotes(CmdModule):
    def __init__(self, log, irc):
        super().__init__(log, irc)
        self.cmd_dict = {
            'qadd': {'function': self.add_quote, 'help':
                     'qadd <text to quote> - Adds a quote to the database.'},
            'qdel': {'function': self.del_quote, 'help':
                     'qdel <quote number> - Deletes a quote from the database.'},
            'quote': {'function': self.read_quote, 'help':
                      'quote <quote number> - Displays a quote.'},
            'qtotal': {'function': self.count_quotes, 'help':
                       'qtotal - Displays the total amount of quotes in the database for the current channel.'}}
        self.mod_type = 'chan'
        self.mod_perm_level = 'Mod'

    def add_quote(self, userinfo, dest, args):
        if len(args) > 1 and args[1] != '':
            quotetext = " ".join(args[1:])
            date = self.irc.get_local_time
            self.irc.sql.query('SELECT IFNULL(MAX(qchid)+1,1) FROM py_quotes WHERE qchan=?', (dest,))
            qid = int(self.irc.sql.fetch()[0])
            self.irc.sql.query('INSERT INTO py_quotes VALUES (null, ?, ?, ?, ?, ?)',
                               (int(qid), userinfo[0], dest, date, quotetext,))
            self.irc.msg(dest, 'Quote #%i added to the database by %s:' % (qid, userinfo[0]))
            self.irc.msg(dest, 'Quote: %s' % (" ".join(args[1:])))
        else:
            self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))

    def del_quote(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo, self.get_perm_level()):
            if len(args) > 1 and args[1] != '':
                try:
                    self.irc.sql.query('SELECT * FROM py_quotes WHERE qchid=? AND qchan=?', (int(args[1]), dest,))
                    qid, qchid, nick, chan, qdate, quote = self.irc.sql.fetch()
                    if qchid == int(args[1]) and chan == dest:
                        self.irc.sql.query('DELETE FROM py_quotes WHERE qchid=? AND qchan=?', (int(args[1]), dest,))
                        self.irc.msg(dest, 'Quote has been removed from the database.')
                except TypeError:
                    self.irc.msg(dest, 'That quote doesn\'t exist in the database!')
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(dest, 'You don\'t have permission to run that command!')

    # noinspection PyUnusedLocal
    def read_quote(self, userinfo, dest, args):
        if len(args) > 1 and args[1] != '':
            try:
                self.irc.sql.query('SELECT * FROM py_quotes WHERE qchid=? AND qchan=?', (int(args[1]), dest,))
                qid, qchid, nick, chan, qdate, quote = self.irc.sql.fetch()
                self.irc.msg(dest, 'Quote %i added by %s on %s:' % (qchid, nick, qdate))
                self.irc.msg(dest, 'Quote: %s' % quote)
            except Exception as err:
                self.log.warning('Error while reading quote: %s' % err)
                self.irc.msg(dest, 'That quote doesn\'t exist in the database!')
        else:
            self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))

    # noinspection PyUnusedLocal,PyUnusedLocal
    def count_quotes(self, userinfo, dest, args):
        self.irc.sql.query('SELECT COUNT(*) FROM py_quotes WHERE qchan=?', (dest,))
        qtotal = self.irc.sql.fetch()
        self.irc.msg(dest, 'There are %i quotes in the database for this channel.' % qtotal)

