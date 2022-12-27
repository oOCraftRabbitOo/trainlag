import random
import numpy as np


def randomly_adjust(value, relative_standard_deviation=0.1) -> int:
    """
    Takes in a value and adds/subtracts some amount of points randomly to hopefully prevent ties
    """

    # Calculate the standard deviation based on 10% of the input value
    std_dev = value * relative_standard_deviation

    # Generate a random value using a Gaussian normal distribution with the calculated standard deviation
    points = np.random.normal(value, std_dev)

    # Cast the value to an integer
    points = int(points)

    return points


def pointcalc_creative(points, ppr, random_number, fixed) -> int:
    # TODO: remove the try except stuff
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


def pointcalc_place(kaffness, grade) -> int:
    points = 90 * kaffness + 20 * grade
    return randomly_adjust(points)