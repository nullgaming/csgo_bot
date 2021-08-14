import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


def send_callback_msg(operation, ctx, command,diff):
    channel = str(ctx.channel.id)
    base_url = "https://discordapp.com/api/channels/{}/messages".format(channel)
    headers = {"Authorization": "Bot {}".format(TOKEN),
               "User-Agent": "WarCry (http://github.com/, v0.1)",
               "Content-Type": "application/json", }
    message = str(operation.__dict__["_status"])
    if message == "Succeeded":
        if command == 0:
            message = "CS:GO Server - `Startup Initialization Successful` in `{}` secs".format(diff)
        elif command == 1:
            message = "CS:GO Server - `Reboot Successful` in `{}` secs".format(diff)
        elif command == 2:
            message = "CS:GO Server - `Shutdown Completed` in `{}` secs".format(diff)
        else:
            message = "How did I reach here ??"
    else:
        message = "Unknown status received"
        print(message)

    payload = json.dumps({"content": message})
    requests.post(base_url, headers=headers, data=payload)
