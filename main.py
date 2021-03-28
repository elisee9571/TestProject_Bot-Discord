import discord
from discord.ext import commands, tasks
import asyncio
import random
import datetime
#import file for commands
import info
import private
import ban
import kick

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

TOKEN = ""

def command_channel(ctx):
    return ctx.message.channel.id == 825095623569047633

def mute_channel(ctx):
        return ctx.message.channel.id == 825094246201557023

#bot ready
@bot.event
async def on_ready():
    print("Ready !")
    status.start()

#background task of bot
@tasks.loop(seconds=5)
@commands.check(command_channel)
async def status():
    game = discord.Game(random.choice(funFact))
    await bot.change_presence(status=discord.Status.dnd, activity=game)

@bot.command()
async def start(ctx, secondes=3):
    status.change_interval(seconds=secondes)

#manage errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Cette commande n'existe pas. \nTappe !help pour consulter les commandes.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument. Des chiffres ou un mot !")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions pour cette commande. \nEcrit !help pour voir vos commandes.")
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Oups, vous ne pouvez pas utilisez cette commande ici !")
    if isinstance(error.original, discord.Forbidden):#error, commands.BotMissingPermissions
        await ctx.send("Oups, je n'est pas les permissions pour ceci")

#id of Owner
def isOwner(ctx):
    return ctx.message.author.id == ... or ... #put your id

#command private
@bot.command()
@commands.check(isOwner)
async def private(ctx):
    await ctx.send("Cette command est seulement pour les fondateurs de Copx !!!")

#bot ping pong for test
@bot.command()
@commands.check(command_channel)
async def ping(ctx):
    #ctx = context
    await ctx.send("Pong !")

#Bot say = dit
@bot.command()
@commands.check(command_channel)
async def say(ctx,*texte):
    await ctx.send(" ".join(texte))

#Bot clear messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number : int):
    messages = await ctx.channel.history(limit = number + 1).flatten()
    for message in messages:
        await message.delete()

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
@commands.check(command_channel)
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
@commands.check(command_channel)
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

bot.add_cog(info.InfoOwner(bot))
bot.add_cog(ban.BanOwner(bot))
bot.add_cog(kick.KickOwner(bot))
bot.add_cog(private.PrivateOwner(bot))
#Token of bot
bot.run(TOKEN)

