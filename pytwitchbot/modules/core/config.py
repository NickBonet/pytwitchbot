#
# pyTwitchbot Config Module ###
# Author: K-Shadow   ###
#

import logging
from configparser import ConfigParser

# Loads and parses the configuration file for the bot. ###


class Config:
    def __init__(self):
        self.log = logging.getLogger('pyTwitchbot.config')
        self.conf = ConfigParser()
        self.file = 'pytwitchbot.conf'
        self.load_config()

    def load_config(self):
        try:
            self.conf.read(self.file)
        except Exception as err:
            self.log.warning('Error loading configuration file: %s' % err)

    def get_option(self, section, option):
        try:
            return self.conf.get(section, option)
        except Exception as err:
            self.log.warning("Can\'t read configuration option: %s" % err)

    def set_option(self, section, option, value):
        try:
            self.conf.set(section, option, value)
            with open(self.file, 'w+') as configfile:
                self.conf.write(configfile)

        except Exception as err:
            self.log.warning('Unable to set configuration option: %s' % err)

    def get_int(self, section, option):
        try:
            return self.conf.getint(section, option)
        except Exception as err:
            self.log.warning("Can\'t read configuration option: %s" % err)
