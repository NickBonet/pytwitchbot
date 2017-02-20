import logging
import platform
from time import strftime, localtime

from twisted.internet import threads
from twisted.words.protocols import irc

from modules.cmdhandler import CmdHandler
from modules.core.antiflood import BotAntiflood
from modules.core.config import Config
from modules.core.sqlitedb import SQLiteDB
from modules.core.userpermission import UserPermission


# Handles IRC protocol/events for the bot. ###


class IRCBotClient(irc.IRCClient):
    conf = Config()
    nickname = conf.get_option('info', 'nickname')
    password = conf.get_option('info', 'serverpass')
    lineRate = None
    versionName = 'pyTwitchBot'
    versionNum = 'Dev'
    versionEnv = platform.system() + ' ' + platform.release()

    # Initialization for the class ###
    def __init__(self):
        self.channels = []
        self.log = logging.getLogger('pyTwitchbot.IRCBotClient')
        self.cmd_prefix = self.conf.get_option('modules', 'command_prefix')
        self.modhandler = CmdHandler(self)
        self.sql = SQLiteDB(self.conf)
        self.perms = UserPermission(self.sql, self.conf)
        self.bot_antiflood = BotAntiflood()
        self.bot_antiflood.setDaemon(True)

    # Processing tags in messages/processing Twitch IRCv3 commands such as WHISPER
    def lineReceived(self, line):
        line_str = line.decode('utf-8')
        # self.log.debug(line_str)
        if line_str.startswith('@'):
            tags = line_str[1:].split(':')[0].split(' ')[0].split(';')
            tags = dict(t.split('=') for t in tags)
            line_str = ':' + line_str.split(' :', 1)[1]
            # noinspection PyTypeChecker
            prefix, cmd, args = irc.parsemsg(line_str)
            if cmd == "PRIVMSG":
                self.privmsg(prefix, args[0], args[1], tags)
            elif cmd == "WHISPER":
                self.privmsg(prefix, args[0], args[1], tags)
            # TODO: Don't have much need to process these for the moment, will just log for now
            elif cmd == "USERSTATE":
                self.log.info('USERSTATE: %s' % str(tags))
            elif cmd == "ROOMSTATE":
                self.log.info('ROOMSTATE: %s' % str(tags))
            elif cmd == "USERNOTICE":
                if len(args) == 2:
                    self.log.info('User %s has resubscribed to the channel!: %s' % (tags['login'], args[1]))
                else:
                    self.log.info('User %s has resubscribed to the channel!' % tags['login'])
            elif cmd == "HOSTTARGET":
                if args[1].split(' ')[0] == "-":
                    self.log.info('Exited host mode in %s.' % args[0])
                else:
                    self.log.info('%s now hosting %s with %s viewers.' % (args[0], args[1], args[2]))
            elif cmd == "CLEARCHAT":
                if len(args) == 1:
                    self.log.info('Chat has been cleared in %s!' % args[0])
                elif len(args) == 2:
                    self.log.info('User %s has been banned from the chat.' % args[1])
            elif cmd == "RECONNECT":
                # TODO: Implement logic to reconnect and rejoin eventually
                self.log.warning('Received reconnect notice from the Twitch server!')
            elif cmd == "NOTICE":
                pass
        else:
            irc.IRCClient.lineReceived(self, line)

    # Twitch support - Request Membership/Tags/Commands capabilities
    def signedOn(self):
        self.sendLine('CAP REQ :twitch.tv/membership')
        self.sendLine('CAP REQ :twitch.tv/tags')
        self.sendLine('CAP REQ :twitch.tv/commands')
        irc.IRCClient.signedOn(self)

    # Loads channels from configuration and joins them. ###
    def load_channels(self):
        confchannels = self.conf.get_option('server', 'channels')
        confchannels = confchannels.split(',')

        for channel in confchannels:
            self.join(channel)

    # Saves the current channels the bot is currently in. ###
    def save_channels(self):
        channellist = ','.join(self.channels)
        self.conf.set_option('server', 'channels', channellist)

    # Loads modules in autoload list in the configuration file. ###
    def load_mods(self):
        modulelist = self.conf.get_option('modules', 'autoload')
        modulelist = modulelist.split(',')

        for module in modulelist:
            self.modhandler.load_cmd_module(module)

    # Returns the address of the IRC server from configuration. ###
    def get_server(self):
        return self.conf.get_option('server', 'address')

    # Returns the port of the IRC server from configuration. ###
    def get_port(self):
        return self.conf.get_int('server', 'port')

    # When the MOTD is received, we assume it's safe to start joining
    # channels. ###
    def receivedMOTD(self, motd):
        self.load_mods()
        self.perms.load_bot_master()
        self.perms.load_users()
        self.load_channels()
        self.bot_antiflood.start()

    # Overrides the join method in the IRCClient class of Twisted, only
    # difference is that it prints the channel it joined. ###
    def join(self, channel, key=None):
        if channel not in self.channels:
            irc.IRCClient.join(self, channel, key)
            self.log.info('Joined %s.' % channel)
            self.channels.append(channel)
            self.save_channels()
        else:
            return

    # Overrides the leave method in the IRCClient class of Twisted ###
    def leave(self, channel, reason=None):
        if channel in self.channels:
            irc.IRCClient.leave(self, channel, reason)
            self.log.info('Left %s.' % channel)
            self.channels.remove(channel)
            self.save_channels()
        else:
            return

    # Handles messages from channels/users. ###
    def privmsg(self, user, channel, message, tags=None):
        usernick = user.split('!')[0]
        userident = user.split('!')[1].split('@')[0]
        userhost = user.split('@')[1]
        userinfo = [usernick, userident, userhost]
        args = message.split(' ')

        if args[0] in self.modhandler.commands or self.modhandler.privcmds:
            if usernick not in self.bot_antiflood.flood:
                self.bot_antiflood.flood.update({usernick: []})
                self.bot_antiflood.flood[usernick] = 0

            self.bot_antiflood.flood[usernick] += 1

            if self.bot_antiflood.flood[usernick] < 7:
                if args[0] in self.modhandler.privcmds and not channel.startswith('#'):
                    cmd = self.modhandler.privcmds[args[0]]
                    threads.deferToThread(cmd['function'], userinfo, userinfo[0], args)
                elif args[0] in self.modhandler.commands:
                    if channel.startswith('#'):
                        cmd = self.modhandler.commands[args[0]]
                        threads.deferToThread(cmd['function'], userinfo, channel, args)
            else:
                return

    # Minor edit of the msg method in twisted. IRC class
    def msg(self, user, message, length=None):
        if not user.startswith('#'):
            fmt = 'PRIVMSG #jtv :/w %s ' % user
        else:
            fmt = 'PRIVMSG %s :' % (user,)

        if length is None:
            length = self._safeMaximumLineLength(fmt)

        # Account for the line terminator.
        minimum_length = len(fmt) + 2
        if length <= minimum_length:
            raise ValueError("Maximum length must exceed %d for message "
                             "to %s" % (minimum_length, user))
        for line in irc.split(message, length - minimum_length):
            self.sendLine(fmt + line)

    # Handles join events on IRC.
    # prefix - The info of the user joining the channel.
    # params - The channel being joined. ###
    def irc_JOIN(self, prefix, params):
        if prefix.split('!')[0] != self.nickname:
            self.modhandler.call_hook('join', prefix, params)

    # Handles part events on IRC.
    # prefix - The info of the user parting the channel.
    # params - The channel being parted. ###
    def irc_PART(self, prefix, params):
        if prefix.split('!')[0] != self.nickname:
            self.modhandler.call_hook('part', prefix, params)

    # Handles quit events on IRC.
    # prefix - The info of the user quitting.
    # params - The quit reason. ###
    def irc_QUIT(self, prefix, params):
        if prefix.split('!')[0] != self.nickname:
            self.modhandler.call_hook('quit', prefix, params)

    @property
    def get_local_time(self):
        return strftime('%a, %d %b %Y %X', localtime())

    def rawDataReceived(self, data):
        pass

    def dccSend(self, user, file):
        pass
