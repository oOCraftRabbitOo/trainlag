import datetime
from config import *
from add_datetime import *
import random

debug_time = False  # Replaces the check for the current time with a predefined time


def time_now() -> datetime.time:
    if debug_time:
        return debug_time
    return datetime.datetime.now().time()


# Specific Period -> Normal Period -> Perimeter Period -> Zurich Period -> End Game Period
def what_time_period(time: datetime.time = None, enable_random: bool = True):
    if time is None:
        time = time_now()

    if enable_random:
        random_seconds = random.randint(-60*TIME_INACCURACY, 60*TIME_INACCURACY)
        time = add_datetimes(time, datetime.timedelta(seconds=random_seconds))

    if time >= GAME_OVER_TIME:
        return "Post Game"
    elif time >= END_GAME_START_TIME:
        return "End Game Period"
    elif time >= ZURICH_START_TIME:
        return "Zurich Period"
    elif time >= PERIMETER_START_TIME:
        return "Perimeter Period"
    elif time >= NORMAL_START_TIME:
        return "Normal Period"
    elif time >= GAME_START_TIME:
        return "Specific Period"
    return "Pre Game"


def maximum_perimeter_distance(time: datetime.time):
    if time < PERIMETER_START_TIME:
        return 69420  # Big number
    return map_datetime_to_value(time, PERIMETER_START_TIME, ZURICH_START_TIME, 45, 20)


def maximum_kaffness(time: datetime.time):
    return map_datetime_to_value(time, PERIMETER_START_TIME, ZURICH_START_TIME, 6.5, 3)


def zurich_probability(time: datetime.time = None):  # Returns a %-Chance of a specific challenge being a Zurich challenge depending on time
    if time is None:
        time = time_now()

    if time < ZURICH_START_TIME:
        return 0
    return map_datetime_to_value(time, PERIMETER_START_TIME, ZURICH_START_TIME, 60, 120)


if __name__ == "__main__":
    print(f"The game ends at {GAME_OVER_TIME}.")
    print(f"Therefore the endgame starts at {END_GAME_START_TIME}, the Zurich Period at {ZURICH_START_TIME} and the perimeter period at {PERIMETER_START_TIME}")
    test_cases = [
        (datetime.time(16, 59), "End Game Period"),
        (datetime.time(17, 0), "Post Game"),
        (datetime.time(16, 45), "End Game Period"),
        (datetime.time(16, 30), "End Game Period"),
        (datetime.time(15, 45), "Zurich Period"),
        (datetime.time(15, 30), "Zurich Period"),
        (datetime.time(13, 31), "Perimeter Period"),
        (datetime.time(13, 30), "Perimeter Period"),
        (datetime.time(13, 29), "Normal Period"),
        (datetime.time(3, 30), "Pre Game"),
        (datetime.time(9, 10), "Specific Period")
    ]
    for test_case in test_cases:
        print(f"Tested time {test_case[0]} ({test_case[1]}) and got back {what_time_period(test_case[0], False)}.")