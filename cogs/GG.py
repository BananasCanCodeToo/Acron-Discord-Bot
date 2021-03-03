import discord
import datetime
import json
from discord.ext import commands, tasks
from discord import Embed, Member
from datetime import timedelta
from itertools import cycle
import UTILITIES as utl
import BOT as main

class GGendgame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.GGs = 0
        self.start = datetime.datetime.now() - timedelta(minutes=5)
        self.owner = None
        self.gglist = []

    @commands.Cog.listener()
    async def on_message(self, message):
        x = datetime.datetime.now()
        msg = message.content
        GG = False
        with open('GG.txt','r') as f:
            GGs = f.read().split('\n')
        for i in GGs:
            if i == '':
                continue
            elif i == msg.lower():
                GG = True


        if utl.r_games() == []:
            GG = False


        if GG == True:
            games = utl.r_games()

            if x > self.start + timedelta(minutes=5):
                self.GGs = 0
                self.start = x
                self.owner = None
                self.gglist = []
            if message.author.id not in self.gglist:
                self.GGs += 1
                a = False
                for i,e in games.items():
                    if int(i) == message.author.id and self.owner == None:
                        self.owner = message.author.id
                        b = False
                        if self.owner != None:
                            b = True
                        utl.log(f'Said GG ({self.GGs}/3 | GO: {b})',message.author)
                        a = True
                if a == False:
                    b = False
                    if self.owner != None:
                        b = True
                    utl.log(f'Said GG ({self.GGs}/3 | GO: {b})',message.author)
                self.gglist.append(message.author.id)



            if self.owner != None:
                if self.GGs >= 3:
                    user = await self.bot.fetch_user(self.owner)

                    contents = games[f'{user.id}']
                    messageID = contents[0]
                    code = contents[1]

                    # Removes game from games.json
                    utl.w_games(user.id, 'pop')

                    # Gets the message from the ID
                    gChannel = utl.settings()['GAME_CHANNEL']
                    channel = self.bot.get_channel(gChannel)
                    gamemsg = await channel.fetch_message(int(messageID))

                    # Edits the embed to say the game has ended
                    e = discord.Embed(colour=discord.Color.red(),title="*ENDED*",description=f"**{code}**")
                    e.set_footer(text=f'{user.name}#{user.discriminator}',icon_url=f'{user.avatar_url}')

                    await gamemsg.edit(embed = e, content = '')

                    await user.send("Your Game has been marked as ended. (3 GG's have been said)")

                    # Logs the ending of a game
                    utl.log(f"Ended a game from GG's ({code})",user)

                    self.GGs = 0
                    self.start = x - timedelta(minutes=5)
                    self.owner = None
                    self.gglist = []

def setup(bot):
    bot.add_cog(GGendgame(bot))

#########################################
#    Developed by BananasCanCodeToo     #
# https://github.com/BananasCanCodeToo/ #
#########################################
