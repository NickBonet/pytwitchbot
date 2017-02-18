import sys


# Handles loading/unloading command modules. ###


class CmdHandler:
    def __init__(self, log, irc):
        self.log = log
        self.irc = irc
        self.commands = {}
        self.privcmds = {}
        self.hooks = {}
        self.modules = {}

    # Adds a hook to be called for a specified event to the module
    # handler's dictionary of hooks.
    def add_hook(self, hookname, hookfunc):
        if hookname not in self.hooks:
            self.hooks.update({hookname: []})
        self.hooks[hookname].append(hookfunc)

    # Adds a command to the module handler's dictionary of commands. ###
    def add_pub_cmd(self, cmd, cmdfunc):
        if cmd not in self.commands:
            self.commands.update({cmd: cmdfunc})

    # Adds a command to the module handler's dictonary of commands for private
    # messages. ###
    def add_priv_cmd(self, cmd, cmdfunc):
        if cmd not in self.privcmds:
            self.privcmds.update({cmd: cmdfunc})

    # Calls all possible hooks for an IRC event. ###
    def call_hook(self, hook, prefix, params):
        if hook not in self.hooks:
            return False

        for function in self.hooks[hook]:
            function(prefix, params)

    # Loads a command module and adds its commands to the module handler's
    # dictionary. ###
    def load_cmd_module(self, module):
        # Checks if module is already loaded. ###
        if module in self.modules:
            self.log.output('Command module %s is already loaded.' % module)
            return False

        # If not, try to load the module! ###
        try:
            # Module is being imported and initiated. ###
            modname = 'cmd_' + module
            # noinspection PyUnusedLocal
            mod = __import__("modules.cmds." + modname)
            mod = eval("mod.cmds." + modname)
            modinstance = getattr(
                mod, 'CmdModule' + module.capitalize())(self.log, self.irc)

            # The instance of the module is stored in a
            # dictionary. ###
            self.modules[module] = modinstance

            # Module commands are iterated and added to dictionary of
            # commands. ###
            for cmdname, cmdfunc in modinstance.get_cmds().items():
                if modinstance.get_mod_type() == 'priv':
                    self.add_priv_cmd(cmdname, cmdfunc)
                elif modinstance.get_mod_type() == 'chan':
                    self.add_pub_cmd(cmdname, cmdfunc)
                elif modinstance.get_mod_type() == 'all':
                    self.add_priv_cmd(cmdname, cmdfunc)
                    self.add_pub_cmd(cmdname, cmdfunc)

            # Module hooks are iterated and added to dictionary of
            # hooks. ###
            for hookname, hookfunc in modinstance.get_hooks().items():
                self.add_hook(hookname, hookfunc)

            self.log.output('Loaded %s module.' % module)
            return True

        except Exception as err:
            self.log.output('Error loading %s module: %s' % (module, err))
            return False

    # Unloads a command module and its commands. ###
    def unload_cmd_module(self, module):
        # Checks if module is even loaded. ###
        if module not in self.modules:
            self.log.output('Module %s is not loaded.' % (str(module)))
            return False

        # Gets the instance of the loaded module. ###
        modinstance = self.modules[module]

        try:
            # The module's commands are iterated and unloaded. ###
            for cmdname, cmdfunc in modinstance.get_cmds().items():
                if modinstance.get_mod_type().lower() == 'priv':
                    del self.privcmds[cmdname]
                elif modinstance.get_mod_type().lower() == 'chan':
                    del self.commands[cmdname]

            # The module's hooks are iterated and unloaded. ###
            for hookname, hookfunc in modinstance.get_hooks().items():
                self.hooks[hookname].remove(hookfunc)

            # The module is unloaded, and the module instance
            # is removed from the module handler's dictionary. ###
            sys.modules.pop('modules.cmds.cmd_' + module)
            self.log.output('Module %s has been unloaded.' % module)
            del self.modules[module]
            return True

        except Exception as err:
            self.log.output('Error unloading module %s: %s' % (module, err))
            return False

    # Simple way to reload modules. ###
    def reload_cmd_module(self, module):
        try:
            self.unload_cmd_module(module)
            self.load_cmd_module(module)
            return True
        except Exception as err:
            self.log.output('Error while reloading %s module: %s' % (module, err))
            return False
