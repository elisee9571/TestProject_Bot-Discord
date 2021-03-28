import discord
from discord.ext import commands, tasks
import asyncio
import random
import datetime


class PrivateOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    Me = 323776561998331914
    FRIEND = 500678449762140170

    def command_channel(ctx):
        return ctx.message.channel.id == 825095623569047633

    #id of Owner
    def isOwner(self, ctx):
        return ctx.message.author.id == ME or FRIEND

    #command private
    @commands.command()
    @commands.check(isOwner)
    @commands.check(command_channel)
    async def private(self, ctx):
        await ctx.send("Cette commande est seulement pour les fondateurs de Copx !!!")

    