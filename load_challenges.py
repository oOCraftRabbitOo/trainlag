import random
import pandas as pd
from pointcalc import pointcalc_creative, pointcalc_place
from class_challenge import Challenge

# Load the CSV files from the Google Sheets
challenge_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/10EaV2iZUAP8oZH7PLdoWGx9lQPvvN3Hfu7jH2zqKPv4/export?format=csv')
kaffs_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/13DlG2BSQfolPCsoj2LBREeIUgThji_zgeE_q-gHQSL4/export?format=csv')

# For both sheets generate their lengths = amount of different challenges
creative_challenges_amount = len(challenge_sheet)
place_challenges_amount = len(kaffs_sheet)

# Generate zone lists
zones = [116, 115, 161, 162, 113, 114, 124, 160, 163, 118, 117, 112, 123, 120, 164, 111, 121, 122, 170, 171, 154, 110, 173, 172, 135, 131, 130, 155, 150, 156, 151, 152, 153, 181, 180, 133, 143, 142, 141, 140, 130, 132, 134]
s_bahn_zones = [132, 110, 151, 180, 120, 181, 155, 133, 156, 117, 121, 141, 142, 134, 112, 154]


def generate_creative_challenge(index, specific_zone_chance=0.25):
    row = challenge_sheet.loc[index]
    description = row['description']
    # Generate a new random number between 1 and 10
    random_number = random.randint(row['min'], row['max'])

    # Select a new random entry from the zone lists
    random_zone = random.choice(zones)
    random_s_bahn_zone = random.choice(s_bahn_zones)

    # Create a dictionary that maps placeholders to values
    placeholders = {
        '%r': random_number,
        '%z': random_zone,
        '%s': random_s_bahn_zone
    }
    # Calculate points
    points = pointcalc_creative(row['points'], row['ppr'], random_number, row['fixed'])

    # Substitute the placeholders using the replace method
    for placeholder, value in placeholders.items():
        description = description.replace(placeholder, str(value))

    title = row['title']

    if random.random() < specific_zone_chance and row['zoneable'] == 1:
        points *= 2
        description = f"{description} Damit ihr Pünkt überchömed, mached das i de Zone {random.choice(zones)}. \033[1m{points} Pünkt\033[0m"
    else:
        description = f"{description} \033[1m{points} Pünkt\033[0m"

    return Challenge(title, description, points, index, "creative")


def generate_place_challenge(index):
    row = kaffs_sheet.loc[index]

    # Calculate points
    kaffness = row['Kaffskala']
    grade = row['Güteklasse']
    grade = (int(grade) if isinstance(grade, int) else kaffness)  # Ignores empty cells, '-' and '?'
    points = pointcalc_place(kaffness, grade)

    # Generate title and description
    title = f"Usflug uf {row['Ort']}"
    description = f"Gönd nach {row['Ort']}. \033[1m{points} Pünkt\033[0m"

    return Challenge(title, description, points, index, "place")


if __name__ == "__main__":
    # Print all place challenges, with one random configuration
    for index in range(place_challenges_amount):
        print(generate_place_challenge(index), end="\n\n")

    # Print every creative challenge, with one random configuration
    for index in range(creative_challenges_amount):
        print(generate_creative_challenge(index), end="\n\n")





