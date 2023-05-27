import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def join(ctx):
    print(ctx)
    channel = ctx.author.voice.channel
    if ctx.author.voice is None:
        await ctx.send("You are not in a voice channel!")
        return
    elif ctx.voice_client != None:
        await ctx.send("I'm already in a voice channel!")
    else:
        await channel.connect()

bot.run('MTExMTkxMDkzNDUzMzkwMjMzNg.GyMKbx.RxIa_a38kk5YDBGGUHaGAutDk8krDLuOEvilKc')
