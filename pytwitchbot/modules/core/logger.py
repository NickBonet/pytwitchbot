#
# PyIRCBot Logger Module ###
# Author: K-Shadow    ###
#

from time import strftime, localtime


# Handles formatting output to console with timestamps. ###


class Logger:
    def __init__(self):
        pass

    def output(self, data):
        out = '[' + self.get_local_time + '] ' + data
        print(out)

    @property
    def get_local_time(self):
        return strftime('%a, %d %b %Y %X', localtime())
