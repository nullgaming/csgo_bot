from csazure import CSGO_AZURE
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

csgo = CSGO_AZURE()

TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix=".", help_command=None)
cspwd = os.getenv("CSPWD")


def server_status():
    return csgo.get_server_status()


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Game(type=discord.ActivityType.playing, name="Counter-Strike: Global Offensive"))
    print('Bot is ready')


@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {}ms'.format(round(bot.latency * 1000)))


@bot.command()
async def status(ctx):
    status = csgo.get_server_status()
    await ctx.send(f"CS:GO Server Status - `{status}`")


@bot.command()
async def start(ctx):
    srv_status = server_status()
    if srv_status == "running":
        await  ctx.send("CS:GO Server - `Started`")
    elif srv_status == "starting":
        await ctx.send("CS:GO Server - `Startup Initialized,Patience!`")
    else:
        await ctx.send("CS:GO Server - `Initializing Startup`")
        csgo.start_server(ctx)


@bot.command()
async def stop(ctx):
    srv_status = server_status()
    if srv_status == "stopped":
        await ctx.send("CS:GO Server - `Stopped`")
    elif srv_status == "stopping":
        await ctx.send("CS:GO Server - `Shutdown Initialized,Patience!`")
    else:
        await ctx.send("CS:GO Server - `Initializing Shutdown`")
        csgo.stop_server(ctx)


@bot.command()
async def restart(ctx):
    await ctx.send("CS:GO Server - `Initializing Reboot`")
    csgo.restart_server(ctx)


@bot.command()
async def help(ctx):
    response_title = "Command List"
    command_list = "`ping`: Returns bot's latency\n`start`: Starts csgo server\n`stop`: Stops csgo server\n`restart`: Restarts csgo server\n`play`: Connect to server\n`status`: Returns server's running status"
    emb = discord.Embed(title=response_title,
                        description=command_list, color=0x679eff)
    await ctx.send(embed=emb)


@bot.command()
async def play(ctx):
    status = csgo.get_server_status()

    if status == "stopped" or status == "stopping" or status == "starting":
        await ctx.send(f"CS:GO Server - Server is NOT ACTIVE")
    else:
        ip = csgo.get_instance_IP()
        response_title = "Connect to Server"
        description = "`Direct Connect`: steam://connect/{0}:27015/{1}\n`Console CMD`: `connect {0}:27015;password {1}`".format(
            ip,
            cspwd)
        emb = discord.Embed(title=response_title,
                            description=description).set_footer(text="glhf!")
        await ctx.send(embed=emb)


if __name__ == "__main__":
    bot.run(TOKEN)
