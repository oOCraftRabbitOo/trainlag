import random
import numpy as np
from test_config import *


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
    return zonic_kaffness_dict[zone]

def pointcalc_specific(kaffness: int, grade: int, challenge_points: int, ppr: int, reps: int, zone: int):
    points = 0
    points += POINTS_PER_KAFFNESS * kaffness
    points += POINTS_PER_GRADE * grade
    points += pointcalc_zone(zone)
    points += reps * ppr
    points += challenge_points
    return randomly_adjust(points)
