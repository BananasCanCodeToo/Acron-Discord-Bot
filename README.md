# **Acron Discord Bot**
* [Software](#required-software)
* [Settings](#settings)
* [Setup](#setup)
* [Usage](#usage)
## Required Software
* Python 3.8
* Discord.py `$ pip install discord`
* PyYAML     `$ pip install pyyaml`

## Settings
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

### PING_ROLE
The **ID** of the role to be pinged upon game creation

### PING_TIMEOUT
The length in minutes between pingable games (regardless of how many games are created)

## Setup
### Download & Run Locally 
1. Clone/Download the files
2. Put them where you want on your computer
3. run SETUP.py
4. Put your settings into SETTINGS.txt
5. Run the Main bot with BOT.py
### Run on Heroku
*Template coming Soon*

## Usage
### Commands
- !game <code>
  - !game 05 67 28
- !endgame
  - !endgame

### Features
- Will not ping for a certain amount of time after the previous ping ([Timeout](#ping_timeout))
- Only pings a specific role ([Ping](#ping_role))
- Deletes game commands for games if they haven't ended their previous game
