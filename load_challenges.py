import random
import pandas as pd
from datetime import date
from pointcalc import pointcalc, distance_dict, perimeter_distances
from class_challenge import Challenge
from numpy import isnan

print('Loading challenges. This may take a while')

# Load the CSV files from the Google Sheets
da_new_kaff_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSEz-OcFSz13kGB2Z9iRzLmBkor8R2o7C-tzOSm91cQKt4foAG6iGynlT8PhO3I5Pt5iB_Mj7Bu0BeO/pub?gid=1687098896&single=true&output=csv')
ortsspezifisch_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSEz-OcFSz13kGB2Z9iRzLmBkor8R2o7C-tzOSm91cQKt4foAG6iGynlT8PhO3I5Pt5iB_Mj7Bu0BeO/pub?gid=1521353166&single=true&output=csv')
regionsspezifisch_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSEz-OcFSz13kGB2Z9iRzLmBkor8R2o7C-tzOSm91cQKt4foAG6iGynlT8PhO3I5Pt5iB_Mj7Bu0BeO/pub?gid=94104575&single=true&output=csv')
unspecific_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSEz-OcFSz13kGB2Z9iRzLmBkor8R2o7C-tzOSm91cQKt4foAG6iGynlT8PhO3I5Pt5iB_Mj7Bu0BeO/pub?gid=633798816&single=true&output=csv')
zoneable_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSEz-OcFSz13kGB2Z9iRzLmBkor8R2o7C-tzOSm91cQKt4foAG6iGynlT8PhO3I5Pt5iB_Mj7Bu0BeO/pub?gid=1768993571&single=true&output=csv')
zkaff_sheet = pd.read_csv('https://docs.google.com/spreadsheets/d/1ht9fhAflPF7g8uo8QnZKZuu8ZGjpOidSFOgSNREx2lY/pub?gid=839076986&single=true&output=csv')

# Make empty lists for specific and non-specific challenges
specific_challenges = []
zurich_challenges = []
unspecific_challenges = []

# Generate zone lists
zones = [116, 115, 161, 162, 113, 114, 124, 160, 163, 118, 117, 112, 123, 120, 164, 111, 121, 122, 170, 171, 154, 110, 173, 172, 135, 131, 155, 150, 156, 151, 152, 153, 181, 180, 133, 143, 142, 141, 140, 130, 132, 134]
s_bahn_zones = [132, 110, 151, 180, 120, 181, 155, 133, 156, 117, 121, 141, 142, 134, 112, 154]

class RawChallenge:
    def __init__(self,
                 title: str,
                 description: str,
                 points: int,
                 walking_minutes: int = 0,
                 stationary_minutes: int = 0,
                 kaffness: int = 0,
                 grade: int = 0,
                 zone: int | None | list[int] | str = None,
                 bias_sat: float = 1.0,
                 bias_sun: float = 1.0,
                 min_reps: int = 0,
                 max_reps: int = 0,
                 ppr: int = 0,
                 zoneable: bool = False,
                 no_disembark: bool = False,
                 fixed: bool = False,
                 dead_end: bool = False,
                 station_distance: int = 0,
                 departures: int | None = None,
                 time_to_hb: int = 0,
                 regionspecific: bool = False,
                 in_perim: bool = True):
        self.title = title
        self.description = description
        self.points = points
        self.walking_minutes = walking_minutes
        self.stationary_minutes = stationary_minutes
        self.kaffness = kaffness
        self.grade = grade
        self.zone = zone
        self.bias_sat = bias_sat
        self.bias_sun = bias_sun
        self.min_reps = min_reps
        self.max_reps = max_reps
        self.ppr = ppr
        self.zoneable = zoneable
        self.no_disembark = no_disembark
        self.fixed = fixed
        self.dead_end = dead_end
        self.station_distance = station_distance
        self.departures = departures
        self.time_to_hb = time_to_hb
        self.regionspecific = regionspecific
        self.in_perim = in_perim


    def __str__(self):
        return f'{self.title}\n{self.description}\np{self.points}k{self.kaffness}g{self.grade}z{self.zone}w{self.walking_minutes}s\
        {self.stationary_minutes}sd{self.station_distance}d{self.departures}t{self.time_to_hb}, zoneable = {self.zoneable}, fixed \
        = {self.fixed}, no_disembark = {self.no_disembark}, dead_end = {self.dead_end}'

    def challenge(self, zoned: bool, id: int, specific: bool, current_zone: int, delta: int) -> Challenge:
        self.description = str(self.description)
        zone = self.zone

        reps = random.randint(self.min_reps, self.max_reps)

        if self.zoneable and zoned:
            zone = random.choice(zones)

        if date.today().weekday() == 6:
            bias = self.bias_sun
        else:
            bias = self.bias_sat

        if not (self.zoneable and zoned) or zone == '%z' or zone == '%s':
            if '%z' in self.description:
                zone = random.choice(zones)
            if '%s' in self.description:
                zone = random.choice(s_bahn_zones)

        if type(zone) == list:
            best = None
            for z in zone:
                if best is None or distance_dict[current_zone][z] < distance_dict[current_zone][best]:
                    best = z 
            zone = best

        points = pointcalc(self.kaffness, self.grade, self.points, self.walking_minutes, self.stationary_minutes, self.ppr, reps, zone, bias, self.fixed, current_zone, delta, self.zoneable and zoned, self.dead_end, self.station_distance, self.time_to_hb, self.departures)

        description = self.description
        description = description.replace('%r', str(reps))
        description = description.replace('%z', str(zone))
        description = description.replace('%s', str(zone))
        if zoned and self.zoneable:
            description += f' Damit ihr Pünkt überchömed, mached das i de Zone {zone}.'
        # description = description + f' *{points} Pünkt*'

        if zone is None:
            zone = current_zone

        print(zone, perimeter_distances[zone], self.kaffness, self.title)

        return Challenge(self.title, description, points, id, specific, zone, kaff=self.kaffness, perimeter_distance=perimeter_distances[zone], no_disembark=self.no_disembark, regionspecific=self.regionspecific, in_perim=self.in_perim)

print('Generating challenges')

# get and add kaff challenges
for i in range(len(da_new_kaff_sheet)):
    row = da_new_kaff_sheet.loc[i]
    place = row['Ort']
    challenge = row['Challenge']
    kaffness = row['Kaffskala']
    grade = row['ÖV Güteklasse']
    zone = row['Zone']
    bias_sat = row['Bias Sat']
    bias_sun = row['Bias Sun']
    title_override = row['Title Override']
    challenge_points = row['Additional Points']
    min_reps = row['Min']
    max_reps = row['Max']
    ppr = row['Points per Repetition']
    walking_minutes = row['Walking Time']
    stationary_minutes = row['Stationary Time']
    no_disembark = row['No Disembark']


    # refine data
    if date.today().weekday() == 6:
        bias = bias_sun
    else:
        bias = bias_sat
    if type(title_override) == str:
        title = title_override
    else:
        title = f'Usflug uf {place}'
    if type(challenge) == str:
        raw_description = challenge
    else:
        raw_description = f'Gönd nach {place}.'
    kaffness = int(kaffness)
    grade = (int(grade) if not isnan(grade) else kaffness)  # Ignores empty cells, '-' and '?'
    zone = int(zone)
    bias = float(bias)
    challenge_points = int(challenge_points) if not isnan(challenge_points) else 0
    min_reps = int(min_reps) if not isnan(min_reps) else 0
    max_reps = int(max_reps) if not isnan(max_reps) else 0
    ppr = int(ppr) if not isnan(ppr) else 0
    stationary_minutes = int(stationary_minutes) if not isnan(stationary_minutes) else 0
    walking_minutes = int(walking_minutes) if not isnan(walking_minutes) else 0
    try:
        no_disembark = bool(no_disembark)
    except:
        no_disembark = False
        print("no No Disembark :(")

    # Return challenge
    if not title.lower == "nan" or raw_description.lower == "nan":
        specific_challenges.append(RawChallenge(title, raw_description, challenge_points, walking_minutes, stationary_minutes, kaffness, grade, zone, bias_sat, bias_sun, min_reps, max_reps, ppr, no_disembark=no_disembark))
    else:
        print("Error: Empty cells in spreadsheet")

for i in range(len(zkaff_sheet)):
    row = zkaff_sheet.loc[i]
    place = row['Ort']
    challenge = row['Challenge']
    title_override = row['Title Override']
    challenge_points = row['Additional Points']
    min_reps = row['Min']
    max_reps = row['Max']
    ppr = row['Points per Repetition']
    walking_minutes = row['Walking Time']
    stationary_minutes = row['Stationary Time']
    no_disembark = row['No Disembark']
    dead_end = row['SG']
    station_distance = row['Station Distance']
    time_to_hb = row['Time to HB']
    departures = row['Departures']

    # refine data
    if type(title_override) == str:
        title = title_override
    else:
        title = f'Tsüridrift nach {place}'
    if type(challenge) == str:
        raw_description = challenge
    else:
        raw_description = f'Gönd ad Station "{place}" in Züri.'
    challenge_points = int(challenge_points) if not isnan(challenge_points) else 0
    min_reps = int(min_reps) if not isnan(min_reps) else 0
    max_reps = int(max_reps) if not isnan(max_reps) else 0
    ppr = int(ppr) if not isnan(ppr) else 0
    stationary_minutes = int(stationary_minutes) if not isnan(stationary_minutes) else 0
    walking_minutes = int(walking_minutes) if not isnan(walking_minutes) else 0
    try:
        no_disembark = bool(no_disembark)
    except:
        no_disembark = False
        print("no No Disembark :(")
    try:
        dead_end = bool(dead_end)
    except:
        dead_end = False
        print("Dead end is dead (not big surprise) :(")
    station_distance = int(station_distance) if not isnan(station_distance) else 0
    time_to_hb = int(time_to_hb) if not isnan(time_to_hb) else 0
    departures = int(departures) if not isnan(departures) else 0

    # Return challenge
    if not title.lower == "nan" or raw_description.lower == "nan":
        zurich_challenges.append(RawChallenge(title, raw_description, challenge_points, walking_minutes, stationary_minutes, kaffness, grade, zone, bias_sat, bias_sun, min_reps, max_reps, ppr, no_disembark=no_disembark))
    else:
        print("Error: Empty cells in spreadsheet")

# get and add specific challenges
for i in range(len(ortsspezifisch_sheet)):
    row = ortsspezifisch_sheet.loc[i]
    title = row['title']
    description = row['description']
    challenge_points = row['points']
    min_reps = row["min"]
    max_reps = row['max']
    ppr = row['ppr']
    fixed = (row['fixed'] == 1) # TODO: does this throw an error?
    zone = row['Zone']
    walking_minutes = row['Walking Time']
    stationary_minutes = row['Stationary Time']
    kaffness = row['Kaffskala']
    grade = row['ÖV Güteklasse']
    no_disembark = row['No Disembark']

    # Refine data
    challenge_points = int(challenge_points) if not isnan(challenge_points) else 0
    min_reps = int(min_reps) if not isnan(min_reps) else 0
    max_reps = int(max_reps) if not isnan(max_reps) else 0
    ppr = int(ppr) if not isnan(ppr) else 0
    # try:
    #     zone = int(zone) if not isnan(zone) else None
    # except TypeError:
    #     zone = None
    try:
        zone = int(zone)
    except ValueError as err:
        try:
            zone = list(map(int, zone.split(',')))
        except (ValueError, AttributeError):
            try:
                zone = str(zone)
                if zone != '%z' and zone != '%s':
                    zone = None
            except ValueError:
                zone = None
    stationary_minutes = int(stationary_minutes) if not isnan(stationary_minutes) else 0
    walking_minutes = int(walking_minutes) if not isnan(walking_minutes) else 0
    kaffness = int(kaffness) if not isnan(kaffness) else 0
    grade = (int(grade) if not isnan(grade) else kaffness)  # Ignores empty cells, '-' and '?'
    try:
        no_disembark = bool(no_disembark)
    except:
        no_disembark = False
        print("no No Disembark :(")

    # Return challenge
    if not title.lower == "nan" or raw_description.lower == "nan":
        specific_challenges.append(RawChallenge(title, description, challenge_points, walking_minutes, stationary_minutes, zone=zone, kaffness = kaffness, grade = grade, min_reps = min_reps, max_reps = max_reps, ppr = ppr, fixed = fixed, no_disembark=no_disembark))
    else:
        print("Error: Empty cells in spreadsheet")


# get and add region specific challenges
for i in range(len(regionsspezifisch_sheet)):
    row = regionsspezifisch_sheet.loc[i]
    title = row['title']
    description = row['description']
    challenge_points = row['points']
    min_reps = row["min"]
    max_reps = row['max']
    ppr = row['ppr']
    fixed = (row['fixed'] == 1) # TODO: does this throw an error?
    no_disembark = row['No Disembark']
    perimeter = row['Perimeter']

    # Refine data
    challenge_points = int(challenge_points) if not isnan(challenge_points) else 0
    min_reps = int(min_reps) if not isnan(min_reps) else 0
    max_reps = int(max_reps) if not isnan(max_reps) else 0
    ppr = int(ppr) if not isnan(ppr) else 0
    try:
        no_disembark = bool(no_disembark)
    except:
        no_disembark = False
        print("no No Disembark :(")

    try:
        in_perim = bool(perimeter)
    except:
        in_perim = False
        print("no Perimeter :(")

    # Return challenge
    if not title.lower == "nan" or raw_description.lower == "nan":
        unspecific_challenges.append(RawChallenge(title, description, challenge_points, min_reps=min_reps, max_reps=max_reps, ppr=ppr, fixed=fixed, no_disembark=no_disembark, regionspecific=True, in_perim=in_perim))
    else:
        print("Error: Empty cells in spreadsheet")

# get and add zoneable challenges
for i in range(len(zoneable_sheet)):
    row = zoneable_sheet.loc[i]
    title = row['title']
    description = row['description']
    challenge_points = row['points']
    min_reps = row["min"]
    max_reps = row['max']
    ppr = row['ppr']
    fixed = (row['fixed'] == 1) # TODO: does this throw an error?
    no_disembark = row['No Disembark']

    # Refine data
    challenge_points = int(challenge_points) if not isnan(challenge_points) else 0
    min_reps = int(min_reps) if not isnan(min_reps) else 0
    max_reps = int(max_reps) if not isnan(max_reps) else 0
    ppr = int(ppr) if not isnan(ppr) else 0
    try:
        no_disembark = bool(no_disembark)
    except:
        no_disembark = False
        print("no No Disembark :(")

    # Return challenge
    if not title.lower == "nan" or raw_description.lower == "nan":
        raw_challenge_to_append = RawChallenge(title, description, challenge_points, min_reps=min_reps,
                                               max_reps=max_reps, ppr=ppr, fixed=fixed, zoneable=True,
                                               no_disembark=no_disembark)
        specific_challenges.append(raw_challenge_to_append)
        unspecific_challenges.append(raw_challenge_to_append)
    else:
        print("Error: Empty cells in spreadsheet")


# get and add unspecific challenges
for i in range(len(unspecific_sheet)):
    row = unspecific_sheet.loc[i]
    title = row['title']
    description = row['description']
    challenge_points = row['points']
    min_reps = row["min"]
    max_reps = row['max']
    ppr = row['ppr']
    fixed = (row['fixed'] == 1) # TODO: does this throw an error?
    no_disembark = row['No Disembark']

    # Refine data
    challenge_points = int(challenge_points) if not isnan(challenge_points) else 0
    min_reps = int(min_reps) if not isnan(min_reps) else 0
    max_reps = int(max_reps) if not isnan(max_reps) else 0
    ppr = int(ppr) if not isnan(ppr) else 0
    try:
        no_disembark = bool(no_disembark)
    except:
        no_disembark = False
        print("no No Disembark :(")

    # Return challenge
    if not title.lower == "nan" or raw_description.lower == "nan":
        unspecific_challenges.append(RawChallenge(title, description, challenge_points, min_reps=min_reps, max_reps=max_reps, ppr=ppr, fixed=fixed, no_disembark=no_disembark))
    else:
        print("Error: Empty cells in spreadsheet")

# For both lists generate their lengths = amount of different challenges
specific_challenges_amount = len(specific_challenges)
unspecific_challenges_amount = len(unspecific_challenges)


def specific_challenge_generate(index, current_zone, delta: int) -> Challenge:
    return specific_challenges[index].challenge(zoned=True, id=index, specific=True, current_zone=current_zone, delta=delta)


def zurich_challenge_generate(index, current_zone, delta: int) -> Challenge:
    return zurich_challenges[index].challenge(zoned=True, id=index, specific=True, current_zone=current_zone, delta=delta)


def unspecific_challenge_generate(index, current_zone, delta: int):
    return unspecific_challenges[index].challenge(zoned=False, id=index, specific=False, current_zone=current_zone, delta=delta)


if __name__ == '__main__':
    print(*unspecific_challenges, sep='\n')
    print('\n\n====\nspez\n====\n')
    print(*specific_challenges, sep='\n')
