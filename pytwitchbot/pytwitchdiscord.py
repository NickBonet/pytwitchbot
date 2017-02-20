import asyncio
import logging

import discord

client = discord.Client()
irc = None
default_channel = None
twitch_relay_channel = None
log = logging.getLogger('pyTwitchbot.Discord')


class DiscordBot(object):

    def __init__(self, token, channel, twitchrelay):
        global default_channel
        global twitch_relay_channel
        self.token = token
        default_channel = channel
        twitch_relay_channel = twitchrelay

    # noinspection PyMethodMayBeStatic
    def set_irc_object(self, ircobj):
        global irc
        irc = ircobj

    def run(self):
        global client
        client.run(self.token)

    # noinspection PyMethodMayBeStatic
    def send_to_discord(self, message):
        global client
        asyncio.run_coroutine_threadsafe(async_send(message), client.loop)


# noinspection PyUnresolvedReferences
async def async_send(message):
    await client.send_message(client.get_channel(default_channel), message.strip())


@client.event
async def on_ready():
    log.info('Logged into Discord as: %s' % client.user.name)


# noinspection PyUnresolvedReferences
@client.event
async def on_message(message):
    if message.content.startswith('.help'):
        await client.send_message(message.channel, 'I don\'t currently have any commands implemented.')
    elif message.author.display_name != client.user.name:
        irc.msg(twitch_relay_channel, '[Discord] %s: %s' % (message.author.display_name, message.content))

