# pytwitchbot
A Twitch chat IRC bot, written in Python 3.x, utilizing the Twisted framework. Based off of one of my other projects, py-ircbot.
README to be updated shortly.

# Example configuration file for bot (save as pytwitchbot.conf in pytwitchbot folder)

```
[server]
address = irc.chat.twitch.tv
port = 6667
channels = #twitch_channel

[info]
nickname = pystreambot
serverpass = oauth:goeshere

[botmaster]
nick = test
pass = test

[modules]
command_prefix = !
autoload = modloader,join,quotes,help,facts,usermanage

[sqlite]
database = pytwitchbot.db

[discord]
token = discord_ouath_token
default_discord_channel = discord_channel_id
default_twitch_relay_channel = #twitch_channel

[github]
user = test
pass = test
```


