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
import UTILITIES as utl
import BOTUTL as butl

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
                name = f'{usr.name} | Rank #{srank}'
            else:
                name = f'{usr.nick} ({usr.name}) | Rank #{srank}'


            emb = discord.Embed(colour=discord.Color.blue(),title=f'**{name}**')

            emb.add_field(inline = False, name = f"LEVEL **{sdata['level']}**", value = f"**{sdata['level']}** {rankprogress} **{sdata['level'] + 1}** | {percentxp}%")
            emb.add_field(inline = True, name = 'EXP Level', value = f'{dxp[0]} / {dxp[1]} XP')
            emb.add_field(inline = True, name = 'EXP Total', value = f'{dxp[2]} XP')

            emb.set_thumbnail(url = f"{usr.avatar_url}")


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
                name = f'{usr.name} | Rank #{srank}'
            else:
                name = f'{usr.nick} ({usr.name}) | Rank #{srank}'

            emb = discord.Embed(colour=discord.Color.purple(),title=f'**{name}**')

            emb.add_field(inline = False, name = f"LEVEL **{sdata['level']}**", value = f"**{sdata['level']}** {rankprogress} **{sdata['level'] + 1}** | {percentxp}%")
            emb.add_field(inline = True, name = 'EXP Level', value = f'{dxp[0]} / {dxp[1]} XP')
            emb.add_field(inline = True, name = 'EXP Total', value = f'{dxp[2]} XP')
            emb.add_field(inline = True, name = '', value = f'')
            if user2 == True:
                axp = adata['detailed_xp']
                emb.add_field(inline = True, name = 'MSGs to Rank Up', value = f'Abt. {round((axp[2]-dxp[2])/20)} Messages')
            else:
                emb.add_field(inline = True, name = 'MSGs to Rank Up', value = f'0 Messages (Rank #1)')
            emb.add_field(inline = True, name = 'MSGs to Level Up', value = f'Abt. {round((dxp[1]-dxp[0])/20)} Messages')

            hierarchy = ''

            if user2 == True:
                axp = adata['detailed_xp']
                hierarchy += f"#{srank-1} {adata['username']} (+{axp[2] - dxp[2]} XP | +{round((axp[2]-dxp[2])/20)} MSGs)\n"

            hierarchy += f"#{srank} >> **{usr.name}** (+0 XP | +0 MSGs)\n"

            if user3 == True:
                bxp = bdata['detailed_xp']
                hierarchy += f"#{srank+1} {bdata['username']} (-{dxp[2] - bxp[2]} XP | -{round((dxp[2]-bxp[2])/20)} MSGs)"

            emb.add_field(inline = False, name = 'Rank Hierarchy', value = hierarchy)



            emb.set_thumbnail(url = f"{usr.avatar_url}")


            await ctx.send(embed = emb)


def setup(bot):
    bot.add_cog(RANK(bot))
