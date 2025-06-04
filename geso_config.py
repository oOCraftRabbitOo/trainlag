import datetime
from add_datetime import *
from normal_config import *

TEAM_FILE = 'geso_teams.json'
PLAYER_FILE = 'geso_players.json'
GENERAL_CHANNEL = 1359589059806236712 # channel for game info

NUM_CATCHERS = 2


NORMAL_PERIOD_NEAR = (0, 25)
NORMAL_PERIOD_FAR = (35, 55)

GAME_START_TIME = datetime.time(hour=14, minute=15)
GAME_OVER_TIME = datetime.time(hour=19, minute=0)

END_GAME_PERIOD = datetime.timedelta(minutes=40)
END_GAME_START_TIME = subtract_datetimes(GAME_OVER_TIME, END_GAME_PERIOD)  # GAME_OVER_TIME - END_GAME_PERIOD

ZURICH_PERIOD = datetime.timedelta(hours=1, minutes=30)
ZURICH_START_TIME = subtract_datetimes(END_GAME_START_TIME, ZURICH_PERIOD)

PERIMETER_PERIOD = datetime.timedelta(hours=1, minutes=20)
PERIMETER_START_TIME = subtract_datetimes(ZURICH_START_TIME, PERIMETER_PERIOD)

SPECIFIC_PERIOD = datetime.timedelta(minutes=15, seconds=0)

NORMAL_START_TIME = add_datetimes(GAME_START_TIME, SPECIFIC_PERIOD)
