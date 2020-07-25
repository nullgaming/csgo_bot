import discord
from discord.ext import commands
from dotenv import load_dotenv
import os, time
load_dotenv()

from ec2 import CSGO_EC2
csgo = CSGO_EC2()

TOKEN = os.getenv("DISCORD_TOKEN")
client = commands.Bot(command_prefix='.')
client.remove_command('help')

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, platform="Twitch", name=".help", game="Counter-Strike Global Offensive", url="steam://connect/13.126.60.35:27015/Urban_Hunger1"))
	print('Bot is ready')


@client.command()
async def ping(ctx):
	await ctx.send('Pong! {}ms'.format(round(client.latency*1000)))


@client.command()
async def start_server(ctx):
	csgo.start_server()
	await ctx.send("CS:GO Server - Initializing Startup")
	time.sleep(20)
	ip = csgo.get_instance_IP()
	await ctx.send(f"CS:GO Server - IP is `{ip}`")


@client.command()
async def stop_server(ctx):
	csgo.stop_server()
	await ctx.send("CS:GO Server - Initializing Shutdown")


@client.command()
async def get_ip(ctx):
	status = csgo.get_server_status()

	if(status=="stopped" or status=="stopping"):
		await ctx.send(f"CS:GO Server - Server is NOT ACTIVE")
	else:
		ip = csgo.get_instance_IP()	
		await ctx.send(f"CS:GO Server - IP is `{ip}`")


@client.command()
async def status(ctx):
	status = csgo.get_server_status()
	await ctx.send(f"CS:GO Server Status - `{status}`")

@client.command()
async def help(ctx):
	response_title = "Command List"
	command_list = "`ping`: Returns bot's latency\n`start_server`: Starts csgo server\n`stop_server`: Stops csgo server\n`get_ip`: Returns server's IP\n`status`: Returns server's running status"
	emb = discord.Embed(title = response_title, description = command_list, color = 0x679eff)
	await ctx.send(embed = emb)

if __name__ == "__main__":
	client.run(TOKEN)