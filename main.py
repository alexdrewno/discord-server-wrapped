import discord
from DiscordClient import DiscordClient
import os

from dotenv import load_dotenv

load_dotenv()

# Main script to start the DiscordClient
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = DiscordClient(intents=intents)

if DISCORD_TOKEN == None:
    print("No DISCORD_TOKEN provided")
else:
    client.run(DISCORD_TOKEN)
