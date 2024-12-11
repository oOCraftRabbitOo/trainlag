import datetime
from add_datetime import *

# ==============
# = Main Stuff =
# ==============
# team compositions and channels
TEAM_FILE = 'teams.json'
PLAYER_FILE = 'players.json'
GENERAL_CHANNEL = 1312741650820501504 # channel for game info

# point calculation
RELATIVE_STANDARD_DEVIATION = 0.05
POINTS_PER_KAFFNESS = 60
POINTS_PER_GRADE = 20
POINTS_PER_WALKING_MINUTE = 10
POINTS_PER_STATIONARY_MINUTE = 10
POINTS_PER_TRAVEL_MINUTE = 10 # currently useless
START_ZONE = 110

# underdog system
UNDERDOG_MULTIPLYER_PER_1000 = 0.25
UNDERDOG_STARTING_DIFFERENCE = 1000

# zonic kaffness
POINTS_PER_CONNECTED_ZONE_LESS_THAN_6 = 15
POINTS_PER_BAD_CONNECTIVITY_INDEX = 25
POINTS_FOR_NO_TRAIN = 30
POINTS_FOR_MONGUS = 50

# emoji dictionary
EMOJI = {1: ":first_place:", 2: ":second_place:", 3: ":third_place:", 4: ":four:", 5: ":five:", 6: ":six:", 7: ":seven:", 8: ":eight:", 9: ":nine:", "last": ":poo:"}

# number of catchers
NUM_CATCHERS = 2

# bounty system
BOUNTY_BASE_POINTS = 0
BOUNTY_START_POINTS = 500 # Now, catchers get this at the beginning
BOUNTY_PERCENTAGE = 1/3

# perimeter system
PERIM_MAX_KAFF = 4
PERIM_MAX_TRAVEL_MINUTES = 30

# Challenge Choice
NORMAL_PERIOD_NEAR = (0, 25)
NORMAL_PERIOD_FAR = (40, 70)
REGIO_RATIO = 0.3

# times
# Specific Period -> Normal Period -> Perimeter Period -> Zurich Period -> End Game Period
GAME_START_TIME = datetime.time(hour=9, minute=0)
GAME_OVER_TIME = datetime.time(hour=17, minute=0)

END_GAME_PERIOD = datetime.timedelta(minutes=45)
END_GAME_START_TIME = subtract_datetimes(GAME_OVER_TIME, END_GAME_PERIOD)  # GAME_OVER_TIME - END_GAME_PERIOD

ZURICH_PERIOD = datetime.timedelta(hours=2, minutes=0)
ZURICH_START_TIME = subtract_datetimes(END_GAME_START_TIME, ZURICH_PERIOD)

PERIMETER_PERIOD = datetime.timedelta(hours=1, minutes=30)
PERIMETER_START_TIME = subtract_datetimes(ZURICH_START_TIME, PERIMETER_PERIOD)

SPECIFIC_PERIOD = datetime.timedelta(minutes=15, seconds=0)

NORMAL_START_TIME = add_datetimes(GAME_START_TIME, SPECIFIC_PERIOD)

TIME_INACCURACY = 7  # +- how many minutes the time reading may be off

# Old Times (for the olden days)
UNSPECIFIC_TIME = datetime.time(hour=22, minute=52)
PERIMETER_TIME = datetime.time(hour=20, minute=46)
