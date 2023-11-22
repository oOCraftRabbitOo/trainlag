import datetime

# team compositions and channels
TEAM_FILE = 'test_teams.json'
PLAYER_FILE = 'test_players.json'
GENERAL_CHANNEL = 1113388616845107262 

# point calculation
RELATIVE_STANDARD_DEVIATION = 0.1
POINTS_PER_KAFFNESS = 90
POINTS_PER_GRADE = 20

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

# times
UNSPECIFIC_TIME = datetime.time(hour=16, minute=30)
