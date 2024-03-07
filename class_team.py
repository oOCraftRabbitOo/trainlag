from load_challenges import generate_specific_challenge, specific_challenges_amount, generate_unspecific_challenge, unspecific_challenges_amount
from class_player import Player
from config import *
from class_channel import Channel
from class_challenge import Challenge
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
        self.bounty = BOUNTY_START_POINTS
        self.completed_unspecific_challenges = []  # ids
        self.places_visited = []  # ids
        self.completed_challenges = []  # Challenge Objects
        self.open_challenges = []
        self.normal_mode_time = (datetime.datetime.now() + SPECIFIC_PERIOD).time()
        self.last_zone = START_ZONE
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

    def generate_specific_challenge(self, zone: int, delta: int) -> Challenge:
        time = datetime.datetime.now().time()

        # Randomly select incomplete challenge (int)
        place = random.randint(0, specific_challenges_amount - 1)
        challenge = generate_specific_challenge(place, zone, delta)
        while place in self.places_visited or (time > PERIMETER_TIME and (not challenge.in_perim or challenge.kaff > PERIM_MAX_KAFF)):
            place = random.randint(0, specific_challenges_amount - 1)
            challenge = generate_specific_challenge(place, zone, delta)

        # Generate challenge and return it
        return challenge
        
    def generate_unspecific_challenge(self, zone: int, delta: int) -> Challenge:
        time = datetime.datetime.now().time()

        # Randomly select incomplete challenge (int)
        index = random.randint(0, unspecific_challenges_amount - 1)
        challenge = generate_unspecific_challenge(index, zone, delta)
        while index in self.completed_unspecific_challenges or (time > PERIMETER_TIME and (not challenge.in_perim or challenge.kaff > PERIM_MAX_KAFF)):
            index = random.randint(0, unspecific_challenges_amount - 1)
            challenge = generate_unspecific_challenge(index, zone, delta)

        # Generate challenge and return it
        return challenge

#    def generate_place_challenge(self, zone: int) -> Challenge:
#        # Randomly select unvisited place (int)
#        place = random.randint(0, specific_challenges_amount - 1)
#        if len(self.places_visited) == specific_challenges_amount:
#            self.places_visited = []
#            print(f'Oh shit, ran out of places, aww man, team {self}')
#        while place in self.places_visited:
#            place = random.randint(0, specific_challenges_amount - 1)
#
#        # Generate challenge and return it
#        return generate_specific_challenge(place, zone)

    '''
    def generate_creative_challenge(self) -> Challenge:
        # Randomly select incomplete challenge (int)
        index = random.randint(0, unspecific_challenges_amount - 1)
        while index in self.completed_unspecific_challenges:
            index = random.randint(0, unspecific_challenges_amount - 1)

        # Generate challenge and return it
        return generate_creative_challenge(index)
    '''

    def generate_challenges(self, zone: int, delta: int) -> None:
        time = datetime.datetime.now().time()
        self.last_challenge_generation = time

        if (time < self.normal_mode_time):
            self.open_challenges = [self.generate_specific_challenge(zone, delta)]
            for _ in range(2):
                challenge = self.generate_specific_challenge(zone, delta)
                while challenge in self.open_challenges:
                    challenge = self.generate_specific_challenge(zone, delta)
                self.open_challenges.append(challenge)

        elif (time < UNSPECIFIC_TIME):
            self.open_challenges = [self.generate_specific_challenge(zone, delta), None, self.generate_unspecific_challenge(zone, delta)]
    
            # Randomly select a specific challenge that's neither completed nor active
            challenge = self.generate_specific_challenge(zone, delta)
            while challenge == self.open_challenges[0]:
                challenge = self.generate_specific_challenge(zone, delta)
    
            # Append the challenge to the open challenges
            self.open_challenges[1] = challenge

        else:
            self.open_challenges = [self.generate_unspecific_challenge(zone, delta)]
            for _ in range(2):
                challenge = self.generate_unspecific_challenge(zone, delta)
                while challenge in self.open_challenges:
                    challenge = self.generate_unspecific_challenge(zone, delta)
                self.open_challenges.append(challenge)

    def complete_challenge(self, index: int, delta: int) -> None:
        # Index should be 1, 2 or 3
        completed_challenge = self.open_challenges[index]

        # Save challenge completion
        self.completed_challenges.append(completed_challenge)

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

        # Backup
        self.backup()  # TODO: Does this work?

    def grant_points(self, points: int) -> None:
        self.points += points
        self.bounty += int(points * BOUNTY_PERCENTAGE)

    def deduct_points(self, points) -> None:
        self.grant_points(-points)

    def reroll_challenges(self, delta: int) -> str:
        if datetime.datetime.now().time() < UNSPECIFIC_TIME:
            print("Cant reroll challenges, too early")
            return "Ihr chönd no kein reroll mache, es isch nonig Ziit."
        elif self.last_challenge_generation > UNSPECIFIC_TIME:
            print("Cant reroll challenges, this team already exclusively has unspecific challenges")
            return "Ihr chönd nöd rerolle, ihr händ scho nur unspezifischi"
        else:
            self.generate_challenges(self.last_zone, delta)
            return "wowzers"

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

    def return_challenges(self) -> str:
        out = f"# Eui Challenges:\n"
        for num, challenge in enumerate(self.open_challenges):
            out += f"### {num + 1}: {challenge}\n"
        out += f'\n\n-=[ **Aktuells Chopfgeld**: {self.bounty} Pünkt ]=-\n'
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
