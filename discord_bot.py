import asyncio
import discord
from discord.ext import commands
from class_team import generate_teams, print_teams, Team
from config import *
import json

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=('$', '-', '!', 'ilo tulenileki o ', 'ß', '#', 'use any prefix ', '?', '§', '%', '/', '+'), intents=intents)
setup_complete = False  # Run setup to set to True
setup_in_progress = False
teams = []  # Run setup to fill
catcher_role = None  # Run setup to fill


async def setup_check(ctx: commands.Context) -> None:
    if not setup_complete:
        await ctx.send('Setup not yet complete. Run `!setup` to setup.')
        raise Exception('Setup incomplete, du Globi!')


def author_is_catcher(ctx: commands.Context) -> bool:
    global teams

    # Get the message author ID
    authorID = ctx.message.author.id

    # get the player to whom that ID corresponds
    author = None
    all_players = [player for team in teams for player in team.players]
    for i in all_players:
        if i.id == authorID:
            author = i
    
    # get the team in which the author is and return whether they are catchers
    for i in teams:
        if author in i.players:
            return i.is_catcher
    
    raise Exception(f'Could not find Player {author} with ID {authorID} in any team.')

# same as team.switch_roles, but also changes roles on discord server
async def discord_switch_roles(team: Team, ctx: commands.Context) -> None:
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
async def on_ready() -> None:
    print('\n------')
    print('Logged in lul')
    print('On the following servers:')
    for server in bot.guilds:
        print(server.name)
    print('------\n')

@bot.command()
@commands.has_permissions(manage_guild=True)
async def assign(ctx: commands.Context, *args):
    if setup_complete:
        await ctx.send('the game cannot be running for this command')
        raise Exception('game running')
    with open(TEAM_FILE, 'r') as f:
        team_list = json.load(f)

    with open(PLAYER_FILE, 'r') as f:
        player_list = json.load(f)

    team = args[0]
    players = args[1:]

    for tihm in team_list:
        if team == tihm["name"]: break
    else:
        await ctx.send('Error: Team not found :(')
        raise Exception('Team not found')

    assigned_players = [player for tihm in team_list for player in tihm['players']]
    for player in players:
        for pleier in player_list:
            if player == pleier["name"]: break
        else:
            await ctx.send(f'Error, Player "{player}" not found')
            raise Exception(f'Player "{player}" not found')
        if player in assigned_players:
            for tihm in team_list:
                if player in tihm['players']:
                    tihm['players'].remove(player)
        for tihm in team_list:
            if tihm["name"] == team:
                tihm['players'].append(player)

    with open(TEAM_FILE, 'w') as f:
        json.dump(team_list, f)

    await ctx.send(f'added players {players} to team {team} without issue')

@bot.command()
@commands.has_permissions(manage_guild=True)
async def add_players(ctx: commands.Context, *players):
    if setup_complete:
        await ctx.send('the game cannot be running for this command')
        raise Exception('game running')
    with open(PLAYER_FILE, 'r') as f:
        player_list = json.load(f)
    player_ids = [player['id'] for player in player_list]
    
    guild_players = []
    for player in players:
        guild_player = ctx.guild.get_member_named(player)
        if guild_player is None:
            await ctx.send(f'Error: Player "{player}" not found :(')
            raise Exception(f'Player "{player}" not found')
        guild_players.append((player, guild_player))

    for player in guild_players:
        if player[1].id not in player_ids:
            player_list.append({'name': player[0], 'id': player[1].id})

    with open(PLAYER_FILE, 'w') as f:
        json.dump(player_list, f)

    await ctx.send('Spieler wurden hinzugefügt.')

@bot.command()
@commands.has_permissions(manage_guild=True)
async def setup(ctx: commands.Context) -> None:
    # ensure that setup doesn't run mutiple times at once
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
        await ctx.send('Es existiert kei "Fänger"-Rolle. Abbruch.')
        raise Exception('No catcher role found')
    print(f'the type of catcher_role is {type(catcher_role)}')
    
    # generate the teams
    global teams
    print(f'generating teams with {NUM_CATCHERS} catchers')
    teams = generate_teams(num_catchers=NUM_CATCHERS)
    print_teams(teams)

    # Remove catcher roles
    print('removing catcher roles')
    player_ids = [player.id for team in teams for player in team.players]
    for player_id in player_ids:
        # Get the member object for the user
        print(player_id)
        member = await ctx.guild.fetch_member(player_id)
        # Remove the role from the user
        await member.edit(roles=[r for r in member.roles if r != catcher_role])
        print(f'catcher role of {member} removed')

    # Add catcher roles to all catchers
    print('adding catcher roles')
    for team in teams:
        if team.is_catcher:
            for player in team.players:
                # Get the member object for the user
                member = await ctx.guild.fetch_member(player.id)
                # Add the role to the user
                await member.edit(roles=member.roles + [catcher_role])
                print(f'catcher role added to {member}')

    # Generate and send challenges to all non-catcher Teams
    print('generate and send challenges')
    non_catchers = [team for team in teams if not team.is_catcher]
    for team in non_catchers:
        team_channel = bot.get_channel(team.channel.id)
        await team_channel.send(team.return_challenges())

    setup_complete = True
    setup_in_progress = False
    print("Setup completed. Have fun!")
    await ctx.send('Setup fertig. Vill Spass!')


@bot.command(aliases=['häts', 'hets', 'fang', 'häx', 'hex', 'hats', 'lolduopferbischfängerjetztimaginewürmicringe'])
async def catch(ctx: commands.Context) -> None:  # TODO: ifangstrass (No Risk No Fun II), vorläufig: kei Pünkt, wänn dete gfangä
    global teams

    await setup_check(ctx)

    # Check if the author has the "Fänger" role
    if author_is_catcher(ctx):
        # Get the ID of the channel where the command was used
        channel_id = ctx.message.channel.id

        # Check if the channel is actually a team channel 
        channel_ids = [t.channel.id for t in teams]
        if channel_id in channel_ids:

            # find the caught team
            for t in teams:
                if t.channel.id == channel_id:
                    caught_team = t
                    break
            else:
                await ctx.send('error')
                raise Exception("couldn't find the channel's id in any team, even though there was a check before to see whether it is present, rewrite your software you idiot")

        # Check if the caught team is already the "Fänger" team
            if caught_team.is_catcher:
                await ctx.send('Das Team isch scho es Fänger-Team...')
            else:
                # Get the catcher player object
                players_by_id = {player.id : player.name for team in teams for player in team.players}
                catcher = players_by_id[ctx.author.id]

                # Find the team that the catcher belongs to
                for team in teams:
                    for player in team.players:
                        if player.id == ctx.author.id:
                            catcher_team = team
                            break
                    else: continue
                    break
                else:
                    await ctx.send('error, catcher team not found')
                    raise Exception("couldn't find the catcher in any team even though he has to be there because that's how we know he's a catcher, fix ya code!")

                # Switch the roles of the caught and catcher teams
                await discord_switch_roles(caught_team, ctx)
                await discord_switch_roles(catcher_team, ctx)

                general_channel = bot.get_channel(GENERAL_CHANNEL)
                catcher_names = ""
                caught_names = ""
                for player in catcher_team.players:
                    catcher_names += player.name + ' '
                for player in caught_team.players:
                    caught_names += player.name + ' '
                catcher_names = catcher_names[:-1]
                caught_names = caught_names[:-1]
                await general_channel.send(f'S Team **{catcher_team.name}** *({catcher_names})* hät s Team **{caught_team.name}** *({caught_names})* gfangä und defür **{caught_team.bounty} Pünkt** Chopfgeld kassiert!')

                # Grant bounty
                catcher_team.points += caught_team.bounty
                received_bounty = caught_team.bounty
                caught_team.bounty = BOUNTY_BASE_POINTS
                catcher_team.bounty = BOUNTY_BASE_POINTS

                # Send challenges to the new runner team
                team_channel = bot.get_channel(catcher_team.channel.id)
                await team_channel.send(f'\n{catcher_team.return_challenges()}')
        else:
            # The channel is not in the list of channels
            await ctx.send('Das isch keis Team...')
    else:
        # The author does not have the "Fänger" role
        await ctx.send('Du bisch kein Fänger. Das chan nur en Fänger usfüehre.')


@bot.command(aliases=['abschlüsse', 'done', 'challenge', 'abschliessen'])
async def complete(ctx: commands.Context, challenge_id: int) -> None:
    await setup_check(ctx)
    # Only runnable by runners
    if author_is_catcher(ctx):
        await ctx.send(f'{ctx.message.author.mention}, du weisch scho, dass du Fänger bisch, oder?')
        return
    # Get channel's team
    channel = ctx.message.channel.id
    for t in teams:
        if t.channel.id == channel:
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
async def finish(ctx: commands.Context) -> None:
    global catcher_role
    global teams

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
    player_ids = [player.id for team in teams for player in team.players]
    for player_id in player_ids:
        # Get the member object for the user
        member = await ctx.guild.fetch_member(player_id)
        # Remove the role from the user
        await member.edit(roles=[r for r in member.roles if r != catcher_role])

@bot.command()
@commands.has_permissions(manage_guild=True)
async def dump(ctx: commands.Context) -> None:
    print_teams(teams)

@bot.command()
@commands.has_permissions(manage_guild=True)
async def switch(ctx: commands.Context) -> None:
    global teams

    # get channel's team
    channel = ctx.message.channel.id
    for t in teams:
        if t.channel.id == channel:
            team = t
            break
    
    # change the role of the team
    await discord_switch_roles(team, ctx)

    if team.is_catcher:
        state = 'Fänger'
    else:
        state = 'Devoränner'

    team.bounty = BOUNTY_BASE_POINTS
    
    await ctx.send(f"S'Team {team.name} isch jetzt {state}.")
    if not team.is_catcher:
        await ctx.send(team.return_challenges())

    general_channel = bot.get_channel(GENERAL_CHANNEL)
    await general_channel.send(f"S'Team {team.name} isch jetzt {state}.")

@bot.command()
@commands.has_permissions(manage_guild=True)
async def sync(ctx: commands.Context) -> None:
    await setup_check(ctx)
    global teams
    global catcher_role
    for team in teams:
        for player in team.players:
            member = await ctx.guild.fetch_member(player.id)
            if catcher_role in member.roles and not team.is_catcher:
                await member.edit(roles=[role for role in member.roles if role != catcher_role])
            elif not catcher_role in member.roles and team.is_catcher:
                await member.edit(roles=member.roles + [catcher_role])

@bot.command(aliases=['chopfgeld', 'kopfgeld', 'chopfgäld', 'wievilfängerhaniamhals', 'kopfgäld'])
async def bounty(ctx: commands.Context) -> None:
    await setup_check(ctx)

    output = "So stahts mit de Chopfgelder:"
    bounties = {team.name: team.bounty for team in teams if not team.is_catcher}
    sorted_teams_by_bounty = sorted(bounties.items(), key=lambda x:x[1])
    for team, bounty in reversed(sorted_teams_by_bounty):
        output += f"\nS Team **{team}** hät es Chopfgeld vo **{bounty}** uf sich"

    general_channel = bot.get_channel(GENERAL_CHANNEL)
    await general_channel.send(output)

@bot.command(aliases=['punkte', 'ranking', 'rangliste', 'pünkt', 'ranglischte'])
async def points(ctx: commands.Context) -> None:
    await setup_check(ctx)

    output = "Das isch d Ranglischte bis jetzt:"
    pointses = {team.name: team.points for team in teams}
    sorted_teams_by_points = sorted(pointses.items(), key=lambda x:x[1])
    for team, points in reversed(sorted_teams_by_points):
        output += f"\nS Team **{team}** hät momentan **{points}**."
        
    general_channel = bot.get_channel(GENERAL_CHANNEL)
    await general_channel.send(output)

@bot.command(aliases=['hunters', 'fänger', 'jäger', 'decirilischenfengermitewillamitumlautischdoof'])
async def catchers(ctx: commands.Context) -> None:
    await setup_check(ctx)

    output = "Das sind d Fänger: \n"
    catchers = [team for team in teams if team.is_catcher]
    for catcher in catchers:
        pleiers = [pleier.name for pleier in catcher.players]
        output += f"**{catcher}** {pleiers}\n"  # Wunderschönä Code ich weiss
        
    general_channel = bot.get_channel(GENERAL_CHANNEL)
    await general_channel.send(output)

@bot.command(aliases=['mitspieler', 'spieler', 'players', 'namen', 'namelist', 'allplayers'])
async def names(ctx: commands.Context) -> None:
    output = "Das sind dini Mitspieler: \n"
    playernames = [player.name for team in teams for player in team.players]
    for name in playernames[:-1]:
        output += f"{name}, "
    output = f"{output[:-2]} und {names[-1]}."

    general_channel = bot.get_channel(GENERAL_CHANNEL)
    await general_channel.send(output)

# Load the token from the .token file
token = ''
with open('.token', 'r') as f:
    token = f.read()

bot.run(token)
