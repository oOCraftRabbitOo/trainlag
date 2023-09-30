import random
import numpy as np
from config import *
import pandas as pd

# Load CSV for Zonic Kaffness
zonic_kaffness_sheet = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRhpVCJ3bps5pBJ0nhmjmSlcDndXXbE-65rbxvfHjtq_9ylBL9fsMyC5fSfBmarR7DSfpwwgTy_qiKc/pub?gid=0&single=true&output=csv")

def calculate_zonic_kaffness(row):
    connected_zones = int(row['num conn zones'])
    connections = int(row['num connections'])
    train_through = True if row['train through'] == "TRUE" else False
    mongus = True if row['Mongus'] == "TRUE" else False
    
    zonic_kaffness = (6 - connected_zones) * 15 + (6 - connections ** 0.5) * 25 + (0 if train_through else 30) + (50 if mongus else 0)
    
    return zonic_kaffness

# Create an empty dictionary to store the results
zonic_kaffness_dict = {int(row['Zone']): calculate_zonic_kaffness(row)}


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


def pointcalc_place(kaffness: int, grade: int) -> int:
    points = POINTS_PER_KAFFNESS * kaffness + POINTS_PER_GRADE * grade
    return randomly_adjust(points)

def pointcalc_zone(zone: int) -> int:
    return 0

def pointcalc_specific(kaffness: int, grade: int, challenge_points: int, ppr: int, reps: int, zone: int):
    points = 0
    points += POINTS_PER_KAFFNESS * kaffness
    points += POINTS_PER_GRADE * grade
    points += pointcalc_zone(zone)
    points += reps * ppr
    points += challenge_points
    return randomly_adjust(points)
