import json
import os
import discord
from discord.ext import bridge, commands
from funcs.derivadas import getdotenv

with open(f"utils/config{getdotenv('Bot')}.json") as f:
    configData = json.load(f)

Intents = discord.Intents(
    bans=True,
    emojis=True,
    emojis_and_stickers=True,
    guild_messages=True,
    dm_messages=True,
    guilds=True,
    members=True,
    message_content=True,
    messages=True,
    voice_states=True,
)

client = bridge.Bot(
    command_prefix=commands.when_mentioned_or("%$", "&&", "&"),
    intents=Intents,
    help_command=None,
    case_insensitive=True
)

pastaname = 'commands'
for filename in os.listdir(f'./{pastaname}'):
    for commands in os.listdir(f'./{pastaname}/{filename}'):
        if commands.endswith('.py') and not commands.startswith('__'):
            client.load_extensions(f'{pastaname}.{filename}.{commands[:-3]}')

for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        client.load_extension(f"events.{filename[:-3]}")
