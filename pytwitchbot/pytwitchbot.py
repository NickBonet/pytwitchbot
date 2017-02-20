import asyncio
from threading import Thread

from twisted.internet import ssl, reactor, protocol

from ircbotclient import IRCBotClient
from modules.core.logger import Logger
from pytwitchdiscord import DiscordBot

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
        # noinspection PyUnresolvedReferences
        reactor.stop()


if __name__ == '__main__':
    bot = IRCBotFactory()
    discordBot = DiscordBot(bot.protocol.get_discord_token(),
                            bot.protocol.get_discord_default_channel(),
                            bot.protocol.get_discord_default_twitch_channel())
    discordBot.set_irc_object(bot.protocol)
    bot.protocol.set_discord_object(discordBot)
    log.output("pyTwitchbot started.")
    # noinspection PyUnresolvedReferences
    if bot.protocol.get_use_ssl() == 1:
        # noinspection PyUnresolvedReferences
        reactor.connectSSL(bot.protocol.get_server(), bot.protocol.get_port(), bot, ssl.ClientContextFactory())
    else:
        reactor.connectTCP(bot.protocol.get_server(), bot.protocol.get_port(), bot)
    # noinspection PyUnresolvedReferences
    Thread(target=reactor.run, args=(False,)).start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(discordBot.run())
