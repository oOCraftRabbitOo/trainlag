from class_player import Player

# ==============
# = Main Stuff =
# ==============
''' Uskommentiert zum teste
# Players
Nelio = Player("Nelio", 289453000370421760)
Aurele = Player("Aurèle", 334204120946704385)
Julian = Player("Julian", 299564881135403008)
Timo = Player("Timo", 319781199910535170)

Leandro = Player("Leandro", 1079855346979442850)
Anna = Player("Anna", 514111562483630080)
Frederic = Player("Frederic", 774661552603267132)
Dennis = Player("Dennis", 713069751164731463)
Finn = Player("Finn", 824684410455851028)
Elric = Player("Elric", 707269592174690354)
Ciril = Player("Ciril", 598945447780024360)
Jonatan = Player("Jonatan", 618114675720323086)
Simon = Player("Simon", 529765758192975872)
Marin = Player("Marin", 709377143276175421)
#Max = Player("Max", 618394223846227969)
Lea = Player("Lea", 724951300806279210)
Moritz = Player("Moritz", 428900377195315231)
Noah = Player("Noah", 1067376649953357894)
Lucy = Player("Lucy", 607887838658297874)
Christopher = Player("Christopher", 803320902645317653)


ALL_PLAYERS = [Nelio, Aurele, Julian, Timo, Leandro, Anna, Frederic, Dennis, Finn, Elric, Ciril, Jonatan, Simon, Marin, Lea, Moritz, Noah, Lucy, Christopher]
PLAYERS_BY_ID = {player.id: player for player in ALL_PLAYERS}

teams = [Team([Nelio, Anna], CHANNELS[0], "alpha"),
         Team([Aurele, Leandro], CHANNELS[1], "bravo"),
         Team([Julian, Noah], CHANNELS[2], "charlie"),
         Team([Simon, Ciril, Elric], CHANNELS[4], "echo"),
         Team([Lucy, Finn, Moritz], CHANNELS[5], "foxtrot"),
         Team([Timo, Marin, Frederic], CHANNELS[6], "guete abig"),
         Team([Jonatan, Lea, Christopher], CHANNELS[7], "h0i")]

# Channel ids
CHANNELS = [1058827059130011708, 1058827074569257070, 1058827090973184070, 1058827105166700584, 1058827120442359920, 1058827148087009410, 1058827175962361926, 1081228497206386708]
GENERAL_CHANNEL = 1080162053202923621


# Emoji Dictionary
EMOJI = {1: ":first_place:", 2: ":second_place:", 3: ":third_place:", 4: ":four:", 5: ":five:", 6: ":six:", 7: ":seven:", 8: ":eight:", 9: ":nine:", "last": ":poo:"}
'''

# ==============
# = Test Stuff =
# ==============
# Players
"""
CraftRabbit = Player("CraftRabbit", 289453000370421760)
DJOkovic = Player("DJOkovic", 334204120946704385)
Metrogamer = Player("Metrogamer", 299564881135403008)
KaiJu = Player("KaiJu", 319781199910535170)
CroftRabbit = Player("CroftRabbit", 688054074637156625)
CraftRibbit = Player("CraftRibbit", 505760247789387776)
Mötrogamer = Player("Mötrogamer", 1113465756856893462)
SkribblMan = Player("SkribblMan", 796762489592741948)
MinecraftGamer = Player("MinecraftGamer", 863153180300017695)
xXWtfIhrHendKeiHobbysIhrMonksXx = Player("xXWtfIhrHendKeiHobbysIhrMonksXx", 714444077789347860)
Volvox = Player("Volvox", 354932090594394113)


ALL_PLAYERS = [CraftRabbit, DJOkovic, Metrogamer, KaiJu, CroftRabbit, CraftRibbit, Mötrogamer, SkribblMan, MinecraftGamer, xXWtfIhrHendKeiHobbysIhrMonksXx, Volvox]
PLAYERS_BY_ID = {player.id: player for player in ALL_PLAYERS}

'''
teams = [Team([CraftRabbit], CHANNELS[0], "alpha"),
         Team([CraftRibbit], CHANNELS[1], "bravo"),
         Team([CroftRabbit], CHANNELS[2], "charlie"),
         Team([KaiJu], CHANNELS[3], "delta"),
         Team([Volvox], CHANNELS[4], "charlie")]
'''

# Channel ids
CHANNELS = [1116691418904281128, 1116691484213772381, 1116691495072841778, 1116691505374044190, 1116691516774158488, 1116691527297662986, 1116691539507302457, 1116691554036355072]
"""
TEAM_FILE = 'test_teams.json'
GENERAL_CHANNEL = 1113388616845107262

RELATIVE_STANDARD_DEVIATION = 0.1
POINTS_PER_KAFFNESS = 90
POINTS_PER_GRADE = 20

# Emoji Dictionary
EMOJI = {1: ":first_place:", 2: ":second_place:", 3: ":third_place:", 4: ":four:", 5: ":five:", 6: ":six:", 7: ":seven:", 8: ":eight:", 9: ":nine:", "last": ":poo:"}

NUM_CATCHERS = 3
BOUNTY_BASE_POINTS = 100
BOUNTY_PERCENTAGE = 0.25