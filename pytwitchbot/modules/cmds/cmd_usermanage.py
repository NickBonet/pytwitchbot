import hashlib

from modules.cmds.cmdmodule import CmdModule


# Module to manage adding and removing users. ###


class CmdModuleUsermanage(CmdModule):
    def __init__(self, log, irc):
        super().__init__(log, irc)
        self.ranklist = ""
        for x in self.irc.perms.levels:
            self.ranklist = x + " " + self.ranklist
        self.cmd_dict = {
            'adduser': {'function': self.add_user_cmd, 'help':
                        'adduser <nick> <password> <rank> - '
                        'Adds a user to the database. Ranks available for use are: %s' % self.ranklist},
            'deluser': {'function': self.del_user_cmd, 'help': 'deluser <nick> - Deletes a user from the database.'}}
        self.mod_perm_level = 'BotAdmin'
        self.mod_type = 'priv'

    def add_user_cmd(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo, self.get_perm_level()):
            if len(args) > 3:
                user_host = args[1] + '.tmi.twitch.tv'
                new_user = [args[1], args[1], user_host]
                passwd = hashlib.sha1(str(args[2]).encode('utf-8')).hexdigest()
                level = args[3]
                try:
                    if int(self.irc.perms.levels[level]) < self.irc.perms.get_user_level(userinfo[0]):
                        if self.irc.perms.check_user_exists(args[1]) is False:
                            if self.irc.perms.add_user(new_user, passwd, level):
                                self.irc.msg(dest, "User added!")
                            else:
                                self.irc.msg(dest, 'Error adding user to the database.')
                        else:
                            self.irc.msg(dest, 'A user with that nickname already exists in the database.')
                    else:
                        self.irc.msg(dest, 'Can\'t add a user with higher or equal permissions as you.')
                except Exception as err:
                    self.log.warning('Error while attempting to add user to the database: %s' % err)
                    self.irc.msg(dest, 'Error adding user to the database.')
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(dest, 'You don\'t have permission to run that command!')

    def del_user_cmd(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo, self.get_perm_level()):
            if len(args) > 1 and args[1] != '':
                user = args[1]
                if self.irc.perms.check_user_exists(user):
                    if self.irc.perms.get_user_level(user) < self.irc.perms.get_user_level(userinfo[0]):
                        if self.irc.perms.del_user(user):
                            self.irc.msg(dest, 'User deleted!')
                        else:
                            self.irc.msg(dest, 'Unable to delete user from the database.')
                    else:
                        self.irc.msg(dest, 'Can\'t delete a user who has higher or equal permissions as you.')
                else:
                    self.irc.msg(dest, 'That user doesn\'t exist in the database.')

            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(dest, 'You don\'t have permission to run that command!')

