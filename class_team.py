from load_uc4 import specific_challenge_generate, specific_challenges_amount, unspecific_challenge_generate, unspecific_challenges_amount, zurich_challenge_generate, zurich_challenges_amount
import discord
from class_player import Player
from config import *
from class_channel import Channel
from class_challenge import Challenge
from normal_config import REGIO_RATIO
from what_time_period import *
from pointcalc import distance_dict
import random
import pickle
import datetime
import glob
import os
import json

class Team:
    def __init__(self, players: list[Player], channel: Channel, name: str, is_catcher: bool = False) -> None:
        self.players = players
        # self.channel_id = channel_id   | deprecated by adding the channel class
        self.channel = channel
        self.name = name
        self.is_catcher = is_catcher
        self.points = 0
        self.bounty = 0
        self.completed_unspecific_challenges = []  # ids
        self.places_visited = []  # ids
        self.zkaffs_visited = []  # ids
        self.completed_challenges = []  # Challenge Objects
        self.open_challenges = []
        #self.normal_mode_time = (datetime.datetime.now() + SPECIFIC_PERIOD).time()
        self.last_zone = START_ZONE
        self.last_challenge_generation = datetime.time(hour=4, minute=20)
        self.generate_challenges(START_ZONE, 0)
        self.backup()

    def deb_str(self) -> str:
        names = ""
        for player in self.players:
            names += player.name + " "
        strink = f'--\n\nTeam {self.name}, \nchannel: {self.channel.name}, {self.channel.id}, \npoints: {self.points}, \ncompCChals: {self.completed_unspecific_challenges}, \nplaces visited: {self.places_visited}, \nopenChals: {self.open_challenges}, \ncompChals: {self.completed_challenges}, \nbounty: {self.bounty}, \nmembers: ({names[:-1]})'
        if self.is_catcher:
            strink += '\n[Fänger]'
        return strink
    
    def __str__(self) -> str:
        names = ""
        for player in self.players:
            names += player.name + " "
        strink = f'Team {self.name} ({names[:-1]})'
        if self.is_catcher:
            strink += ' [fänger]'
        return strink

    def __lt__(self, other):  # Used for sorting "less than", ich weiss nöd wieso ich das muss so ummä iigäh, aber isch halt so
        return self.points > other.points

    def generate_specific_challenge(self, zone: int, delta: int, zurich_only: bool = False, min_perim_distance: int = -1, max_perim_distance: int | None = None, min_personal_distance: int = -1, max_personal_distance: int = 69420, zoneables: bool = True) -> Challenge:  # TODO: Walking Distance
        time = time_now()
        # Set min/max times
        if max_perim_distance is None:
            max_perim_distance = maximum_perimeter_distance(time)

        # Randomly select incomplete challenge (int)
        print("spec ", end="")
        place = random.randint(0, specific_challenges_amount - 1)
        challenge = specific_challenge_generate(place, zone, delta)
        for _ in range(2000):
            if (place in self.places_visited or
                    (challenge.perimeter_distance <= min_perim_distance) or
                    (challenge.perimeter_distance >= max_perim_distance) or
                    (challenge.kaff > maximum_kaffness(time)) or
                    (distance_dict[zone][challenge.zone] <= min_personal_distance) or
                    (distance_dict[zone][challenge.zone] >= max_personal_distance) or
                    (not zoneables and challenge.zoneable)):

                print("spec ", end="")
                place = random.randint(0, specific_challenges_amount - 1)
                if zurich_only:
                    challenge = zurich_challenge_generate(place, zone, delta) # TODO: Test
                else:
                    challenge = specific_challenge_generate(place, zone, delta)
            else:
                break
        else:
            print(f"fuck:\nTeam: {self.deb_str()}\ncompleted unspec: {self.completed_unspecific_challenges}\nplaces visited: {self.places_visited}\npoints: {self.points}\nlast zone: {self.last_zone}\nis catcher: {self.is_catcher}\ntime: {time}, current time: {datetime.datetime.now().time()}\nchallenge: {challenge}")
            index = random.randint(0, unspecific_challenges_amount - 1)
            challenge = unspecific_challenge_generate(index, zone, delta)

        # Generate challenge and return it
        return challenge

    def generate_zurich_challenge(self, zone: int, delta: int) -> Challenge:
        zkaff = random.randint(0, zurich_challenges_amount-1)
        challenge = zurich_challenge_generate(zkaff, zone, delta)
        if len(self.zkaffs_visited) == zurich_challenges_amount:
            self.zkaffs_visited = []
        while zkaff in self.zkaffs_visited:
            zkaff = random.randint(0, zurich_challenges_amount-1)
            challenge = zurich_challenge_generate(zkaff, zone, delta)

        return challenge

    def generate_unspecific_challenge(self, zone: int, delta: int, make_regionspecific: bool = False) -> Challenge:
        time = time_now()
        time_period = what_time_period()
        # Randomly select incomplete challenge (int)
        print("unsp ", end="")
        index = random.randint(0, unspecific_challenges_amount - 1)
        challenge = unspecific_challenge_generate(index, zone, delta)
        for _ in range(2000):
            if index in self.completed_unspecific_challenges or (time_period == "Perimeter Period" and not challenge.in_perim) or (challenge.regionspecific != make_regionspecific):
                print("unsp ", end="")
                index = random.randint(0, unspecific_challenges_amount - 1)
                challenge = unspecific_challenge_generate(index, zone, delta)
            else:
                break
        else:
            print(f"fuck:\nTeam: {self.deb_str()}\ncompleted unspec: {self.completed_unspecific_challenges}\nplaces visited: {self.places_visited}\npoints: {self.points}\nlast zone: {self.last_zone}\nis catcher: {self.is_catcher}\ntime: {time}, current time: {datetime.datetime.now().time()}\nchallenge: {challenge}")
            index = random.randint(0, unspecific_challenges_amount - 1)
            challenge = unspecific_challenge_generate(index, zone, delta)

        # Generate challenge and return it
        return challenge

    def generate_regionspecific_challenge(self, zone: int, delta: int):
        return self.generate_unspecific_challenge(zone, delta, True)

    def generate_challenges(self, zone: int, delta: int) -> None:
        time_period = what_time_period()

        match time_period:
            case "Postgame":
                print("Error: Can't generate challenges after the game ended.")
            case "End Game Period":
                self.generate_end_game_challenges(zone, delta)
            case "Zurich Period":
                self.generate_zurich_challenges(zone, delta)
            case "Perimeter Period":
                self.generate_perimeter_challenges(zone, delta)
            case "Normal Period":
                self.generate_normal_challenges(zone, delta)
            case "Specific Period":
                self.generate_specific_challenges(zone, delta)
            case "Pre Game":
                print(f"Game hasn't started yet, generating three specific challenges for team {self.name} and assuming the team is still in zone {START_ZONE}.")
                self.generate_specific_challenges(START_ZONE, delta)
            case _:
                print("Wut? This is not a valid time period!")

    def generate_specific_challenges(self, zone: int, delta: int):  # 3x Specific (no perim), 0x Unspecific
        self.open_challenges = [self.generate_specific_challenge(zone, delta)]
        for _ in range(2):
            challenge = self.generate_specific_challenge(zone, delta)
            while challenge in self.open_challenges:
                challenge = self.generate_specific_challenge(zone, delta)
            self.open_challenges.append(challenge)
        self.shuffle_challenges()

    def generate_normal_challenges(self, zone: int, delta: int):  # 1x Unspecific, 1x specific near team (may be zoneable), 1x specific further from team (may be regionspecific)
        # unspecific
        self.open_challenges = [self.generate_unspecific_challenge(zone, delta)]

        # specific near
        challenge = self.generate_specific_challenge(zone, delta, min_personal_distance=NORMAL_PERIOD_NEAR[0], max_personal_distance=NORMAL_PERIOD_NEAR[1], zoneables=True)
        self.open_challenges.append(challenge)

        # specific far
        if random.random() < REGIO_RATIO: # Chose a regionspecific challenge
            challenge = self.generate_regionspecific_challenge(zone, delta)
        else:
            challenge = self.generate_specific_challenge(zone, delta, min_personal_distance=NORMAL_PERIOD_FAR[0], max_personal_distance=NORMAL_PERIOD_FAR[1], zoneables=False)
        self.open_challenges.append(challenge)

        self.shuffle_challenges()

    def generate_zurich_challenges(self, zone: int, delta: int):   # 2x Specific (with a growing chance to be in 110), 1x Unspecific
        time = time_now()
        max_perim_distance = maximum_perimeter_distance(time)
        # unspecific
        self.open_challenges = [self.generate_unspecific_challenge(zone, delta)]

        random_float = random.random() * 100
        print("zufallsprozent: ", random_float)
        zurich_percentage = zurich_probability()
        print("zurichsprozent: ", zurich_percentage)

        replace_near = ((zurich_percentage - 50) * 2) > random_float
        replace_far = (zurich_percentage * 2) > random_float

        # specific near
        if replace_near:
            challenge = self.generate_zurich_challenge(zone, delta)
        else:
            challenge = self.generate_specific_challenge(zone, delta, min_perim_distance=0, max_perim_distance=max_perim_distance / 2)
        self.open_challenges.append(challenge)

        # specific far
        if replace_far:
            challenge = self.generate_zurich_challenge(zone, delta)
        else:
            challenge = self.generate_specific_challenge(zone, delta, min_perim_distance=max_perim_distance / 2 + 1, max_perim_distance=max_perim_distance)
        self.open_challenges.append(challenge)

        self.shuffle_challenges()

    def generate_perimeter_challenges(self, zone: int, delta: int):  # 1x Specific (outer half)(may not be Regio), 1x specific (inner half)(may not be zoneable), 1x Unspecific
        time = time_now()
        max_perim_distance = maximum_perimeter_distance(time)
        # unspecific
        self.open_challenges = [self.generate_unspecific_challenge(zone, delta)]

        # specific near
        challenge = self.generate_specific_challenge(zone, delta, min_perim_distance=0,
                                                     max_perim_distance=max_perim_distance/2)
        self.open_challenges.append(challenge)

        # specific far
        challenge = self.generate_specific_challenge(zone, delta, min_perim_distance=max_perim_distance/2+1,
                                                         max_perim_distance=max_perim_distance, zoneables=False)
        self.open_challenges.append(challenge)

        self.shuffle_challenges()

    # def generate_zurich_challenges(self, zone: int, delta: int):  # 2x Specific (within 20 min of ZUE or in 110 itself), 1x Unspecific (no regio) TODO: Add Züri-Challenges to generation
    #     self.generate_normal_challenges(zone, delta)  # I mean, it should work... TODO: Test

    def generate_end_game_challenges(self, zone: int, delta: int):  # 1x Specific in z110, 2x Unspecific
        self.open_challenges = [self.generate_zurich_challenge(zone, delta)]
        for _ in range(2):
            challenge = self.generate_unspecific_challenge(zone, delta)
            while challenge in self.open_challenges:
                challenge = self.generate_unspecific_challenge(zone, delta)
            self.open_challenges.append(challenge)
        self.shuffle_challenges()

    def shuffle_challenges(self):  # TODO: test, reason to include: harder to read which period you're in
        random.shuffle(self.open_challenges)

    def complete_challenge(self, index: int, delta: int) -> None:
        # Index should be 1, 2 or 3
        completed_challenge = self.open_challenges[index]

        # Save challenge completion
        self.completed_challenges.append(completed_challenge)

        if completed_challenge.zkaff:
            self.zkaffs_visited.append(completed_challenge.id)
        else:
            if not completed_challenge.specific:
                self.completed_unspecific_challenges.append(completed_challenge.id)
            elif completed_challenge.specific:
                self.places_visited.append(completed_challenge.id)

        # Grant points
        self.grant_points(completed_challenge.points)

        delta = delta - completed_challenge.points

        # Generate new challenges
        self.generate_challenges(completed_challenge.zone, delta)

        self.last_zone = completed_challenge.zone
        print(f'd zone vom team {self.name} isch jetzt {self.last_zone}')

        # Backup
        self.backup()  # TODO: Does this work?

    def grant_points(self, points: int) -> None:
        self.points += points
        self.bounty += int(points * BOUNTY_PERCENTAGE)

    def deduct_points(self, points) -> None:
        self.grant_points(-points)

    '''
    def reroll_challenges(self, delta: int) -> str:  # TODO: remove
        if time_now() < UNSPECIFIC_TIME:
            print("Cant reroll challenges, too early")
            return "Ihr chönd no kein reroll mache, es isch nonig Ziit."
        elif self.last_challenge_generation > UNSPECIFIC_TIME:
            print("Cant reroll challenges, this team already exclusively has unspecific challenges")
            return "Ihr chönd nöd rerolle, ihr händ scho nur unspezifischi"
        else:
            self.generate_challenges(self.last_zone, delta)
            return "wowzers"
    '''

    def uncomplete_challenge(self, index) -> None:
        # Get challenge to uncomplete and remove it from completed challenges
        uncompleted_challenge = self.completed_challenges.pop(index)

        if not uncompleted_challenge.specific:
            self.completed_unspecific_challenges.remove(uncompleted_challenge.id)
        elif uncompleted_challenge.specific:
            self.places_visited.remove(uncompleted_challenge.id)

        # Deduct points
        self.deduct_points(uncompleted_challenge.points)

    def backup(self) -> None:
        # TODO: test
        # Get the current date and time
        now = datetime.datetime.now()

        # Generate a filename using the current date and time
        file = f'backups/{self.name}_{now:%Y-%m-%d_%H-%M-%S}.pickle'
        # Open a file in binary write mode
        with open(file, 'wb') as f:
            # Serialize the object and write it to the file
            pickle.dump(self, f)

    def load(self, file: str | None = None) -> None:
        # TODO: test
        if file is None:
            # Find the newest file in the current directory
            files = glob.glob(f'backups/{self.name}*.pickle')
            file = max(files, key=os.path.getctime)

        # Open a file in binary read mode
        with open(file, 'rb') as f:
            # Deserialize the object from the file
            loaded_team = pickle.load(f)

        # Update all values to the loaded file
        self.players = loaded_team.players
        self.channel_id = loaded_team.channel_id
        self.name = loaded_team.name
        self.is_catcher = loaded_team.is_catcher
        self.points = loaded_team.points
        self.bounty = loaded_team.bounty
        self.completed_unspecific_challenges = loaded_team.completed_unspecific_challenges
        self.places_visited = loaded_team.places_visited
        self.completed_challenges = loaded_team.completed_challenges
        self.open_challenges = loaded_team.open_challenges

    def switch_roles(self, delta: int, zone: int | None = None) -> None:
        if self.is_catcher:
            self.is_catcher = False
            self.generate_challenges(START_ZONE if zone is None else zone, delta)
        else:
            self.is_catcher = True
            self.open_challenges = []
        self.backup()

    def return_challenges(self) -> list[discord.Embed]:
        out = []
        for num, challenge in enumerate(self.open_challenges):
            embed = discord.Embed(title=f"{u'🛤️ ' if challenge.no_disembark else ''}{challenge.title}", description=challenge.description)
            embed.set_footer(text=f"{challenge.points} Pünkt")
            embed.set_author(name=f"Challenge {num+1}")
            out.append(embed)
        out.append(discord.Embed(title=f"Aktuells Chopfgeld: {self.bounty}", colour=15823957))
        return out


def get_teams_from_json() -> list:
    with open(TEAM_FILE, 'r') as f:
        return json.load(f)

def get_players_from_json() -> list:
    with open(PLAYER_FILE, 'r') as f:
        return json.load(f)

def get_players_in_team(raw_players, all_players, team_name) -> list[Player]:
    players_in_team = []
    if len(raw_players) == 0:
        raise Exception(f'no players found in team {team_name}')
    for raw_player in raw_players:
        raw_id = get_player_id(raw_player, all_players)
        players_in_team.append(Player(raw_player, raw_id))
    return players_in_team

def get_player_id(player_name, all_players) -> int:
    for raw_player in all_players:
        if raw_player["name"] == player_name:
            return raw_player["id"]
    raise Exception("Couldn't find id???")

def choose_catchers(teams, num_catchers):
    catchers = random.sample(teams, num_catchers)
    for team in catchers:
        team.is_catcher = True

def generate_teams(num_catchers: int) -> list[Team]:
    teams = []
    raw_teams = get_teams_from_json()
    players = get_players_from_json()

    for raw_team in raw_teams:
        # get the team name
        name = raw_team['name']
        players_in_team = get_players_in_team(raw_team['players'], players, name)
        channel = Channel(
            raw_team['channel']['name'],
            raw_team['channel']['id']
        )

        teams.append(Team(players_in_team, channel, name))

    choose_catchers(teams, num_catchers)

    return teams

def print_teams(teams: list[Team]) -> None:
    # Only for debug purposes, prints out the Teams, duh
    print("---------")
    print("The Teams:")
    for team in teams:
        print(team.deb_str())
    print("---------")


if __name__ == "__main__":
    teams = generate_teams(1)
    print_teams(teams)
