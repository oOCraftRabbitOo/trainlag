from load_challenges import generate_creative_challenge, generate_place_challenge, creative_challenges_amount, place_challenges_amount
import random


class Team:
    def __init__(self, players, channel_id, name):
        self.players = players
        self.channel_id = channel_id
        self.name = name
        self.points = 0
        self.completed_creative_challenges = []  # ids
        self.places_visited = []  # ids
        self.completed_challenges = []  # Challenge Objects
        self.open_challenges = []
        self.generate_challenges()

    def __str__(self):
        names = ""
        for player in self.players:
            names += player + " "
        return f'Team {self.name} ({names[:-1]})'  # Remove last space and return

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
        self.points += completed_challenge.points

        # Generate new challenges
        self.generate_challenges()

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
