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

class RANK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rank','ar','abrank','abr'])
    async def arank(self, ctx, usr : discord.Member=''):
        if usr == '':
            usr = ctx.author
        user = False
        page = 0
        rank = 1
        while user == False:
            data = requests.get(f'https://mee6.xyz/api/plugins/levels/leaderboard/{ctx.guild.id}?page={page}').json()
            sdata = {}
            if data['players'] == []:
                await ctx.send('That user is not ranked!')
                break
            for i in data['players']:
                if i['username'] == f'{usr.name}' and i['discriminator'] == f'{usr.discriminator}':
                    sdata = i
                    srank = rank
                else:
                    rank += 1
            if sdata != {}:
                user = True
            page += 1
        if user == True:
            dxp = sdata['detailed_xp']
            pexp = dxp[0]/dxp[1]
            percentxp = round(round(pexp, 3) * 100, 1)
            percxp = round(round(pexp, 2) * 10)
            rankprogress = ''
            color = random.choice(['🟧','🟦','🟥','🟫','🟪','🟩','🟨'])
            for i in range(1, 11):
                if i <= percxp:
                    rankprogress += color
                else:
                    rankprogress += '⬜'


            if usr.nick == None:
                name = f'{usr.name}'
            else:
                name = f'{usr.nick} ({usr.name})'


            emb = discord.Embed(colour=discord.Color.blue(),title=f'Rank #**{srank}**')

            emb.add_field(inline = False, name = f"LEVEL **{sdata['level']}** (**{percentxp}**%)", value = f"**{sdata['level']}** {rankprogress} **{sdata['level'] + 1}**")
            emb.add_field(inline = True, name = '**EXP Level**', value = f'{dxp[0]} / {dxp[1]} XP')
            emb.add_field(inline = True, name = '**EXP Total**', value = f'{dxp[2]} XP')
            emb.add_field(inline = True, name = '**Messages**', value = f"{sdata['message_count']}")

            emb.set_author(name = f'{name}', icon_url = f"{usr.avatar_url}")


            await ctx.send(embed = emb)

    @commands.command(aliases=['rdash','adash','ad','rd','dashr','dr'])
    async def dashrank(self, ctx, usr : discord.Member=''):
        if usr == '' or utl.getadmin(ctx.author) == False:
            usr = ctx.author
        user = False
        user2 = False
        user3 = False
        page = 0
        rank = 1
        go = False
        sdata = {}
        adata = {}
        bdata = {}
        tempdata = {}

        while user == False:
            data = requests.get(f'https://mee6.xyz/api/plugins/levels/leaderboard/{ctx.guild.id}?page={page}').json()
            if data['players'] == []:
                await ctx.send('That user is not ranked!')
                break
            for i in data['players']:
                if i['username'] == f'{usr.name}' and i['discriminator'] == f'{usr.discriminator}':
                    sdata = i
                    srank = rank
                    adata = tempdata
                    go = True
                else:
                    if go == True:
                        bdata = i
                        break
                    tempdata = i
                    rank += 1
            if sdata != {}:
                user = True
            if adata != {}:
                user2 = True
            if bdata != {}:
                user3 = True
            page += 1
        if user == True:
            dxp = sdata['detailed_xp']
            pexp = dxp[0]/dxp[1]
            percentxp = round(round(pexp, 3) * 100, 1)
            percxp = round(pexp*10)
            rankprogress = ''
            color = random.choice(['🟧','🟦','🟥','🟫','🟪','🟩','🟨'])
            for i in range(1, 11):
                if i <= percxp:
                    rankprogress += color
                else:
                    rankprogress += '⬜'

            if usr.nick == None:
                name = f'{usr.name}'
            else:
                name = f'{usr.nick} ({usr.name})'

            emb = discord.Embed(colour=discord.Color.purple(),title=f'Rank #**{srank}**')

            emb.add_field(inline = False, name = f"LEVEL **{sdata['level']}** (**{percentxp}**%)", value = f"**{sdata['level']}** {rankprogress} **{sdata['level'] + 1}**")
            emb.add_field(inline = True, name = '**EXP Level**', value = f'{dxp[0]} / {dxp[1]} XP')
            emb.add_field(inline = True, name = '**EXP Total**', value = f'{dxp[2]} XP')
            emb.add_field(inline = True, name = '**Messages**', value = f"{sdata['message_count']}")
            if user2 == True:
                axp = adata['detailed_xp']
                emb.add_field(inline = True, name = '**MSGs to Rank Up**', value = f'Abt. {round((axp[2]-dxp[2])/20)} Messages')
            else:
                emb.add_field(inline = True, name = '**MSGs to Rank Up**', value = f'0 Messages (Rank #1)')
            emb.add_field(inline = True, name = '**MSGs to Level Up**', value = f'Abt. {round((dxp[1]-dxp[0])/20)} Messages')

            hierarchy = ''

            if user2 == True:
                axp = adata['detailed_xp']
                hierarchy += f"#{srank-1} {adata['username']} (+{axp[2] - dxp[2]} XP | +{round((axp[2]-dxp[2])/20)} MSGs)\n"

            hierarchy += f"**#{srank} {usr.name} (+0 XP | +0 MSGs)**\n"

            if user3 == True:
                bxp = bdata['detailed_xp']
                hierarchy += f"#{srank+1} {bdata['username']} (-{dxp[2] - bxp[2]} XP | -{round((dxp[2]-bxp[2])/20)} MSGs)"

            emb.add_field(inline = False, name = '**Rank Hierarchy**', value = hierarchy)



            emb.set_author(name = f'{name}', icon_url = f"{usr.avatar_url}")


            await ctx.send(embed = emb)


    @commands.command(aliases=['alevels','al','ldrbrd','aleaderboard'])
    async def leaderboard(self, ctx):
        user = ctx.author
        user_ = False
        user_t5 = False
        userdata = {}
        data = requests.get(f'https://mee6.xyz/api/plugins/levels/leaderboard/{ctx.guild.id}?page=0').json()
        page = 0

        try:
            top5 = requests.get(f'https://mee6.xyz/api/plugins/levels/leaderboard/{ctx.guild.id}?page=0').json()['players'][:10]
        except IndexError:
            top5 = requests.get(f'https://mee6.xyz/api/plugins/levels/leaderboard/{ctx.guild.id}?page=0').json()['players']


        for i in range(0,len(top5)):
            if top5[i]['username'] == f'{user.name}' and top5[i]['discriminator'] == f'{user.discriminator}':
                userdata = top5[i]
                userrank = i + 1
                rangel = i
                user_t5 = True
                user_ = True


        while user_ == False:
            data = requests.get(f'https://mee6.xyz/api/plugins/levels/leaderboard/{ctx.guild.id}?page={page}').json()
            if data['players'] == []:
                await ctx.send('You are not ranked!')
                break
            for i in range(0, len(data['players'])):
                if data['players'][i]['username'] == f'{user.name}' and data['players'][i]['discriminator'] == f'{user.discriminator}':
                    userdata = data['players'][i]
                    userrank = i + 1
                    rangel = i
                    fulldata = data
            if userdata != {}:
                user_ = True
            page += 1

        emb = discord.Embed(colour = discord.Color.random(), title = f"**{data['guild']['name']}**", description = '==========================')
        emb.set_author(name = f'Leaderboard', url = f'https://mee6.xyz/leaderboard/{ctx.guild.id}')


        for i in range(0,len(top5)):
            if top5[i]['username'] == f'{user.name}' and top5[i]['discriminator'] == f'{user.discriminator}':
                emb.add_field(inline = False, name = f">> **#{i+1} {top5[i]['username']}** <<", value = f"Lvl {top5[i]['level']} / {top5[i]['detailed_xp'][2]} XP / {top5[i]['message_count']} MSGs")
            else:
                emb.add_field(inline = False, name = f"#**{i+1}** {top5[i]['username']}", value = f"Lvl {top5[i]['level']} / {top5[i]['detailed_xp'][2]} XP / {top5[i]['message_count']} MSGs")


        if user_ == True:
            if user_t5 != True:
                emb.add_field(inline = False, name = f"", value = f"==========================\n")

                emb.add_field(inline = False, name = f">> **#{userrank} {userdata['username']}** <<", value = f"Lvl {userdata['level']} / {userdata['detailed_xp'][2]} XP / {userdata['message_count']} MSGs")

        await ctx.send(embed = emb, content = f'<https://mee6.xyz/leaderboard/{ctx.guild.id}>')
def setup(bot):
    bot.add_cog(RANK(bot))
