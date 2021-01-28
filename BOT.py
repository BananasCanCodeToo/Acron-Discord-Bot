
# importing all needed libraries
import discord
import datetime
import json
import pickle
import yaml
from discord.ext import commands, tasks
from discord import Embed
from datetime import timedelta


# Registering the bot with a prefix
bot = commands.Bot(command_prefix = '!')

# The command to start games
@bot.command()
async def game(ctx, c1, c2, c3):
    # Finds the date and finds the specified game channel
    x = datetime.datetime.now()
    with open('SETTINGS.txt','r') as f:
        settings = yaml.load(f,Loader=yaml.FullLoader)
        gChannel = settings['GAME_CHANNEL']
    gameChannel = bot.get_channel(gChannel)

    # Logs the the ATTEMPT activation of a game in the log files
    print(f'[INFO] {x.strftime("%H:%M:%S")} > {ctx.author.name}#{ctx.author.discriminator} Attempted to start game.')
    with open('log.txt','a') as f:
        f.write(f'\n[INFO] {x.strftime("%H:%M:%S")} > {ctx.author.name}#{ctx.author.discriminator} Attempted to start game.')


    with open('games.data','r') as f:
        games = json.load(f)
    game = False

    # looks to see if this player already has a game
    for i,e in games.items():
        if i == f'{ctx.author.id}':
            game = True
            break

    if game == False:
        # Processes ping timeout to see if it can ping
        currentPing = x
        ping = ''
        with open('ping.data','rb') as f:
            pastPing = pickle.load(f)

        with open('SETTINGS.txt','r') as f:
            settings = yaml.load(f,Loader=yaml.FullLoader)
            timeout = settings['PING_TIMEOUT']

        if currentPing > pastPing + timedelta(minutes=timeout):
            with open('ping.data','wb') as f:
                pickle.dump(currentPing, f)
                ping = ctx.guild.get_role(settings['PING_ROLE']).mention

        # Sends game code
        e = discord.Embed(colour=discord.Color.orange(),title=f"**{c1} {c2} {c3}**")
        e.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}',icon_url=f'{ctx.author.avatar_url}')
        message = await gameChannel.send(embed = e, content = f'{ping}')

        await ctx.author.send(f'Successfully started the game. Remember to use `!endgame` when you are done!')

        # Logs the successful start of a game
        print(f'[INFO] {x.strftime("%H:%M:%S")} > {ctx.author.name}#{ctx.author.discriminator} Successfully started Game. Code: {c1} {c2} {c3}')
        with open('log.txt','a') as f:
            f.write(f'\n[INFO] {x.strftime("%H:%M:%S")} > {ctx.author.name}#{ctx.author.discriminator} Successfully started Game. Code: {c1} {c2} {c3}')

        # Writes the game to the Game JSON file
        with open('games.data','w') as f:
            games[f'{ctx.author.id}'] = [message.id,c1,c2,c3]
            json.dump(games, f, indent=4)
    else:
        await ctx.channel.purge(limit=1)
        await ctx.author.send(f'{ctx.author.mention}, You already have a game running. Use `!endgame` to mark your previous game as ended.')

# Command to end the game
@bot.command()
async def endgame(ctx):
    x = datetime.datetime.now()

    # Opens game file to find message ID and game code
    with open('games.data','r') as f:
        games = json.load(f)

    game = False
    for i,e in games.items():
        if i == f'{ctx.author.id}':
            game = True

    # Gets the message ID and game code
    if game == True:
        contents = games[f'{ctx.author.id}']
        messageID = contents[0]
        c1 = contents[1]
        c2 = contents[2]
        c3 = contents[3]

        # Removes game from games.json
        games.pop(f'{ctx.author.id}')
        with open('games.data','w') as f:
            json.dump(games, f, indent=4)

        # Gets the message from the ID
        with open('SETTINGS.txt','r') as f:
            settings = yaml.load(f,Loader=yaml.FullLoader)
            gChannel = settings['GAME_CHANNEL']
        channel = bot.get_channel(gChannel)
        message = await channel.fetch_message(int(messageID))

        # Edits the embed to say the game has ended
        e = discord.Embed(colour=discord.Color.red(),title=f"**{c1} {c2} {c3}** *ENDED*")
        e.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}',icon_url=f'{ctx.author.avatar_url}')
        await message.edit(embed = e, content = '')
        await ctx.author.send('Your Game has been marked as ended.')

        # Logs the ending of a game
        print(f'[INFO] {x.strftime("%H:%M:%S")} > {ctx.author.name}#{ctx.author.discriminator} Has ended a game.')
        with open('log.txt','a') as f:
            f.write(f'\n[INFO] {x.strftime("%H:%M:%S")} > {ctx.author.name}#{ctx.author.discriminator} Has ended a game.')








# Configures the Bot on startup
@bot.event
async def on_ready():
    x = datetime.datetime.now()
    # Prints the log
    print(f'[INFO] {x.strftime("%H:%M:%S")} > Bot is Online')
    with open('log.txt','a') as f:
        f.write(f'\n\n\n\n[DATE] {x.strftime("%Y.%m.%d")}\n[INFO] {x.strftime("%H:%M:%S")} > Bot is Online')


# BOT TOKEN TO RUN!!!! DO NOT SHARE!!!!
with open('SETTINGS.txt','r') as f:
    settings = yaml.load(f,Loader=yaml.FullLoader)
    botToken = settings['BOT_TOKEN']
bot.run(botToken)

#########################################
#    Developed by BananasCanCodeToo     #
# https://github.com/BananasCanCodeToo/ #
#########################################
