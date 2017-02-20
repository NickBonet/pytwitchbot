#
# pyTwitchbot Logger Module ###
# Author: K-Shadow    ###
#

import logging

# Handles formatting output to console with timestamps. ###


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('pyTwitchbot')
        self.logger.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        file = logging.FileHandler('pytwitchbot.log')
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
        console.setLevel(logging.DEBUG)
        file.setLevel(logging.DEBUG)
        file.setFormatter(formatter)
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        self.logger.addHandler(file)

    def output(self, output):
        self.logger.info(output)

