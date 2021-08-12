from csazure import CSGO_AZURE
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import time

load_dotenv()


csgo = CSGO_AZURE()

TOKEN = os.getenv("DISCORD_TOKEN")
client = commands.Bot(command_prefix='.')
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Game(type=discord.ActivityType.playing, name="Counter-Strike: Global Offensive"))
    print('Bot is ready')


@client.command()
async def ping(ctx):
    await ctx.send('Pong! {}ms'.format(round(client.latency * 1000)))


@client.command()
async def start(ctx):
    await ctx.send("CS:GO Server - Initializing Startup")
    csgo.start_server()
    ip = csgo.get_instance_IP()
    await ctx.send(f"CS:GO Server - IP is `{ip}`")


@client.command()
async def stop(ctx):
    await ctx.send("CS:GO Server - Initializing Shutdown")
    csgo.stop_server()
    status = csgo.get_server_status()
    await ctx.send(f"CS:GO Server Status - `{status}`")


@client.command()
async def restart(ctx):
    await ctx.send("CS:GO Server - Initializing Shutdown")
    csgo.restart_server()
    ip = csgo.get_instance_IP()
    await ctx.send(f"CS:GO Server - IP is `{ip}`")


@client.command()
async def status(ctx):
    status = csgo.get_server_status()
    await ctx.send(f"CS:GO Server Status - `{status}`")


@client.command()
async def help(ctx):
    response_title = "Command List"
    command_list = "`ping`: Returns bot's latency\n`start_server`: Starts csgo server\n`stop_server`: Stops csgo server\n`restart_server`: Restarts csgo server\n`play`: Connect to server\n`status`: Returns server's running status"
    emb = discord.Embed(title=response_title,
                        description=command_list, color=0x679eff)
    await ctx.send(embed=emb)


@client.command()
async def play(ctx):
    status = csgo.get_server_status()

    if status == "stopped" or status == "stopping" or status == "starting":
        await ctx.send(f"CS:GO Server - Server is NOT ACTIVE")
    else:
        ip = csgo.get_instance_IP()
        response_title = "Connect to Server"
        description = "`Direct Connect`: steam://connect/{0}:27015/kalajadu69\n`Console CMD`: `connect {0}:27015;password kalajadu69`".format(
            ip)
        emb = discord.Embed(title=response_title,
                            description=description).set_footer(text="glhf!")
        await ctx.send(embed=emb)


if __name__ == "__main__":
    client.run(TOKEN)
