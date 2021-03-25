import discord
from discord.ext import commands, tasks
import asyncio
import random
import datetime

bot = commands.Bot(command_prefix = "!", description = "Bot de Hanki")
funFact = ["L'eau mouille",
            "Le feu brule",
            "La glace brule",
            "La terre salie",
            "La neige blanche",
            "Le ciel bleu",
            "Python for ever",
            "Google chrome",
            "League of legends",
            "Valorant",
            "Dofus",
            "Mon créateur est Hanki",
            "Fondation COPX",
            "Pourquoi vous lisez ?",
            "!help"]

#bot ready
@bot.event
async def on_ready():
    print("Let's go !")
    status.start()

#background task of bot
@tasks.loop(seconds=5)
async def status():
    game = discord.Game(random.choice(funFact))
    await bot.change_presence(status=discord.Status.dnd, activity=game)

@bot.command()
async def start(ctx, secondes=3):
    status.change_interval(seconds=secondes)

#id of Owner
def isOwner(ctx):
    return ctx.message.author.id == 323776561998331914 or 500678449762140170

#command private
@bot.command()
@commands.check(isOwner)
async def private(ctx):
    await ctx.send("Cette command est seulement pour les fondateurs de Copx !!!")

#bot ping pong for test
@bot.command()
async def ping(ctx):
    #ctx = context
    await ctx.send("Pong !")

#info Server, all info
@bot.command()
async def severisnfo(ctx):
    server = ctx.guild
    numberTextChannels = len(server.text_channels)
    numberVoiceChannels = len(server.voice_channels)
    description = server.description
    numberPerson = server.member_count
    serverName = server.name
    message = f"Le serveur **{serverName}** contient **{numberPerson}** personnes. \nLa description du serveur est **{description}**. \nCe serveur possède **{numberTextChannels}** salons textuels et **{numberVoiceChannels}** salons vocaux."
    await ctx.send(message)

#info Server, await info
@bot.command()
async def getinfo(ctx, info):
    server = ctx.guild
    if info == "memberCount":
        await ctx.send(server.member_count)
    elif info == "numberChannels":
        await ctx.send(len(server.text_channels) + len(server.voice_channels))
    elif info == "name":
        await ctx.send(server.name)
    else:
        await ctx.send("Etrange... Je ne connais pas cela")

#Bot say = dit
@bot.command()
async def say(ctx,*texte):
    await ctx.send(" ".join(texte))

#Bot clear messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number : int):
    messages = await ctx.channel.history(limit = number + 1).flatten()
    for message in messages:
        await message.delete()

#bot kick user with permission kick_members under from embed
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user : discord.User, *, reason="Aucune raison n'a été donnée"):
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

#bot ban user with permission ban_members under form embed
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user : discord.User, *, reason="Aucune raison n'a été donnée"):
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
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user, *reason):
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

#bot create muted role
async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted", permissions=discord.Permissions(send_messages=False, speak=False), reason="Créaton du role Muted pour mute les users")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages=False, speak=False)
    return mutedRole

#user get muted role
async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

#mute user
@bot.command()
@commands.has_permissions(ban_members=True)
async def mute(ctx, member : discord.Member, *, reason="Aucune raison n'a été donnée"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été mute !")

#unmute user
@bot.command()
@commands.has_permissions(ban_members=True)
async def unmute(ctx, member : discord.Member, *, reason="Aucune raison n'a été donnée"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été unmute !")

#bot await messages and react
@bot.command()
async def cuisiner(ctx):
    await ctx.send("Quelle plat voulez-vous faire ?")
    def checkMessage(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel
    try:
        recette = await bot.wait_for("message", timeout = 10, check = checkMessage)
    except:
        await ctx.send("La commande a expiré !")
    message = await ctx.send(f"La préparation de {recette.content} va commencer. Veuillez valider si oui ou non vous poursuivez.")
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def checkEmoji(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")
    try:
        reaction, user = await bot.wait_for("reaction_add", timeout = 10, check = checkEmoji)
        if reaction.emoji == "✅":
            await ctx.send("La recette a démarré")
        else:
            await ctx.send("La recettte a été annulé")
    except:
        await ctx.send("La commande a expiré !")

#roulette game
@bot.command()
async def roulette(ctx):
    await ctx.send("La roulette commencera dans 10 secondes. \nEnvoyer \"moi\" dans ce channel pour y participer.")

    #list of participants
    players = []
    def check(message):
        return message.channel == ctx.message.channel and message.author not in players and message.content == "moi"
    
    try:
        while True:
            participation = await bot.wait_for('message', timeout = 15, check = check)
            players.append(participation.author)
            print("Nouveau participant : ")
            print(participation)
            await ctx.send(f"**{participants.author.name}** participe au jeu ! Le tirage commence dans 10 secondes ! ")
    except: #Timeout
        print("Demarrage du tirage")

    gagner = ["mute", "role personnel","gage"]

    await ctx.send("Le tirage va commencer dans 3...")
    await asyncio.sleep(1)
    await ctx.send("2")
    await asyncio.sleep(1)
    await ctx.send("1")
    await asyncio.sleep(1)
    loser = random.choice(players)
    price = random.choice(gagner)
    await ctx.send(f"La personne qui a gagnée un {price} est...")
    await asyncio.sleep(1)
    await ctx.send("**" + loser.name + "**" + " !")

#Token of bot
bot.run("")
