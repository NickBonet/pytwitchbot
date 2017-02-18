from modules.cmds.cmdmodule import *


# Module to display help information for a specified command. ###


class CmdModuleHelp(CmdModule):
    def __init__(self, log, irc):
        super().__init__(log, irc)
        self.mod_type = 'all'
        self.cmd_dict = {'!help': {'function': self.help_cmd, 'help':
                         '!help <command> - Shows help for a specified command.'}}

    def help_cmd(self, userinfo, dest, args):
        if len(args) > 1 and args[1] != '':
            if args[1] in self.irc.modhandler.commands:
                cmd = self.irc.modhandler.commands[args[1]]
                self.irc.msg(dest, cmd['help'])
            elif args[1] in self.irc.modhandler.privcmds and not dest.startswith('#'):
                cmd = self.irc.modhandler.privcmds[args[1]]
                self.irc.msg(dest, cmd['help'])
            else:
                self.irc.msg(dest, 'Help for that command wasn\'t found.')
        else:
            self.irc.msg(dest, self.cmd_dict[args[0]]['help'])

    def get_cmds(self):
        return self.cmd_dict
