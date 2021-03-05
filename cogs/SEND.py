import discord
import datetime
from discord.ext import commands, tasks
from datetime import timedelta
from itertools import cycle
import things.UTILITIES as utl

class Send(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['sh','msg'])
    async def send(self, ctx, *, msg):
        # Fun command to send messages as the bot
        if utl.getadmin(ctx.author):
            await ctx.message.delete()
            await ctx.send(msg)

    @commands.command(aliases=['shc','chmsg'])
    async def sendchannel(self, ctx, channel, *, msg):
        # Fun command to send messages as the bot to a specific channel
        if utl.getadmin(ctx.author):
            channel = self.bot.get_channel(int(channel[2:-1]))
            await channel.send(msg)
            await ctx.message.add_reaction(emoji='👍')

def setup(bot):
    bot.add_cog(Send(bot))

#########################################
#    Developed by BananasCanCodeToo     #
# https://github.com/BananasCanCodeToo/ #
#########################################
