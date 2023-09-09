import json

def main():
    file = input('which file should be converted? > ')
    with open(file, 'r') as f:
        teams = json.load(f)
    with open(file + "_old", 'w') as f:
        json.dump(teams, f)

    players = [player for team in teams for player in team["players"]]
    
    teams = [{"name": team["name"], "players": [player["name"] for player in team["players"]], "channel": team["channel"]} for team in teams]
    with open(file, 'w') as f:
        json.dump(teams, f)
    file = input('What should the player file be called? > ')
    with open(file, 'w') as f:
        json.dump(players, f)

if __name__ == '__main__':
    main()
