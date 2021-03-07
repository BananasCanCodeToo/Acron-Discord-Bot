# importing all needed libraries
import discord
import datetime
import json
import pickle
import yaml
import requests
import random
from discord.ext import commands, tasks
from discord import Embed, Member
from datetime import timedelta
from itertools import cycle
import things.UTILITIES as utl
import things.BOTUTL as butl

# Registering the bot with a prefix
intents = discord.Intents().all()
bot = commands.Bot(command_prefix = '!',intents=intents)
bot.remove_command('help')
bot_presence = cycle([discord.Activity(type=discord.ActivityType.listening, name='Game Codes without the !game command'),discord.Game(name="Acron: Attack of the Squirrels"),discord.Activity(type=discord.ActivityType.watching, name="Squirrels Stealing Acorns")])

@tasks.loop(seconds=20)
async def Loop():
    await bot.change_presence(status=discord.Status.online, activity=next(bot_presence))
    x = datetime.datetime.now()
    gamesLoop = utl.r_games()
    newGames = utl.r_games()
    for i,e in gamesLoop.items():
        gTime = datetime.datetime.strptime(e[2], "%Y.%m.%d.%H:%M:%S")
        if x >= gTime + timedelta(hours=1):
            user = await bot.fetch_user(int(i))
            if await butl.endgame(user, bot):
                await user.send('Your Game has automatically been marked as ended. (2 Hours have passed)')
                utl.log(f'Ended a game [TIMEOUT]',user)



@bot.event
async def on_message(message):
    x = datetime.datetime.now()
    msg = f"{message.content}"
    msglen = len(msg)
    botID = bot.user.id

    CTN = True

    if msg == '':
        CTN = False
    elif msg[0] == '!':
        CTN = False
    elif message.author.bot:
        CTN = False
    elif "https://" in message.content:
        CTN = False
    elif "http://" in message.content:
        CTN = False
    elif "ban this guy" in message.content.lower():
        # Replies to "ban this guy" with "ban this guy"
        await message.channel.send('ban this guy')
        CTN = False
    # Detects if user is a bot or nto (continues if not a bot)
    if CTN:
        num = False
        code = ""
        attempt = 0
        emojiTest = False
        # Goes through the message to detect a game code
        for i in range(msglen):
            cde = ""
            if emojiTest == True:
                if msg[i] == ':':
                    emojiTest = False
            elif attempt > 0:
                attempt += -1
            else:
                for e in msg[i:]:
                    if e.isdigit():
                        cde += e
                    elif e == " ":
                        continue
                    elif e != " ":
                        if len(cde) == 6:
                            code = cde
                            num = True
                        else:
                            num = False
                            cde = ""
                        break
                    else:
                        try:
                            if msg[i-1] + msg[i] == "<@":
                                attempt += 19
                            if msg[i-1] + msg[i] == "<#":
                                attempt += 19
                            if msg[i-2] + msg[i-1] == "<:":
                                emojiTest = True
                                attempt += 19
                            continue
                        except IndexError:
                            continue
                    # Accepts code if it is 6 characters but ignores if 7
                    if len(cde) == 6:
                        code = cde
                        num = True
                    if len(cde) == 7:
                        num = False
                        code = ''
                        attempt += 6
                    elif len(cde) > 7:
                        attempt += 1
                        num = False
                        code = ''

                if len(cde) == 6:
                    code = cde
                    num = True
                    break

        if num == True:
            botID = bot.user.id
            if message.author.id != botID:
                # If it is a game code, sends message to user saying "hey use !game <code>"
                await message.add_reaction(emoji="💬")
                await message.author.send(f'**Please use `!game {code}`, {message.author.mention} to start games.**\nAlternatively, you can react with 💬 to start the game')
                utl.log(f'sent a raw code ({code})',message.author)

                messages = utl.r_pgames()
                utl.w_pgames(message.author.id, [message.id,f'{code}'])

    else:
        await bot.process_commands(message)


@bot.event
async def on_raw_reaction_add(payload):
    # Detects if a user that sent a "raw code" reacts with 💬 and sends a game if so
    x = datetime.datetime.now()
    botID = bot.user.id
    messageIDs = utl.r_pgames()
    for i,e in messageIDs.items():
        if e[0] == payload.message_id and payload.member.bot == False and payload.emoji.name == "💬" and payload.member.id == int(i):
            pgames = utl.r_pgames()

            code = ''
            for i,e in pgames.items():
                if i == f'{payload.member.id}':
                    code = e[1]
            if await butl.startgame(payload.member, code, bot.get_guild(payload.guild_id), bot):
                await payload.member.send(f'Successfully started the game. Remember to use `!endgame` when you are done!')
                utl.log(f'Started a game from a reaction ({code})',payload.member)
            else:
                await payload.member.send(f'You already have a game running. Use `!endgame` to mark your previous game as ended.')


# The command to start games
@bot.command()
async def game(ctx, *, code):
    # Calls startgame() function from BOTUTL.py
    if await butl.startgame(ctx.author, code, ctx.guild, bot):
        await ctx.author.send(f'Successfully started the game. Remember to use `!endgame` when you are done!')
        utl.log(f'Started a game ({code})',ctx.author)
    else:
        await ctx.author.send(f'You already have a game running. Use `!endgame` to mark your previous game as ended.')

# Command to end the game
@bot.command()
async def endgame(ctx, forceUser : discord.User=''):
    # Checks to see if user is an admin
    user = ctx.author

    admins = utl.admins()
    playerDebug = False
    fEnd = False
    if utl.getadmin(ctx.author):
        if forceUser != '':
            user = forceUser
            fEnd = True

    if await butl.endgame(user, bot):
        if fEnd == True:
            await ctx.author.send(f"{user.mention}'s has been marked as ended.")
            await user.send(f"{ctx.author.mention} ended your game.")
        else:
            await ctx.author.send("Your Game has been marked as ended.")

        # Logs the ending of a game
        utl.log(f'Ended a game',ctx.author)
    else:
        if fEnd == True:
            await ctx.author.send(f"{user.mention} doesn't have a game running!")
        else:
            await ctx.author.send("You don't have a game running!")




# Configures the Bot on startup
@bot.event
async def on_ready():
    x = datetime.datetime.now()
    # Prints the LOG
    utl.startLog(bot)
    Loop.start()


@bot.command()
async def help(ctx, *, none=''):
    # HELP COMMAND YEAH!
    e = discord.Embed(colour=discord.Color.green(),title=f"**Acron Bot Help**",description=f"{utl.help.help()}")
    await ctx.send(embed=e)
    if utl.getadmin(ctx.author):
        e2 = discord.Embed(colour=discord.Color.red(),title=f"**Admin Commands**",description=f"{utl.help.admin()}")
        await ctx.author.send(embed=e2)


@bot.command()
async def adebug(ctx, cmd='', *, args=''):
    admins = utl.admins()
    playerDebug = False
    if utl.getadmin(ctx.author):
        playerDebug = True

        if cmd.lower() == 'end':
            # Args: <userID> <messageID> <code>
            argSplit = args.split(' ')
            if len(argSplit) != 3:
                await ctx.send('[DEBUG] Invalid usage\n`!adebug end <userID> <messageID> <code>`')
            else:
                x = datetime.datetime.now()
                userID = argSplit[0]
                user = await bot.fetch_user(int(userID))
                # Opens game file to find message ID and game code
                games = utl.r_games()

                messageID = argSplit[1]
                code = argSplit[2]

                game = False
                for i,e in games.items():
                    if i == f'{userID}':
                        game = True

                # Gets the message ID and game code
                extraText = ''
                if game == True:
                    contents = games[f'{userID}']
                    messageID = contents[0]
                    code = contents[1]
                    extraText = '(pre-logged game)'
                    # Removes game from games.json
                    utl.w_games(userID, 'pop')

                # Gets the message from the ID
                gChannel = utl.settings()['GAME_CHANNEL']
                channel = bot.get_channel(gChannel)
                message = await channel.fetch_message(int(messageID))

                # Edits the embed to say the game has ended
                e = discord.Embed(colour=discord.Color.red(),title="*ENDED*",description=f"**{code}**")
                e.set_footer(text=f'{user.name}#{user.discriminator}',icon_url=f'{user.avatar_url}')

                await message.edit(embed = e, content = '')
                await ctx.send('[DEBUG] Forced Game to End ' + extraText)

                # Logs the ending of a game
                utl.debuglog(f'Forcibly ended a game ({messageID})',ctx.author)

        elif cmd.lower() == 'games':
            # Args: [<Reset>]
            Gamelist = ''
            if args.lower() == 'reset':
                empty = {}
                with open('games.data','w') as f:
                    json.dump(empty, f, indent=4)

                await ctx.send(f'[DEBUG] Removed all active games')
                utl.debuglog(f'Reset all games',ctx.author)
            else:
                games = utl.r_games()
                for i,e in games.items():
                    user = await bot.fetch_user(int(i))
                    Gamelist += f'\n{i} ({user.name}#{user.discriminator}) > {e[0]} > {e[1]} > {e[2]}'

                if Gamelist != '':
                    await ctx.send(f'[DEBUG] Game List:```{Gamelist}```')
                    utl.debuglog(f'Accessed all active games',ctx.author)
                else:
                    await ctx.send(f'[DEBUG] No Games Active')

        elif cmd.lower() == 'logs':
            # Args: [<Reset/Recent>]
            if args.lower() == 'reset':
                empty = ''
                with open('LOG.txt','w') as f:
                    f.write(empty)
                await ctx.send(f'[DEBUG] Removed all logs')
                utl.debuglog(f'Reset all logs',ctx.author)


            elif args.lower() == 'recent':
                logs = utl.getlogs()
                splitlogs = logs.split("[DATE]")
                await ctx.send(f'**Current Logs**\n\n```[DATE]{splitlogs[len(splitlogs)-1]}```')
                utl.debuglog(f'Accessed recent logs',ctx.author)


            else:
                file = discord.File(f"LOG.txt")
                await ctx.author.send(content='',file=file)
                await ctx.send('[DEBUG] Logs have been sent')
                utl.debuglog(f'Accessed all logs',ctx.author)

        elif cmd.lower() == 'pgames':
            # Args: [<Reset>]
            Gamelist = ''
            if args.lower() == 'reset':
                empty = {}
                with open('pgames.data','w') as f:
                    json.dump(empty, f, indent=4)
                await ctx.send(f'[DEBUG] Removed all possible games')
                utl.debuglog(f'Removed all possible games',ctx.author)
            else:
                pgames = utl.r_pgames()
                for i,e in pgames.items():
                    user = await bot.fetch_user(int(i))
                    Gamelist += f'\n{i} ({user.name}#{user.discriminator}) > {e[0]} > {e[1]}'

                if Gamelist != '':
                    await ctx.send(f'[DEBUG] Possible Game List:```{Gamelist}```')
                    utl.debuglog(f'Accessed all possible games',ctx.author)
                else:
                    await ctx.send(f'[DEBUG] No Possible Games')
        else:
            await ctx.send('[DEBUG] Invalid usage\n\n- end <userId> <messageID> <code>\n- logs [<reset/recent>]\n- pgames [<reset>]\n- games [<reset>]')

    if playerDebug == False:
        await ctx.send('[DEBUG] You do not have permission to use `!adebug`')

@bot.command(aliases=['github','src'])
async def source(ctx):
    await ctx.send('Developed by `Chunk IV` / `BananasCanCodeToo` on Github\n\nhttps://github.com/BananasCanCodeToo/Acron-Discord-Bot')


bot.load_extension("cogs.TREE")
bot.load_extension("cogs.GG")
bot.load_extension("cogs.SEND")
if utl.settings()['MEE6_API'] == True:
    bot.load_extension("cogs.RANK")

# BOT TOKEN TO RUN!!!! DO NOT SHARE!!!!
botToken = utl.settings()['BOT_TOKEN']
bot.run(botToken)

#########################################
#    Developed by BananasCanCodeToo     #
# https://github.com/BananasCanCodeToo/ #
#########################################
