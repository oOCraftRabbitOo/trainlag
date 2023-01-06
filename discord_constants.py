from class_player import Player

# Players
Nelio = Player("Nelio", 289453000370421760)
Aurele = Player("Aurèle", 334204120946704385)
Julian = Player("Julian", 299564881135403008)
Timo = Player("Timo", 299564881135403008)

ALL_PLAYERS = [Nelio, Aurele, Julian, Timo]
PLAYERS_BY_ID = {player.id: player for player in ALL_PLAYERS}

# Channel ids
CHANNELS = [1058827059130011708, 1058827074569257070, 1058827090973184070, 1058827105166700584, 1058827120442359920, 1058827148087009410, 1058827175962361926]
