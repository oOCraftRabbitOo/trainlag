import random
import pandas as pd
from datetime import date
from pointcalc import pointcalc_creative, pointcalc_place, pointcalc_specific
from class_challenge import Challenge
from numpy import isnan

# Load the CSV files from the Google Sheets
challenge_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/10EaV2iZUAP8oZH7PLdoWGx9lQPvvN3Hfu7jH2zqKPv4/export?format=csv')
kaffs_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/13DlG2BSQfolPCsoj2LBREeIUgThji_zgeE_q-gHQSL4/export?format=csv')
specific_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSEz-OcFSz13kGB2Z9iRzLmBkor8R2o7C-tzOSm91cQKt4foAG6iGynlT8PhO3I5Pt5iB_Mj7Bu0BeO/pub?gid=1687098896&single=true&output=csv')
unspecific_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSEz-OcFSz13kGB2Z9iRzLmBkor8R2o7C-tzOSm91cQKt4foAG6iGynlT8PhO3I5Pt5iB_Mj7Bu0BeO/pub?gid=563784869&single=true&output=csv')

# For both sheets generate their lengths = amount of different challenges
creative_challenges_amount = len(challenge_sheet)
place_challenges_amount = len(kaffs_sheet)
specific_challenges_amount = len(specific_sheet)
unspecific_challenges_amount = len(unspecific_sheet)

# Generate zone lists
zones = [116, 115, 161, 162, 113, 114, 124, 160, 163, 118, 117, 112, 123, 120, 164, 111, 121, 122, 170, 171, 154, 110, 173, 172, 135, 131, 155, 150, 156, 151, 152, 153, 181, 180, 133, 143, 142, 141, 140, 130, 132, 134]
s_bahn_zones = [132, 110, 151, 180, 120, 181, 155, 133, 156, 117, 121, 141, 142, 134, 112, 154]

def generate_specific_challenge(index):
    # get data
    row = specific_sheet.loc[index]
    place = row['Ort']
    challenge = row['Challenge']
    kaffness = row['Kaffskala']
    grade = row['ÖV Güteklasse']
    zone = row['Zone']
    bias_sat = row['Bias Sat']
    bias_sun = row['Bias Sun']
    title_override = row['Title Override']
    challenge_points = row['Points']
    min_reps = row["Min"]
    max_reps = row['Max']
    ppr = row['Points per Repetition']


    # refine data
    if date.today().weekday() == 6:
        bias = bias_sun
    else:
        bias = bias_sat
    if type(title_override) == str:
        title = title_override
    else:
        title = f'Usflug uf {place}'
    if type(challenge) == str:
        raw_description = challenge
    else:
        raw_description = f'Gönd nach {place}.'
    kaffness = int(kaffness)
    grade = (int(grade) if isinstance(grade, int) else kaffness)  # Ignores empty cells, '-' and '?'
    zone = int(zone)
    bias = float(bias)
    challenge_points = int(challenge_points) if not isnan(challenge_points) else 0
    min_reps = int(min_reps) if not isnan(min_reps) else 0
    max_reps = int(max_reps) if not isnan(max_reps) else 0
    reps = random.randint(min_reps, max_reps)
    ppr = int(ppr) if not isnan(ppr) else 0

    # Calculate points
    points = pointcalc_specific(kaffness, grade, challenge_points, ppr, reps, zone)

    # make description
    description = raw_description + f' *{points} Pünkt*'
    description.replace('%r', str(reps))

    # Return challenge
    return Challenge(title, description, points, index, True)


def generate_unspecific_challenge(index):
    return generate_creative_challenge(index, specific_zone_chance=0.0, specific=False)


def generate_creative_challenge(index, specific_zone_chance=0.25, specific='creative'):
    row = unspecific_sheet.loc[index] # ALARM, FUULE CODER (und au vllt e chli dumm) TODO
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
        description = f"{description} Damit ihr Pünkt überchömed, mached das i de Zone {random.choice(zones)}. *{points} Pünkt*"
    else:
        description = f"{description} *{points} Pünkt*"

    return Challenge(title, description, points, index, specific)


def generate_place_challenge(index: int) -> Challenge:
    row = kaffs_sheet.loc[index]

    # Calculate points
    kaffness = row['Kaffskala']
    grade = row['Güteklasse']
    grade = (int(grade) if isinstance(grade, int) else kaffness)  # Ignores empty cells, '-' and '?'
    points = pointcalc_place(kaffness, grade)

    # Generate title and description
    title = f"Usflug uf {row['Ort']}"
    description = f"Gönd nach {row['Ort']}. *{points} Pünkt*"

    return Challenge(title, description, points, index, "place")


if __name__ == "__main__":
    # Print all place challenges, with one random configuration
    for index in range(place_challenges_amount):
        print(generate_place_challenge(index), end="\n\n")

    # Print every creative challenge, with one random configuration
    for index in range(creative_challenges_amount):
        print(generate_creative_challenge(index), end="\n\n")

