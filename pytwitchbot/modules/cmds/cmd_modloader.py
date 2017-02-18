from modules.cmds.cmdmodule import CmdModule


# Module for loading other command modules for the bot. ###


class CmdModuleModloader(CmdModule):
    def __init__(self, log, irc):
        super().__init__(log, irc)
        self.cmd_dict = {
            'loadmod': {'function': self.load_mod, 'help':
                        'loadmod <module> - Loads a module.'},
            'unloadmod': {'function': self.unload_mod, 'help':
                          'unloadmod <module> - Unloads a module.'},
            'reloadmod': {'function': self.reload_mod, 'help':
                          'reloadmod <module> - Reloads a module.'},
            'rehash': {'function': self.reload_conf, 'help': 'rehash - Reloads the configuration file.'}}
        self.mod_perm_level = 3
        self.mod_type = 'all'

    def load_mod(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo[0], self.get_perm_level()):
            if len(args) > 1 and args[1] != '':
                if self.irc.modhandler.load_cmd_module(args[1]):
                    self.irc.msg(dest, 'Loaded %s module.' % (args[1]))
                else:
                    self.irc.msg(dest, 'Unable to load %s module.' % (args[1]))
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(
                dest, 'You don\'t have permission to run that command!')

    def unload_mod(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo[0], self.get_perm_level()):
            if len(args) > 1 and args[1] != '':
                if self.irc.modhandler.unload_cmd_module(args[1]):
                    self.irc.msg(dest, 'Unloaded %s module.' % (args[1]))
                else:
                    self.irc.msg(
                        dest, 'Error unloading %s module.' % (args[1]))
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(
                dest, 'You don\'t have permission to run that command!')

    def reload_mod(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo[0], self.get_perm_level()):
            if len(args) > 1 and args[1] != '':
                if self.irc.modhandler.reload_cmd_module(args[1]):
                    self.irc.msg(dest, 'Reloaded %s module.' % (args[1]))
                else:
                    self.irc.msg(
                        dest, 'Error reloading %s module.' % (args[1]))
            else:
                self.irc.msg(dest, self.irc.modhandler.get_help_text(args[0], self.mod_type))
        else:
            self.irc.msg(
                dest, 'You don\'t have permission to run that command!')

    def reload_conf(self, userinfo, dest, args):
        if self.irc.perms.check_perm(userinfo[0], self.get_perm_level()):
            self.irc.conf.load_config()
            self.irc.msg(dest, 'Reloaded configuration file.')
        else:
            self.irc.msg(
                dest, 'You don\'t have permission to run that command!')

