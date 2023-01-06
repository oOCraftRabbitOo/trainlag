import asyncio
import discord
from discord.ext import commands
from class_team import generate_teams, print_teams
from discord_constants import *

bot = commands.Bot(command_prefix='$')

teams = generate_teams()
print_teams(teams)

@bot.event
async def on_ready():
    print('Logged in lul')
    print('On the following servers:')
    for server in bot.guilds:
        print(server.name)
    print('------\n')


@bot.command()
@commands.has_permissions(manage_guild=True)
async def setup(ctx, arg1, arg2):
    # TODO: put catchers to catcher role
    await ctx.send(f'You passed {arg1} and {arg2}')


@bot.command()
async def catch(ctx):
    # Get the message author
    author = ctx.message.author

    # Get the role by name
    catcher_role = discord.utils.get(author.guild.roles, name='Fänger')

    if catcher_role in author.roles:
        # The author has the role
        channel_id = ctx.message.channel.id
        if channel_id in CHANNELS:
            index = CHANNELS.index(channel_id)
            caught_team = teams[index]
            if caught_team.is_catcher:
                await ctx.send('Das Team isch es Fänger-Team...')
            else:
                catcher = PLAYERS_BY_ID[author.id]
                for team in teams:
                    for player in team.players:
                        if player == catcher:
                            catcher_team = team
                try:
                    caught_team.switch_roles()
                    catcher_team.switch_roles()
                except NameError:
                    ctx.send('Du bisch zwar Fänger, aber nöd Teil vom Spiil. Sorry.')
        else:
            await ctx.send('Das Team chammer nöd fangä!')
    else:
        # The author does not have the role
        await ctx.send('Du bisch kein Fänger. Das chan nur en Fänger usfüehre.')


# Load the token from the .token_shrek file
token = ''
with open('.token_shrek', 'r') as f:
    token = f.read()

bot.run(token)
