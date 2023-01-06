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
    # Get the message author and their roles
    author = ctx.message.author
    roles = author.roles

    # Get the "Fänger" role
    catcher_role = discord.utils.get(roles, name='Fänger')

    # Check if the author has the "Fänger" role
    if catcher_role is not None:
        # Get the ID of the channel where the command was used
        channel_id = ctx.message.channel.id

        # Check if the channel is in the list of channels
        if channel_id in CHANNELS:
            # Get the index of the channel in the list
            index = CHANNELS.index(channel_id)

            # Get the team for the channel
            caught_team = teams[index]

            # Check if the caught team is already the "Fänger" team
            if caught_team.is_catcher:
                await ctx.send('Das Team isch es Fänger-Team...')
            else:
                # Get the catcher player object
                catcher = PLAYERS_BY_ID[author.id]

                # Find the team that the catcher belongs to
                for team in teams:
                    if catcher in team.players:
                        catcher_team = team
                        break

                # Switch the roles of the caught and catcher teams
                caught_team.switch_roles()
                # TODO: Here is code repetition müüüüüü
                player_ids = [player.id for player in caught_team.players]
                for player_id in player_ids:
                    # Get the member object for the user
                    member = await ctx.guild.fetch_member(player_id)
                    # Add the role to the user
                    await member.edit(roles=member.roles + [catcher_role])

                catcher_team.switch_roles()
                player_ids = [player.id for player in catcher_team.players]
                for player_id in player_ids:
                    # Get the member object for the user
                    member = await ctx.guild.fetch_member(player_id)
                    # Remove the role from the user
                    await member.edit(roles=[r for r in member.roles if r != catcher_role])
        else:
            # The channel is not in the list of channels
            await ctx.send('Das Team chammer nöd fangä!')
    else:
        # The author does not have the "Fänger" role
        await ctx.send('Du bisch kein Fänger. Das chan nur en Fänger usfüehre.')


# Load the token from the .token_shrek file
token = ''
with open('.token', 'r') as f:
    token = f.read()

bot.run(token)
