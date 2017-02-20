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

[github]
user = test
pass = test
```


