import discord
import datetime
from discord.ext import commands, tasks
from discord import Embed, Member
from datetime import timedelta
from itertools import cycle
import things.UTILITIES as utl




class Tree(commands.Cog):
    # Initializes the cog for the tree command
    def __init__(self, bot):
        self.bot = bot
        self.active = False
        self.players = {}
        self.lastPing = datetime.datetime.now() - timedelta(minutes=30)
        self.message = None
        self.force = {}

    # Detects if someone reacts to the tree ping message
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.active == True:
            if payload.message_id == self.message.id:
                if self.bot.user.id != payload.member.id:
                    user = payload.member
                    self.players[user] = datetime.datetime.now()

                    # If they do react to the tree ping message, edit the embed to include their usernames
                    em = discord.Embed(colour=discord.Color.green(),title="Tree Ping (3+ Squirrels required)",description=f"React with 🐿️ to show you are available")
                    footer = ''
                    for i,e in self.players.items():
                        footer += f'{i.name}#{i.discriminator}\n'
                    em.set_footer(text=footer)
                    await self.message.edit(embed=em)
                    utl.log(f'Joined Tree ping ({len(self.players)}/3)',payload.member)

    # Detects if users un-react to the tree ping message
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if self.active == True:
            if payload.message_id == self.message.id:
                if self.bot.user.id != payload.user_id:
                    user = await self.bot.fetch_user(payload.user_id)
                    try:
                        self.players.pop(user)
                    except:
                        pass
                    em = discord.Embed(colour=discord.Color.green(),title="Tree Ping (3+ Squirrels required)",description=f"React with 🐿️ to show you are available")
                    footer = ''

                    # If so, removes the from the embed
                    for i,e in self.players.items():
                        footer += f'{i.name}#{i.discriminator}\n'
                    em.set_footer(text=footer)
                    await self.message.edit(embed=em)
                    utl.log(f'Left Tree ping ({len(self.players)}/3)',user)

    @commands.command(aliases=['treeping','pingtree','tr'])
    async def tree(self, ctx, tpass=''):
        x = datetime.datetime.now()
        user = ctx.author
        if tpass.lower() == 'pass':
            if utl.getadmin(ctx.author):
                channel = self.bot.get_channel(utl.settings()['GAME_CHANNEL'])
                utl.log('Forced Tree ping',ctx.author)
                if self.lastPing + timedelta(minutes=utl.settings()['PING_TIMEOUT'])< x:
                    # Pings the trees if 3 people are available
                    await channel.send(f"{self.bot.get_guild(ctx.guild.id).get_role(utl.settings()['TREE_ROLE']).mention}, There are 3 (or more) squirrels available!")
                    if self.active == True:
                        self.ping.cancel()
                    self.active = False
                    self.players = {}
                    self.lastPing = x
                    self.message = None
                else:
                    if ctx.author.id not in self.force.keys():
                        self.force[ctx.author.id] = False
                    if self.force[ctx.author.id] == False:
                        await ctx.send(f"**WARNING!** It has not been the tree ping timeout of `{utl.settings()['PING_TIMEOUT']}` minutes\n*Run command again to confirm*")
                        self.force[ctx.author.id] = True
                        utl.log('Attempted to force Tree ping [TIMEOUT]',ctx.author)
                    elif self.force[ctx.author.id] == True:
                        # Pings the trees if 3 people are available
                        await channel.send(f"{self.bot.get_guild(ctx.guild.id).get_role(utl.settings()['TREE_ROLE']).mention}, There are 3 (or more) squirrels available!")
                        self.active = False
                        self.players = {}
                        self.lastPing = x
                        self.message = None
                        utl.log('Forced Tree ping [TIMEOUT]',ctx.author)
                        self.force[ctx.author.id] = False
            elif not utl.getadmin(ctx.author):
                await ctx.send('*You do not have permission to do that*')
        elif self.active == False:
            if self.lastPing + timedelta(minutes=utl.settings()['PING_TIMEOUT'])< x:
                utl.log('Started Tree ping',ctx.author)
                self.players[ctx.author] = x

                # Creates the embed of the tree ping to send to the game channel
                em = discord.Embed(colour=discord.Color.green(),title="Tree Ping (3+ Squirrels required)",description=f"React with 🐿️ to show you are available")
                footer = ''
                for i,e in self.players.items():
                    footer += f'{i.name}#{i.discriminator}\n'
                em.set_footer(text=footer)

                # Gets the game channel
                channel = self.bot.get_channel(utl.settings()['GAME_CHANNEL'])

                # Sends the embed to the game channel
                self.message = await channel.send(embed = em, content = '')
                await self.message.add_reaction(emoji="🐿️")
                self.active = True
                self.ping.start()
            else:
                # Sends a message saying ther tee ping command is on cooldown
                await ctx.send('Tree ping is on cooldown!')
                utl.log('Attempted to start tree ping (COOLDOWN ERROR)',ctx.author)
        else:
            # If a tree ping is already active, it adds them to the tree ping
            self.players[ctx.author] = x
            em = discord.Embed(colour=discord.Color.green(),title="Tree Ping (3+ Squirrels required)",description=f"React with 🐿️ to show you are available")
            footer = ''
            for i,e in self.players.items():
                footer += f'{i.name}#{i.discriminator}\n'
            em.set_footer(text=footer)
            await self.message.edit(embed=em)
            utl.log(f'Joined Tree ping ({len(self.players)}/3)',ctx.author)


    @tasks.loop(seconds=15)
    async def ping(self):
        x = datetime.datetime.now()
        em = discord.Embed(colour=discord.Color.green(),title="Tree Ping (3+ Squirrels required)",description=f"React with 🐿️ to show you are available")
        footer = ''
        newplayers = {}
        for i,e in self.players.items():
            # Removes offline players 10 minutes after joining the tree ping
            if x > e + timedelta(minutes=10):
                if i.status != discord.Status.online:
                    utl.log(f'was removed from Tree ping ({i.status})',i)
                # Removes online players 30 minutes after joining
                elif x > e + timedelta(minutes=30):
                    utl.log(f'was removed from Tree ping ({i.status} - 30 minute timeout)',i)
                else:
                    # Doesn't remove all other players
                    footer += f'{i.name}#{i.discriminator}\n'
                    newplayers[i] = e
            else:
                footer += f'{i.name}#{i.discriminator}\n'
                newplayers[i] = e

        # Updates the player variable with players
        self.players = newplayers
        em.set_footer(text=footer)

        # Edits the embed wit hthe (possibly) updated lsit of players
        await self.message.edit(embed = em)
        channel = self.bot.get_channel(utl.settings()['GAME_CHANNEL'])
        if len(self.players) >= 3:
            # Pings the trees if 3 people are available
            await channel.send(f"{self.bot.get_guild(self.message.guild.id).get_role(utl.settings()['TREE_ROLE']).mention}, There are 3 (or more) squirrels available!")
            self.active = False
            self.players = {}
            self.lastPing = x
            self.message = None
            utl.log('Tree ping succeeded')
            self.ping.cancel()
        elif len(self.players) == 0:
            # Ends tree ping if everyone was removed for inactivity or left
            self.active = False
            self.players = {}
            utl.log('Tree ping failed (0/3)')
            self.ping.cancel()
            em = discord.Embed(colour=discord.Color.red(),title="Tree Ping **FAILED**",description=f"Not enough squirrels!")
            await self.message.edit(embed = em)
            self.message = None

    @commands.command(aliases=['tdebug'])
    async def treedebug(self, ctx,arg=''):
        # Debug command for tree ping (sends data about current tree ping)
        x = datetime.datetime.now()
        list = ''
        for i,e in self.players.items():
            list += f'{i.id} ({i.name}#{i.discriminator}) > {e.strftime("%H:%M:%S")} ({x - e} / {i.status})\n'
        if self.active == True:
            if self.players == {}:
                await ctx.send(f'[DEBUG] No players in current tree ping')
            else:
                await ctx.send(f'[DEBUG]\n```{list}```')
        else:
            await ctx.send(f'[DEBUG] No Tree ping active')
        utl.debuglog('Accessed Tree ping data', ctx.author)

def setup(bot):
    bot.add_cog(Tree(bot))

#########################################
#    Developed by BananasCanCodeToo     #
# https://github.com/BananasCanCodeToo/ #
#########################################
