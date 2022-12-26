import random
import pandas as pd
from pointcalc import pointcalc
from class_challenge import Challenge

# Load the CSV file from the Google Sheet
challenge_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/10EaV2iZUAP8oZH7PLdoWGx9lQPvvN3Hfu7jH2zqKPv4/export?format=csv')

# Create empty challenge dict to fill with all challenges (No, I won't put the following code into a list operation.)
challenges = {}

for index, row in challenge_sheet.iterrows():
    description = row['description']
    # Generate a new random number between 1 and 10
    random_number = random.randint(row['min'], row['max'])

    # Select a new random entry from the list
    zones = [116, 115, 161, 162, 113, 114, 124, 160, 163, 118, 117, 112, 123, 120, 164, 111, 121, 122, 170, 171, 154, 110, 173, 172, 135, 131, 130, 155, 150, 156, 151, 152, 153, 181, 180, 133, 143, 142, 141, 140, 130, 132, 134]
    random_zone = random.choice(zones)

    s_bahn_zones = [132, 110, 151, 180, 120, 181, 155, 133, 156, 117, 121, 141, 142, 134, 112, 154]
    random_s_bahn_zone = random.choice(s_bahn_zones)

    # Create a dictionary that maps placeholders to values
    placeholders = {
        '%r': random_number,
        '%z': random_zone,
        '%s': random_s_bahn_zone
    }
    # Calculate points
    points = pointcalc(row['points'], row['ppr'], random_number, row['fixed'])

    # Substitute the placeholders using the replace method
    for placeholder, value in placeholders.items():
        description = description.replace(placeholder, str(value))

    title = row['title']
    description = f"{description} \033[1m{points} Pünkt\033[0m"

    challenges[index] = Challenge(title, description, points, index)
    print(challenges[index], end="\n\n")

