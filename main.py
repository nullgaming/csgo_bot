import discord
from discord.ext import commands
from dotenv import load_dotenv
import os, time
load_dotenv()

from ec2 import CSGO_EC2
csgo = CSGO_EC2()

TOKEN = os.getenv("DISCORD_TOKEN")
client = commands.Bot(command_prefix='^')

@client.event
async def on_ready():
    print('Bot is ready')


@client.command()
async def ping(ctx):
	await ctx.send('Pong! {}ms'.format(round(client.latency*1000)))


@client.command()
async def start_server(ctx):
	csgo.start_server()
	await ctx.send("CS:GO Server - Initializing Startup")
	time.sleep(15)
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


if __name__ == "__main__":
	client.run(TOKEN)