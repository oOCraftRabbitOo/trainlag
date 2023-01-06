import asyncio
import discord
from discord.ext import commands
from class_team import generate_teams, print_teams
from discord_constants import *

bot = commands.Bot(command_prefix=('$', '-', '!', 'ilo tulenileki o ', 'ß', '#', 'use any prefix ', '?', '§', '%'))
setup_complete = False  # Run setup to set to True
teams = []  # Run setup to fill


async def setup_check(ctx):
    if not setup_complete:
        await ctx.send('Setup not yet complete. Run `!setup` to setup.')
        raise Exception('Setup incomplete, du Globi!')


async def author_is_runner(ctx):
    # Get the message author and their roles
    author = ctx.message.author
    roles = author.roles

    # Get the "Fänger" role
    catcher_role = discord.utils.get(roles, name='Fänger')

    # Check if the author has the "Fänger" role
    return catcher_role is None

@bot.event
async def on_ready():
    print('\n------')
    print('Logged in lul')
    print('On the following servers:')
    for server in bot.guilds:
        print(server.name)
    print('------\n')


@bot.command()
@commands.has_permissions(manage_guild=True)
async def setup(ctx):
    global teams
    teams = generate_teams()
    print_teams(teams)
    # Get catcher role
    roles = ctx.guild.roles
    catcher_role = discord.utils.get(roles, name='Fänger')
    # Remove catcher roles
    player_ids = PLAYERS_BY_ID.keys()
    for player_id in player_ids:
        # Get the member object for the user
        member = await ctx.guild.fetch_member(player_id)
        # Remove the role from the user
        await member.edit(roles=[r for r in member.roles if r != catcher_role])

    # Add catcher roles to all catchers
    for team in teams:
        if team.is_catcher:
            for player in team.players:
                # Get the member object for the user
                member = await ctx.guild.fetch_member(player.id)
                # Add the role to the user
                await member.edit(roles=member.roles + [catcher_role])

    # Generate and send challenges to all non-catcher Teams
    non_catchers = [team for team in teams if not team.is_catcher]
    for team in non_catchers:
        team_channel = bot.get_channel(team.channel_id)
        await team_channel.send(team.return_challenges())

    # TODO: finish
    global setup_complete
    setup_complete = True
    print("Setup completed. Have fun!")
    await ctx.send('Setup completed. Have fun!')


@bot.command()
async def catch(ctx):
    await setup_check(ctx)
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
                await ctx.send('Das Team isch scho es Fänger-Team...')
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
                await ctx.send(f'Team {catcher_team.name} hät Team {caught_team.name} gfangä!')
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
