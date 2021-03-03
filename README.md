# **Acron Discord Bot**
* [Software](#required-software)
* [Settings](#settings)
* [Setup](#setup)
* [Usage](#usage)
* [Other](#other)
## **Required Software**
* Python 3.8+
* Discord.py `$ pip install discord`
* PyYAML `$ pip install pyyaml`
* Requests `$ pip install requests`

## **Settings**
### BOT_TOKEN
This is where you will put your bot token.
#### Make A Bot
1. Go to https://discord.com/developers/
2. Click **New Application**
3. Name it and give it a profile picture (If you want)
4. Click The **Bot** section (On the Left)
5. Press **Add bot** and then press **Yes, do it!**
6. Below the bot token, press **Copy**
7. Paste the token into SETTINGS.txt

### GAME_CHANNEL
The **ID** of the channel you want the games redirected to

### SQUIRREL_ROLE
The **ID** of the role to be pinged upon game creation

### TREE_ROLE
The **ID** of the role to be pinged when a tree ping succeeds

### PING_TIMEOUT
The length in minutes between pingable games (regardless of how many games are created)

## **Setup**
### Download & Run Locally
1. Clone/Download the files
2. Put them where you want on your computer
3. run SETUP.py
4. Put your settings into SETTINGS.txt
5. Run the Main bot with BOT.py

## **Usage**
### Commands

* `!game <code>`
  - ex. `!game 05 67 28`
* `!endgame`
  - ex. `!endgame`
* `!tree`
  - ex. `!tree`
* `!arank [<user>]`
  - ex. `!arank`

### Features
* Will not ping for a certain amount of time after the previous ping ([Timeout](#ping_timeout))
* Only pings a specific role ([Ping](#ping_role))
* Ends game automatically after 1 hour
* Ends games with 3 GG's within 5 minutes of each other (GAME CREATOR HAS TO SAY GG)
* MEE6 Rank API with custom rank commands
* Tree ping command to notify trees that 3 (or more) squirrels are available
* Send commands to send messages as the bot

## **Other**
I'm just a programming hobbyist that likes to make discord bots.
