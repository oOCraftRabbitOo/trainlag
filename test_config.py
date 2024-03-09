import datetime

# team compositions and channels
TEAM_FILE = 'test_teams.json'
PLAYER_FILE = 'test_players.json'
GENERAL_CHANNEL = 1113388616845107262 

# point calculation
RELATIVE_STANDARD_DEVIATION = 0.05
POINTS_PER_KAFFNESS = 80
POINTS_PER_GRADE = 20
POINTS_PER_WALKING_MINUTE = 10
POINTS_PER_STATIONARY_MINUTE = 10
POINTS_PER_TRAVEL_MINUTE = 5
START_ZONE = 121

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
NUM_CATCHERS = 3

# bounty system
BOUNTY_BASE_POINTS = 100
BOUNTY_START_POINTS = 250
BOUNTY_PERCENTAGE = 0.25

# perimeter system
PERIM_MAX_KAFF = 4

# times
UNSPECIFIC_TIME = datetime.time(hour=10, minute=52)
SPECIFIC_PERIOD = datetime.timedelta(minutes=1)
PERIMETER_TIME = datetime.time(hour=11, minute=15)
