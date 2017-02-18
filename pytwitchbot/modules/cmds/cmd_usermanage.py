import hashlib

from modules.cmds.cmdmodule import CmdModule


# Module to manage adding and removing users. ###


class CmdModuleUsermanage(CmdModule):
    def __init__(self, log, irc):
        super().__init__(log, irc)
        self.cmd_dict = {
            '!adduser': {'function': self.add_user_cmd, 'help':
                         '!adduser <nick> <ident> <hostmask> <password> <rank> - Adds a user to the database.'},
            '!deluser': {'function': self.del_user_cmd, 'help': '!deluser <nick> - Deletes a user from the database.'}}
        self.mod_perm_level = 3
        self.mod_type = 'priv'

    def add_user_cmd(self, userinfo, dest, args):
        if self.irc.perms.check_perm(dest, self.get_perm_level()):
            if len(args) > 5:
                userinfo = [args[1], args[2], args[3]]
                passwd = hashlib.sha1(str(args[4]).encode('utf-8')).hexdigest()
                level = int(args[5])
                if self.irc.perms.add_user(userinfo, passwd, level):
                    self.irc.msg(dest, "User added!")
                else:
                    self.irc.msg(dest, 'Unable to add user.')
            else:
                self.irc.msg(dest, self.cmd_dict[args[0]]['help'])
        else:
            self.irc.msg(
                dest, 'You don\'t have permission to run that command!')

    def del_user_cmd(self, userinfo, dest, args):
        if self.irc.perms.check_perm(dest, self.get_perm_level()):
            if len(args) > 1 and args[1] != '':
                user = args[1]
                if self.irc.perms.del_user(user):
                    self.irc.msg(dest, 'User deleted!')
                else:
                    self.irc.msg(dest, 'Unable to delete user.')
            else:
                self.irc.msg(dest, self.cmd_dict[args[0]]['help'])
        else:
            self.irc.msg(
                dest, 'You don\'t have permission to run that command!')

    def get_cmds(self):
        return self.cmd_dict
