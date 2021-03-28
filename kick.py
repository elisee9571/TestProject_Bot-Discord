import discord
from discord.ext import commands, tasks
import asyncio
import random
import datetime


class KickOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def kick_channel(ctx):
        return ctx.message.channel.id == 825094216891105330

    #bot kick user with permission kick_members under from embed
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.check(kick_channel)
    async def kick(self, ctx, user : discord.User, *, reason="Aucune raison n'a été donnée"):
        #await ctx.guild.kick(user, reason = reason)
        embed = discord.Embed(title="**Kick**", description="Un modérateur est chaud !", url="https://github.com/elisee9571/Bot-Discord", color=0x2ECC71)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/36101493?s=200&v=4")
        embed.add_field(name="Membre kick", value=user.name, inline=False)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.name, inline=True)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text='Bot Python Test', icon_url="https://avatars.githubusercontent.com/u/36101493?s=200&v=4")
        
        await ctx.send(embed = embed)