import discord
import datetime
import json
import pickle
import yaml
from discord.ext import commands, tasks
from discord import Embed, Member
from datetime import timedelta
from itertools import cycle
import things.UTILITIES as utl

async def startgame(user, code, guild, bot):
    x = datetime.datetime.now()

    games = utl.r_games()
    game = False

    # looks to see if this player already has a game
    for i,e in games.items():
        if i == f'{user.id}':
            game = True
            break

    if game == False:
        gChannel = utl.settings()['GAME_CHANNEL']
        gameChannel = bot.get_channel(gChannel)
        currentPing = x

        ping = ''
        if utl.ping() == True:
            ping = guild.get_role(utl.settings()['SQUIRREL_ROLE']).mention

        # Sends game code
        e = discord.Embed(colour=discord.Color.orange(),title=f"**{code}**",description='React with 🐿️ if you joined')
        e.set_footer(text=f'{user.name}#{user.discriminator}',icon_url=f'{user.avatar_url}')

        message = await gameChannel.send(embed = e, content = f'{ping}')
        await message.add_reaction(emoji="🐿️")

        try:
            utl.w_pgames(user.id, 'pop')
        except KeyError:
            pass
        games = utl.r_games()

        # Writes the game to the Game JSON file
        utl.w_games(user.id, [message.id,code,x.strftime("%Y.%m.%d.%H:%M:%S")])
        return True
    else:
        return False

async def pgames(user):
    pgames = utl.r_pgames()

    code = ''
    for i,e in pgames.items():
        if i == f'{user.id}':
            code = e[1]
    return code

async def endgame(user, bot):
    # Opens game file to find message ID and game code
    games = utl.r_games()

    game = False
    for i,e in games.items():
        if i == f'{user.id}':
            game = True

    # Gets the message ID and game code
    if game == True:
        contents = games[f'{user.id}']
        messageID = contents[0]
        code = contents[1]

        # Removes game from games.json
        utl.w_games(user.id, 'pop')

        # Gets the message from the ID
        gChannel = utl.settings()['GAME_CHANNEL']
        channel = bot.get_channel(gChannel)
        message = await channel.fetch_message(int(messageID))

        # Edits the embed to say the game has ended
        e = discord.Embed(colour=discord.Color.red(),title="*ENDED*",description=f"**{code}**")
        e.set_footer(text=f'{user.name}#{user.discriminator}',icon_url=f'{user.avatar_url}')

        await message.edit(embed = e, content = '')

        return True
    else:
        return False
