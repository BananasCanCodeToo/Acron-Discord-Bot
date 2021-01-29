
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

@bot.event
async def on_message(message):
    x = datetime.datetime.now()
    msg = f"{message.content}"
    msglen = len(msg)
    botID = bot.user.id
    if message.author.id != botID:
        if msg[0] != '!':
            num = False
            code = ""
            attempt = 0
            for i in range(msglen):
                cde = ""
                if attempt > 0:
                    attempt += -1
                else:
                    try:
                        intTestI = int(msg[i])
                        for e in msg[i:]:
                            try:
                                intI = int(e)
                                cde += e
                            except:
                                if e == " ":
                                    continue
                                elif e != " ":
                                    num = False
                                    cde = ""
                            if len(cde) == 6:
                                code = cde
                                num = True
                                break
                    except:
                        if msg[i-1] + msg[i] == "<@":
                            attempt = 18
                        continue
                    if len(cde) == 6:
                        code = cde
                        num = True
                        break

            if num == True:
                print(f'[INFO] {datetime.datetime.now().strftime("%H:%M:%S")} > {message.author.name}#{message.author.discriminator} sent a raw code ({code})')
                with open('log.txt','a') as f:
                    f.write(f'\n[INFO] {x.strftime("%H:%M:%S")} > {message.author.name}#{message.author.discriminator} sent a raw code ({code})')
                await message.add_reaction(emoji="💬")

                with open('pgames.data','r') as f:
                    messages = json.load(f)
                messages[f'{message.author.id}'] = [message.id,f'{code}']
                with open('pgames.data','w+') as f:
                    json.dump(messages, f, indent=4)

        else:
            await bot.process_commands(message)
@bot.event
async def on_raw_reaction_add(payload):
    x = datetime.datetime.now()
    botID = bot.user.id
    with open('pgames.data','r') as f:
        messageIDs = json.load(f)
    for i,e in messageIDs.items():
        if e[0] == payload.message_id:
            if payload.member.id == int(i):
                if payload.member.id != botID:
                    with open('games.data','r') as f:
                        games = json.load(f)
                    game = False
                    # looks to see if this player already has a game
                    for i,e in games.items():
                        if i == f'{payload.member.id}':
                            game = True
                            break

                    if game == False:
                        user = payload.member
                        code = e[1]
                        with open('SETTINGS.txt','r') as f:
                            settings = yaml.load(f,Loader=yaml.FullLoader)
                            gChannel = settings['GAME_CHANNEL']
                        gameChannel = bot.get_channel(gChannel)
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
                                ping = bot.get_guild(payload.guild_id).get_role(settings['PING_ROLE']).mention
                        # Sends game code
                        e = discord.Embed(colour=discord.Color.orange(),title=f"**{code}**")
                        e.set_footer(text=f'{payload.member.name}#{payload.member.discriminator}',icon_url=f'{payload.member.avatar_url}')
                        message = await gameChannel.send(embed = e, content = f'{ping}')
                        await payload.member.send(f'Successfully started the game. Remember to use `!endgame` when you are done!')
                        print(f'[INFO] {x.strftime("%H:%M:%S")} > {payload.member.name}#{payload.member.discriminator} started game from reaction.')
                        with open('log.txt','a') as f:
                            f.write(f'\n[INFO] {x.strftime("%H:%M:%S")} > {payload.member.name}#{payload.member.discriminator} started game from reaction.')
                        with open('pgames.data','r') as f:
                            messages = json.load(f)
                        messages.pop(f'{payload.member.id}')
                        with open('pgames.data','w+') as f:
                            json.dump(messages, f, indent=4)
                        with open('games.data','r') as f:
                            games = json.load(f)
                        # Writes the game to the Game JSON file
                        with open('games.data','w') as f:
                            games[f'{payload.member.id}'] = [message.id,code]
                            json.dump(games, f, indent=4)
                    else:
                        await payload.member.send(f'{payload.member.mention}, You already have a game running. Use `!endgame` to mark your previous game as ended.\n*Un-react to the message then react again after you end your previous game.*')


# The command to start games
@bot.command()
async def game(ctx, *, code):
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
        e = discord.Embed(colour=discord.Color.orange(),title=f"**{code}**")
        e.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}',icon_url=f'{ctx.author.avatar_url}')
        message = await gameChannel.send(embed = e, content = f'{ping}')

        await ctx.author.send(f'Successfully started the game. Remember to use `!endgame` when you are done!')

        print(f'[INFO] {x.strftime("%H:%M:%S")} > {ctx.author.name}#{ctx.author.discriminator} Successfully started Game. Code: {code}')
        with open('log.txt','a') as f:
            f.write(f'\n[INFO] {x.strftime("%H:%M:%S")} > {ctx.author.name}#{ctx.author.discriminator} Successfully started Game. Code: {code}')

        with open('games.data','r') as f:
            games = json.load(f)
        # Writes the game to the Game JSON file
        with open('games.data','w') as f:
            games[f'{ctx.author.id}'] = [message.id,code]
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
        code = contents[1]

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
        e = discord.Embed(colour=discord.Color.red(),title="*ENDED*",description=f"**{code}**")
        e.set_footer(text=f'{ctx.author.name}#{ctx.author.discriminator}',icon_url=f'{ctx.author.avatar_url}')

        await message.edit(embed = e, content = '')
        await ctx.author.send('Your Game has been marked as ended.')

        # Logs the ending of a game
        print(f'[INFO] {x.strftime("%H:%M:%S")} > {ctx.author.name}#{ctx.author.discriminator} Has ended a game.')
        with open('log.txt','a') as f:
            f.write(f'\n[INFO] {x.strftime("%H:%M:%S")} > {ctx.author.name}#{ctx.author.discriminator} Has ended a game.')
    else:
        await ctx.author.send("You don't have a game running!")




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
