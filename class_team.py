from load_challenges import generate_creative_challenge, generate_place_challenge, creative_challenges_amount, place_challenges_amount
from class_player import Player
from config import *
import random
import pickle
import datetime
import glob
import os


class Team:
    def __init__(self, players, channel_id, name, is_catcher=False):
        self.players = players
        self.channel_id = channel_id
        self.name = name
        self.is_catcher = is_catcher
        self.points = 0
        self.bounty = BOUNTY_BASE_POINTS
        self.completed_creative_challenges = []  # ids
        self.places_visited = []  # ids
        self.completed_challenges = []  # Challenge Objects
        self.open_challenges = []
        self.generate_challenges()
        self.backup()

    def deb_str(self) -> str:
        names = ""
        for player in self.players:
            names += player.name + " "
        strink = f'--\n\nTeam {self.name}, \nchannel: {self.channel_id}, \npoints: {self.points}, \ncompCChals: {self.completed_creative_challenges}, \nplaces visited: {self.places_visited}, \nopenChals: {self.open_challenges}, \ncompChals: {self.completed_challenges}, \nmembers: ({names[:-1]})'
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

    def generate_place_challenge(self):
        # Randomly select unvisited place (int)
        place = random.randint(0, place_challenges_amount - 1)
        while place in self.places_visited:
            place = random.randint(0, place_challenges_amount - 1)

        # Generate challenge and return it
        return generate_place_challenge(place)

    def generate_creative_challenge(self):
        # Randomly select incomplete challenge (int)
        index = random.randint(0, creative_challenges_amount - 1)
        while index in self.completed_creative_challenges:
            index = random.randint(0, creative_challenges_amount - 1)

        # Generate challenge and return it
        return generate_creative_challenge(index)

    def generate_challenges(self):
        self.open_challenges = [self.generate_place_challenge(), self.generate_creative_challenge()]
        if random.random() < 0.5:
            # Randomly select a place challenge that's neither completed nor active
            challenge = self.generate_place_challenge()
            while challenge == self.open_challenges[0]:
                challenge = self.generate_place_challenge()
        else:
            # Randomly select a creative challenge that's neither completed nor active
            challenge = self.generate_creative_challenge()
            while challenge == self.open_challenges[1]:
                challenge = self.generate_creative_challenge()

        # Append the challenge to the open challenges
        self.open_challenges.append(challenge)

    def complete_challenge(self, index):
        # Index should be 1, 2 or 3
        completed_challenge = self.open_challenges[index]

        # Save challenge completion
        self.completed_challenges.append(completed_challenge)

        if completed_challenge.type == 'creative':
            self.completed_creative_challenges.append(completed_challenge.id)
        elif completed_challenge.type == 'place':
            self.places_visited.append(completed_challenge.id)

        # Grant points
        self.grant_points(completed_challenge.points)

        # Generate new challenges
        self.generate_challenges()

        # Backup
        self.backup()  # TODO: Does this work?

    def grant_points(self, points):
        self.points += points
        self.bounty += int(points * BOUNTY_PERCENTAGE)

    def deduct_points(self, points):
        self.grant_points(-points)

    def uncomplete_challenge(self, index):
        # Get challenge to uncomplete and remove it from completed challenges
        uncompleted_challenge = self.completed_challenges.pop(index)

        if uncompleted_challenge.type == 'creative':
            self.completed_creative_challenges.remove(uncompleted_challenge.id)
        elif uncompleted_challenge.type == 'place':
            self.places_visited.remove(uncompleted_challenge.id)

        # Deduct points
        self.deduct_points(uncompleted_challenge.points)

    def backup(self):
        # TODO: test
        # Get the current date and time
        now = datetime.datetime.now()

        # Generate a filename using the current date and time
        file = f'backups/{self.name}_{now:%Y-%m-%d_%H-%M-%S}.pickle'
        # Open a file in binary write mode
        with open(file, 'wb') as f:
            # Serialize the object and write it to the file
            pickle.dump(self, f)

    def load(self, file=None):
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
        self.completed_creative_challenges = loaded_team.completed_creative_challenges
        self.places_visited = loaded_team.places_visited
        self.completed_challenges = loaded_team.completed_challenges
        self.open_challenges = loaded_team.open_challenges

    def switch_roles(self):
        if self.is_catcher:
            self.is_catcher = False
            self.generate_challenges()
        else:
            self.is_catcher = True
            self.open_challenges = []
        self.backup()

    def return_challenges(self):
        out = "**Eui Challenges:** \n-------------------------------------------- \n"
        for challenge in self.open_challenges:
            out += f"{challenge}\n-------------------------------------------- \n"
        return out


def generate_teams(num_catchers=2) -> list:
    teams = [Team([CraftRabbit], CHANNELS[0], "alpha"),
         Team([CraftRibbit], CHANNELS[1], "bravo"),
         Team([CroftRabbit], CHANNELS[2], "charlie"),
         Team([KaiJu], CHANNELS[3], "delta"),
         Team([Volvox], CHANNELS[4], "echo")]

    # Choose catchers
    catchers = random.sample(teams, num_catchers)
    for team in catchers:
        team.is_catcher = True

    return teams


def print_teams(teams):
    # Only for debug purposes, prints out the Teams, duh
    print("---------")
    print("The Teams:")
    for team in teams:
        print(team.deb_str())
    print("---------")


if __name__ == "__main__":
    teams = generate_teams()
    print_teams(teams)
