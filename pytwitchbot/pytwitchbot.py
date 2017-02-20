from twisted.internet import reactor, protocol

from ircbotclient import IRCBotClient
from modules.core.logger import Logger

log = Logger()


# Creates an instance of the protocol. ###
class IRCBotFactory(protocol.ClientFactory):
    def __init__(self):
        self.protocol = IRCBotClient()

    def buildProtocol(self, addr):
        return self.protocol

    # If the connection to the server is lost, reconnect! ###
    def clientConnectionLost(self, connector, reason):
        connector.connect()

    # If the connection fails, stop the reactor. ###
    def clientConnectionFailed(self, connector, reason):
        reactor.stop()


if __name__ == '__main__':
    bot = IRCBotFactory()
    log.output("pyTwitchbot started.")
    reactor.connectTCP(bot.protocol.get_server(), bot.protocol.get_port(), bot)
    reactor.run()
