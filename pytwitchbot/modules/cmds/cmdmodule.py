# Simple class for extending into a command module. ###
class CmdModule(object):
    def __init__(self, log, irc):
        # The logger object. ###
        self.log = log
        # IRC bot protocol instance. ###
        self.irc = irc
        # Dictionary which maps command names to their functions in a module,
        # as well as information on how to use the command
        self.cmd_dict = {}
        # Dictionary which maps IRC events to functions one may want to execute during said events when they occur
        self.hook_dict = {}
        # Defines whether the module is intended to work in channels only, private messages only, or both
        self.mod_type = ''
        # Defines what level of permission is required to run some or all commands in a module
        # The permission levels defined in order from lowest to highest are: Mod, BotOp, BotAdmin
        self.mod_perm_level = None

    def get_cmds(self):
        return self.cmd_dict

    def get_hooks(self):
        return self.hook_dict

    def get_perm_level(self):
        return self.mod_perm_level

    def get_mod_type(self):
        return self.mod_type
