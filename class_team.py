from load_challenges import generate_creative_challenge, generate_place_challenge, creative_challenges_amount, place_challenges_amount
from class_player import Player
from discord_constants import *
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
        self.completed_creative_challenges = []  # ids
        self.places_visited = []  # ids
        self.completed_challenges = []  # Challenge Objects
        self.open_challenges = []
        self.generate_challenges()
        self.backup()

    def __str__(self):
        names = ""
        for player in self.players:
            names += player.name + " "
        if self.is_catcher:
            return f'Team {self.name} ({names[:-1]}) [Fänger]'
        return f'Team {self.name} ({names[:-1]})'  # Remove last space and return

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
        self.points += completed_challenge.points  # TODO: use grant_points

        # Generate new challenges
        self.generate_challenges()

        # Backup
        self.backup()  # TODO: Does this work?

    def grant_points(self, points):
        self.points += points

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


def generate_teams(num_catchers=2):
    # TODO: allgemeiner für Teams im fertige Spiil
    teams = [Team([Nelio], CHANNELS[0], "alpha"),
             Team([Aurele], CHANNELS[1], "bravo"),
             Team([Julian], CHANNELS[2], "charlie"),
             Team([Timo], CHANNELS[3], "delta")]

    # Chose catchers
    catchers = random.sample(teams, num_catchers)
    for team in catchers:
        team.is_catcher = True

    return teams


def print_teams(teams):
    # Only for debug purposes, prints out the Teams, duh
    print("---------")
    print("The Teams:")
    for team in teams:
        print(team)
    print("---------")


if __name__ == "__main__":
    teams = generate_teams()
    print_teams(teams)
