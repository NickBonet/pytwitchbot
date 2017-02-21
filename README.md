# pytwitchbot
pyTwitchbot is a (work in progress) Twitch chat bot written in Python using the Twisted framework. pyTwitchbot is based off of one of my older projects, py-ircbot, 
which has been adapted to connect to Twitch's IRC to provide modular chat bot functionality to a stream's chat. pyTwitchbot also currently has experimental Discord support to interface between Twitch chat and Discord chat, 
creating even more possibilities in terms of modules and functionality.

# License
pyTwitchbot is licensed under the MIT license.
- https://opensource.org/licenses/MIT

# Dependencies
In order to utilize the bot, the following are required:

- Python 3.x (developed under 3.6 currently)
- Twisted
- discord.py
- pyOpenSSL
- PyGithub (optional, for github module)

After all of the dependencies are installed:
- Copy the example configuration below and save it as pytwitchbot.py in the pytwitchbot folder (same folder as pytwitchbot.py)
- Setup the config file to your liking, then simply launch the bot by executing pytwitchbot.py!

# Example configuration file

```
[server]
address = irc.chat.twitch.tv
port = 6697 # Use port 6697 for SSL, 6667 for regular connections
channels = #twitch_channel
use_ssl = 1

[info]
nickname = pystreambot
serverpass = twitch_ouath_token

[botmaster]
nick = test
pass = test

[modules]
command_prefix = !
autoload = modloader,join,quotes,help,facts,usermanage

[sqlite]
database = pytwitchbot.db

[discord]
token = discord_oauth_token
default_discord_channel = discord_channel_id
default_twitch_relay_channel = #twitch_channel

[github]
user = test
pass = test
```


