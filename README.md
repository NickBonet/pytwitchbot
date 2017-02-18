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
username = pystreambot
realname = pystreambot
serverpass = oauth:goeshere

[botmaster]
nick = kshad98
ident = kshad98
host = *
pass = test

[modules]
autoload = modloader,join,quotes,help,facts,usermanage

[mysql]
host = 127.0.0.1
port = 3311
user = root
pass = root
database = pyircbot

[github]
user = test
pass = test
```


