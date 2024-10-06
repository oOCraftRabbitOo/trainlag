import numpy as np
from config import *
import pandas as pd

print('Generating data for point calculation')

# Load CSV for Zonic Kaffness
zonic_kaffness_sheet = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSEz-OcFSz13kGB2Z9iRzLmBkor8R2o7C-tzOSm91cQKt4foAG6iGynlT8PhO3I5Pt5iB_Mj7Bu0BeO/pub?gid=1336941165&single=true&output=csv")
distance_sheet = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSEz-OcFSz13kGB2Z9iRzLmBkor8R2o7C-tzOSm91cQKt4foAG6iGynlT8PhO3I5Pt5iB_Mj7Bu0BeO/pub?gid=381450010&single=true&output=csv")

def calculate_zonic_kaffness(row):
    connected_zones = int(row['num conn zones'])
    connections = int(row['num connections'])
    train_through = row['train through']
    mongus = row['Mongus']
    
    zonic_kaffness = (6 - connected_zones) * POINTS_PER_CONNECTED_ZONE_LESS_THAN_6 + (6 - connections ** 0.5) * POINTS_PER_BAD_CONNECTIVITY_INDEX + (0 if train_through else POINTS_FOR_NO_TRAIN) + (POINTS_FOR_MONGUS if mongus else 0)
    
    return zonic_kaffness

# Create an empty dictionary to store the results
zonic_kaffness_dict = {int(row['Zone']): calculate_zonic_kaffness(row) for index, row in zonic_kaffness_sheet.iterrows()}
distance_dict: dict[int, dict[int, int]] = {}

for index, row in distance_sheet.iterrows():
    zone_a = int(row['Zone A'])
    zone_b = int(row['Zone B'])
    travel_time = int(row['Travel Time'])

    if zone_a not in distance_dict.keys():
        distance_dict[zone_a] = {}

    distance_dict[zone_a][zone_b] = travel_time

perimeter_distances = {k: distance_dict[k][110] for k in list(set(distance_dict.keys()))}
print(perimeter_distances)

'''perim = []

for k in distance_dict[110].keys():
    if perim.append(distance_dict[110][k] < PERIM_MAX_TRAVEL_MINUTES:
        perim.append(k)

print(perim)'''

def randomly_adjust(value: int) -> int:
    """
    Takes in a value and adds/subtracts some amount of points randomly to hopefully prevent ties
    """

    # Calculate the standard deviation based on 10% of the input value
    std_dev = value * RELATIVE_STANDARD_DEVIATION

    # Generate a random value using a Gaussian normal distribution with the calculated standard deviation
    points = np.random.normal(value, std_dev)

    # Cast the value to an integer
    points = int(points)

    return points


def pointcalc_creative(points: int, ppr: int, random_number: int, fixed: int) -> int:
    # Test if all cells are filled, if not the points are returned as 0
    for i in [points, ppr, random_number, fixed]:
        try:
            i = int(i)
        except ValueError:
            return 0

    # If the points are fixed, they are immediately returned
    if fixed == 1:
        return int(points)

    value = points + ppr * random_number

    return randomly_adjust(value)

def pointcalc_zone(zone: int) -> int:
    return zonic_kaffness_dict[zone]

def pointcalc(kaffness: int,
              grade: int,
              challenge_points: int,
              walking_minutes: int,
              stationary_minutes: int,
              ppr: int,
              reps: int,
              zone: int | None,
              bias: float,
              fixed: bool,
              current_zone: int,
              delta: int,
              zoneable_and_zoned: bool,
              dead_end: bool,
              station_distance: int,
              time_to_hb: int,
              departures: int | None) -> int:
    points = 0
    points += POINTS_PER_KAFFNESS * kaffness
    points += POINTS_PER_GRADE * grade
    points += POINTS_PER_WALKING_MINUTE * walking_minutes
    points += POINTS_PER_STATIONARY_MINUTE * stationary_minutes
    points += pointcalc_zone(zone) if zone is not None else 0
    points += reps * ppr
    points += challenge_points
    points += 100 if zoneable_and_zoned else 0
    # points += distance_dict[current_zone][zone] * POINTS_PER_TRAVEL_MINUTE if zone is not None else 0
    points += distance_dict[current_zone][zone]**1.4 * 3 if zone is not None else 0
    points += 50 if dead_end else 0
    points += int(station_distance/20)
    points += time_to_hb * 5
    if departures is not None:
        points += int((7-departures**(1/3))*32)
    if not fixed:
        points += (points * (delta - UNDERDOG_STARTING_DIFFERENCE) * UNDERDOG_MULTIPLYER_PER_1000 * 0.001) if delta > UNDERDOG_STARTING_DIFFERENCE else 0
    points *= bias
    points = int(points)
    points = points if fixed else randomly_adjust(points)
    return points

if __name__ == "__main__":
    print(*zonic_kaffness_dict.values(), sep='\n')
