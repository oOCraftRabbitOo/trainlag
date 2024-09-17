import datetime

# team compositions and channels
TEAM_FILE = 'test_teams.json'
PLAYER_FILE = 'test_players.json'
GENERAL_CHANNEL = 1113388616845107262 

# point calculation
RELATIVE_STANDARD_DEVIATION = 0.05
POINTS_PER_KAFFNESS = 90
POINTS_PER_GRADE = 30
ZONEABLE_AND_ZONED_BONUS = 50
POINTS_PER_WALKING_MINUTE = 10
POINTS_PER_STATIONARY_MINUTE = 10
POINTS_PER_TRAVEL_MINUTE = 5
START_ZONE = 121

# zonic kaffness
POINTS_PER_CONNECTED_ZONE_LESS_THAN_6 = 15
POINTS_PER_BAD_CONNECTIVITY_INDEX = 25
POINTS_FOR_NO_TRAIN = 30
POINTS_FOR_MONGUS = 50

# emoji dictionary
EMOJI = {1: ":first_place:", 2: ":second_place:", 3: ":third_place:", 4: ":four:", 5: ":five:", 6: ":six:", 7: ":seven:", 8: ":eight:", 9: ":nine:", "last": ":poo:"}

# number of catchers
NUM_CATCHERS = 2

# times
UNSPECIFIC_TIME = datetime.time(hour=15, minute=30)
TSUERI_TIME = datetime.time(hour=14, minute=30)
SPECIFIC_PERIOD = datetime.timedelta(minutes=15)

GLOBAL_SHOPS = ["Wetzikon", "Horgen", "Winterthur HB"]
START_LOCATION_PRIZE = 500
GLOBAL_SHOP_PRIZE = 400
FINAL_SHOPS_PRIZE = 300
