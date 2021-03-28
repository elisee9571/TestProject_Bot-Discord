import discord
from discord.ext import commands, tasks
import asyncio
import random
import datetime


class BanOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def ban_channel(ctx):
        return ctx.message.channel.id == 825094189527334972

    #bot ban user with permission ban_members under form embed
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.check(ban_channel)
    async def ban(self, ctx, user : discord.User, *, reason="Aucune raison n'a été donnée"):
        #await ctx.guild.ban(user, reason = reason)
        embed = discord.Embed(title="**Banissement**", description="Un modérateur a frappé !", url="https://github.com/elisee9571/Bot-Discord", color=0x6844ff)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/36101493?s=200&v=4")
        embed.add_field(name="Membre banni", value=user.name, inline=False)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.name, inline=True)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text='Bot Python Test', icon_url="https://avatars.githubusercontent.com/u/36101493?s=200&v=4")
        
        await ctx.send(embed = embed)

    #bot unban user
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.check(ban_channel)
    async def unban(self, ctx, user, *reason):
        reason = " ".join(reason)
        userName, userId = user.split("#")
        bannedUsers = await ctx.guild.bans()
        for i in bannedUsers:
            if i.user.name == userName and i.user.discriminator == userId:
                await ctx.guild.unban(i.user, reason = reason)
                await ctx.send(f"**{user}** a été unban.")
                return
        #user not found
        await ctx.send(f"L'utilisateur **{user}** n'est pas dans la liste des bans ! ")