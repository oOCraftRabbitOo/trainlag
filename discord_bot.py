import asyncio
import discord
from discord.ext import commands
from class_team import generate_teams, print_teams, Team
from config import *

bot = commands.Bot(command_prefix=('$', '-', '!', 'ilo tulenileki o ', 'ß', '#', 'use any prefix ', '?', '§', '%', '/', '+'))
setup_complete = False  # Run setup to set to True
setup_in_progress = False
teams = []  # Run setup to fill
catcher_role = None  # Run setup to fill


async def setup_check(ctx):
    if not setup_complete:
        await ctx.send('Setup not yet complete. Run `!setup` to setup.')
        raise Exception('Setup incomplete, du Globi!')


def author_is_catcher(ctx) -> bool:
    global teams

    # Get the message author ID
    authorID = ctx.message.author.id

    # get the player to whom that ID corresponds
    author = None
    for i in ALL_PLAYERS:
        if i.id == authorID:
            author = i
    
    # get the team in which the author is and return whether they are catchers
    for i in teams:
        if author in i.players:
            return i.is_catcher
    
    raise Exception(f'Could not find Player {author} with ID {authorID} in any team.')

# same as team.switch_roles, but also changes roles on discord server
async def discord_switch_roles(team: Team, ctx) -> None:
    global catcher_role
    print(f'changing the role of {team.name}')

    # get ids of all players in team
    player_ids = [player.id for player in team.players]

    for player_id in player_ids:
        # will get member of discord server corresponding to id
        member = await ctx.guild.fetch_member(player_id)

        if not team.is_catcher:
            # add catcher role to current roles
            await member.edit(roles = member.roles + [catcher_role])
            print(f'made {member} a catcher')

        else:
            # remove catcher role from current roles
            await member.edit(roles = [role for role in member.roles if role != catcher_role])
            print(f'made {member} a runner')
    
    team.switch_roles()
    print()


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
async def setup(ctx: commands.Context):
    print('\n\n===\nStarting setup\n----')
    print('checking whether setup is already done or in progress')
    global setup_complete
    global setup_in_progress
    if setup_complete or setup_in_progress:
        await ctx.send('Spiel lauft bereits, Spiel mit "finish" beende.')
        raise Exception('Game already in progress')
    setup_in_progress = True

    # Get catcher role
    print('getting server catcher role')
    roles = ctx.guild.roles
    global catcher_role
    catcher_role = discord.utils.get(roles, name='Fänger')
    if catcher_role is None:
        await ctx.send('Es existiert kei "Fänger" rolle, Abbruch')
        raise Exception('No catcher role found')
    print(f'the type of catcher_role is {type(catcher_role)}')
    
    global teams
    print(f'generating teams with {NUM_CATCHERS} catchers')
    teams = generate_teams(num_catchers=NUM_CATCHERS)
    print_teams(teams)

    print('removing catcher roles')
    # Remove catcher roles
    player_ids = PLAYERS_BY_ID.keys()
    for player_id in player_ids:
        # Get the member object for the user
        member = await ctx.guild.fetch_member(player_id)
        # Remove the role from the user
        await member.edit(roles=[r for r in member.roles if r != catcher_role])
        print(f'catcher role of {member} removed')

    print('adding catcher roles')
    # Add catcher roles to all catchers
    for team in teams:
        if team.is_catcher:
            for player in team.players:
                # Get the member object for the user
                member = await ctx.guild.fetch_member(player.id)
                # Add the role to the user
                await member.edit(roles=member.roles + [catcher_role])
                print(f'catcher role added to {member}')

    print('generate and send challenges')
    # Generate and send challenges to all non-catcher Teams
    non_catchers = [team for team in teams if not team.is_catcher]
    for team in non_catchers:
        team_channel = bot.get_channel(team.channel_id)
        await team_channel.send(team.return_challenges())

    setup_complete = True
    setup_in_progress = False
    print("Setup completed. Have fun!")
    await ctx.send('Setup fertig. Vill spass!')


@bot.command()
async def catch(ctx):  # TODO: ifangstrass (No Risk No Fun II), vorläufig: kei Pünkt, wänn dete gfangä
    global catcher_roll

    await setup_check(ctx)

    # Check if the author has the "Fänger" role
    if author_is_catcher(ctx):
        # Get the ID of the channel where the command was used
        channel_id = ctx.message.channel.id

        # Check if the channel is in the list of channels
        if channel_id in CHANNELS:
            # Get the index of the channel in the list
            index = CHANNELS.index(channel_id)

            # Get the team for the channel
            try:
                caught_team = teams[index]
            except IndexError:
                await ctx.send('Öppis isch schiefgloffe, wahrschinlich existiert das Team hüt nöd')
                raise Exception('Index out of range bim teams accesse')

        # Check if the caught team is already the "Fänger" team
            if caught_team.is_catcher:
                await ctx.send('Das Team isch scho es Fänger-Team...')
            else:
                # Get the catcher player object
                catcher = PLAYERS_BY_ID[ctx.author.id]

                # Find the team that the catcher belongs to
                for team in teams:
                    if catcher in team.players:
                        catcher_team = team
                        break

                # Switch the roles of the caught and catcher teams
                await discord_switch_roles(caught_team, ctx)
                await discord_switch_roles(catcher_team, ctx)

                general_channel = bot.get_channel(GENERAL_CHANNEL)
                await general_channel.send(f'Team {catcher_team.name} hät Team {caught_team.name} gfangä! Team {caught_team.name}, ihr söttet no Discord neustarte, will ihr susch evtl. nöd vo allne alli aktive Challenges gsehnd.')

                # Send challenges to the new runner team
                team_channel = bot.get_channel(catcher_team.channel_id)
                await team_channel.send(catcher_team.return_challenges())
        else:
            # The channel is not in the list of channels
            await ctx.send('Das Team chammer nöd fangä!')
    else:
        # The author does not have the "Fänger" role
        await ctx.send('Du bisch kein Fänger. Das chan nur en Fänger usfüehre.')


@bot.command()
async def complete(ctx, challenge_id):
    await setup_check(ctx)
    # Only runnable by runners
    if author_is_catcher(ctx):
        await ctx.send(f'{ctx.message.author.mention}, du weisch scho, dass du Fänger bisch, oder?')
        return
    # Get channel's team
    channel = ctx.message.channel.id
    for t in teams:
        if t.channel_id == channel:
            team = t
            break
    try:
        # Complete challenge
        completed_challenge =team.open_challenges[int(challenge_id)-1]
        challenge_name = completed_challenge.title
        challenge_reward = completed_challenge.points
        team.complete_challenge(int(challenge_id)-1)
        await ctx.send(f'Nice, d Challenge "{challenge_name}" hät eu {challenge_reward} Pünkt gäh. '
                       f'Das heisst, ihr händ jetzt {team.points} Pünkt!\n'
                       f'--------------------------------------------')
        # Send challenges to the team
        await ctx.send(team.return_challenges())
    except ValueError:
        await ctx.send(f'{challenge_id} isch kei Zahl. Gänd bitte 1, 2 oder 3 ii.')
    except IndexError:
        await ctx.send(f'Challenge {challenge_id} schiint nöd z existiere. Gänd bitte 1, 2 oder 3 ii.')

@bot.command()
@commands.has_permissions(manage_guild=True)
async def finish(ctx):
    global catcher_role

    await setup_check(ctx)
    global setup_complete
    global setup_in_progress
    setup_complete = False
    setup_in_progress = False
    # Get a list of teams by highest score
    winners = teams.copy()
    winners.sort()

    # Generate the output string
    out = f"""@everyone Das isch s Podescht:
--------------------------------------------
{EMOJI[1]} **{winners[0]}** mit {winners[0].points} Pünkt
{EMOJI[2]} **{winners[1]}** mit {winners[1].points} Pünkt
{EMOJI[3]} **{winners[2]}** mit {winners[2].points} Pünkt\n"""

    for n, team in enumerate(winners[3:-1]):
        out += f"{EMOJI[4+n]} **{winners[3+n]}** mit {winners[3+n].points} Pünkt\n"
    out += f"{EMOJI['last']} **{winners[len(teams)-1]}** mit {winners[len(teams)-1].points} Pünkt"

    general_channel = bot.get_channel(GENERAL_CHANNEL)
    await general_channel.send(out)

    # Remove catcher roles
    player_ids = PLAYERS_BY_ID.keys()
    for player_id in player_ids:
        # Get the member object for the user
        member = await ctx.guild.fetch_member(player_id)
        # Remove the role from the user
        await member.edit(roles=[r for r in member.roles if r != catcher_role])

@bot.command()
@commands.has_permissions(manage_guild=True)
async def dump(ctx):
    print_teams(teams)

@bot.command()
@commands.has_permissions(manage_guild=True)
async def switch(ctx):
    global teams

    # get channel's team
    channel = ctx.message.channel.id
    for t in teams:
        if t.channel_id == channel:
            team = t
            break
    
    # change the role of the team
    await discord_switch_roles(team, ctx)

    if team.is_catcher:
        state = 'Fänger'
    else:
        state = 'Devoränner'
    
    await ctx.send(f"S'Team {team.name} isch jetzt {state}.")
    if not team.is_catcher:
        await ctx.send(team.return_challenges())

    general_channel = bot.get_channel(GENERAL_CHANNEL)
    await general_channel.send(f"S'Team {team.name} isch jetzt {state}.")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def sync(ctx: commands.Context):
    setup_check()
    global teams
    global catcher_role
    for team in teams:
        for player in team.players:
            member = await ctx.guild.fetch_member(player.id)
            if catcher_role in member.roles() and not team.is_catcher:
                member.edit(roles=[role for role in member.roles() if role != catcher_role])
            elif not catcher_role in member.roles() and team.is_catcher:
                member.edit(roles=member.roles() + [catcher_role])



# Load the token from the .token file
token = ''
with open('.token', 'r') as f:
    token = f.read()

bot.run(token)
