import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('Logged in lul')
    print('On The following servers:')
    for server in bot.guilds:
        print(server.name)
    print('------\n')

token = ''
with open('.token', 'r') as f:
    token = f.read()
bot.run(token)
