import discord
from discord.ext import commands, tasks
import asyncio
import random
import datetime


class InfoOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def info_channel(ctx):
        return ctx.message.channel.id == 825089282066481252

    #info Server, all info
    @commands.command()
    @commands.check(info_channel)
    async def serverinfo(self, ctx):
        server = ctx.guild
        numberTextChannels = len(server.text_channels)
        numberVoiceChannels = len(server.voice_channels)
        description = server.description
        numberPerson = server.member_count
        serverName = server.name
        message = f"Le serveur **{serverName}** contient **{numberPerson}** personnes. \nLa description du serveur est **{description}**. \nCe serveur possède **{numberTextChannels}** salons textuels et **{numberVoiceChannels}** salons vocaux."
        await ctx.send(message)

    #info Server, await info
    @commands.command()
    @commands.check(info_channel)
    async def getinfo(self, ctx, info):
        server = ctx.guild
        if info == "memberCount":
            await ctx.send(server.member_count)
        elif info == "numberChannels":
            await ctx.send(len(server.text_channels) + len(server.voice_channels))
        elif info == "name":
            await ctx.send(server.name)
        else:
            await ctx.send("Etrange... Je ne connais pas cela")