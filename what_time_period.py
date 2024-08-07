import datetime
from config import *
from add_datetime import *
import random

# Specific Period -> Normal Period -> Perimeter Period -> Zurich Period -> End Game Period


def what_time_period(time: datetime.time = None, enable_random=True):
    if time is None:
        time = datetime.now().time()

    if time >= GAME_START_TIME and time < NORMAL_START_TIME:
        return "Specific Period"
    elif time < GAME_START_TIME:
        return "Pre Game"
    elif time >= GAME_OVER_TIME:
        return "Post Game"

    if enable_random:
        random_seconds = random.randint(-60 *
                                        TIME_INACCURACY, 60*TIME_INACCURACY)
        time = add_datetimes(time, datetime.timedelta(seconds=random_seconds))

    if time >= END_GAME_START_TIME:
        return "End Game Period"
    elif time >= ZURICH_START_TIME:
        return "Zurich Period"
    elif time >= PERIMETER_START_TIME:
        return "Perimeter Period"
    return "Normal Period"


if __name__ == "__main__":
    print(f"The game ends at {GAME_OVER_TIME}.")
    print(f"Therefore the endgame starts at {END_GAME_START_TIME}, the Zurich Period at {
          ZURICH_START_TIME} and the perimeter period at {PERIMETER_START_TIME}")
    test_cases = [
        (datetime.time(16, 59), "End Game Period"),
        (datetime.time(17, 0), "Post Game"),
        (datetime.time(16, 45), "End Game Period"),
        (datetime.time(16, 30), "End Game Period"),
        (datetime.time(15, 45), "Zurich Period"),
        (datetime.time(15, 30), "Zurich Period"),
        (datetime.time(13, 31), "Perimeter Period"),
        (datetime.time(13, 30), "Perimeter Period"),
        (datetime.time(13, 29), "Unspecific Period"),
        (datetime.time(3, 30), "Pre Game"),
        (datetime.time(9, 10), "Specific Period")
    ]
    for test_case in test_cases:
        print(f"Tested time {test_case[0]} ({test_case[1]}) and got back {
              what_time_period(test_case[0], False)}.")
