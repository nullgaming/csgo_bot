import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = commands.Bot(command_prefix='^')

@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def ping(ctx):
    await ctx.send('Pong! {}ms'.format(round(client.latency*1000)))

client.run(TOKEN)