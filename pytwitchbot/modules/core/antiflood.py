import threading
import time


# Thread to handle resetting flood counter for users. ###
# noinspection PyAttributeOutsideInit
class BotAntiflood(threading.Thread):

    def run(self):
        while True:
            self.flood = {}
            time.sleep(20)
