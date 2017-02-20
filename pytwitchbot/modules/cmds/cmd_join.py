from modules.cmds.cmdmodule import CmdModule


# Module to manage the channels the bot is in. ###


class CmdModuleJoin(CmdModule):
    def __init__(self, log, irc):
        super().__init__(log, irc)
        self.cmd_dict = {
            'join': {'function': self.join_chan_cmd, 'help':
                     'join <stream_channel> - Makes the bot join a different stream\'s chat.'},
            'part': {'function': self.part_chan_cmd, 'help':
                     'part <stream_channel> - Makes the bot leave a different stream\'s chat.'}}
        self.hook_dict = {}
        self.mod_perm_level = 'BotOp'
        self.mod_type = 'chan'

    def greet_nn_join(self, prefix, params):
        self.irc.msg(params[0], 'Hello %s, welcome to the stream! Enjoy your stay.' % prefix.split('!')[0])

    def join_chan_cmd(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo, self.get_perm_level()):
            if len(args) > 1 and args[1] != '':
                if '#' + args[1] not in self.irc.channels:
                    self.irc.msg(dest, 'Joining channel %s.' % args[1])
                    self.irc.join('#' + args[1])
                else:
                    self.irc.msg(dest, 'I\'m already in that channel!')
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(dest, 'You don\'t have permission to run that command!')

    def part_chan_cmd(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo, self.get_perm_level()):
            if len(args) > 1 and args[1] != '':
                if '#' + args[1] in self.irc.channels:
                    self.irc.msg(dest, 'Parting channel %s.' % args[1])
                    self.irc.leave('#' + args[1])
                else:
                    self.irc.msg(dest, 'I\'m not in that channel!')
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(dest, 'You don\'t have permission to run that command!')

