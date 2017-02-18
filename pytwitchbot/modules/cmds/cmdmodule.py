# Simple class for extending into a command module. ###
class CmdModule(object):
    def __init__(self, log, irc):
        # The logger object. ###
        self.log = log
        # IRC bot protocol instance. ###
        self.irc = irc
        self.cmd_dict = {}
        self.hook_dict = {}
        self.mod_type = ''
        self.mod_perm_level = None

    # The list of commands and the functions they bind to. ###
    def get_cmds(self):
        return self.cmd_dict

    # Optional, allow your module to hook
    # to other IRC events, such as joins, quits, etc. ###
    def get_hooks(self):
        return self.hook_dict

    def get_perm_level(self):
        return self.mod_perm_level

    def get_mod_type(self):
        return self.mod_type
