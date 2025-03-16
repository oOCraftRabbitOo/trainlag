import random
import pandas as pd
from datetime import date
from pointcalc import pointcalc, distance_dict, perimeter_distances
from class_challenge import Challenge
from numpy import isnan

print('Loading challenges. This may take a while')

# Load the CSV file from Google Sheets
uc4 = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRcImsj8yCZNaKSx4wYk6GZnBkZ_Eody246mqM4UjsvYIW3wqd37kIhhIlrWJ3tiwSLbN9RWzMVs-V1/pub?gid=1012921349&single=true&output=csv')

# Make empty lists for specific and non-specific challenges
specific_challenges = []
zurich_challenges = []
unspecific_challenges = []

# Generate zone lists
zones = [110, 111, 112, 113, 114, 115, 116, 117, 118, 120, 121, 122, 123, 124, 130, 131, 132, 133, 134, 135, 140, 141, 142, 143, 150, 151, 152, 153, 154, 155, 156, 160, 161, 162, 163, 164, 170, 171, 172, 173, 180, 181]
s_bahn_zones = [110, 112, 117, 120, 121, 132, 133, 134, 141, 142, 151, 154, 155, 156, 180, 181]


class RawChallenge:
    def __init__(self,
                 challenge_type: str,
                 title: str | None,
                 description: str | None,
                 place: str | None,
                 kaffskala: int | None,
                 grade: int | None,
                 zone: int | None | list[int] | str = None,
                 weight: int = 1,
                 bias_sat: float = 1,
                 bias_sun: float = 1,
                 walking_time: int = 0,
                 stationary_time: int = 0,
                 additional_points: int = 0,
                 min_reps: int | None = None,
                 max_reps: int | None = None,
                 points_per_rep: int | None = None,
                 station_distance: int | None = None,
                 time_to_hb: int | None = None,
                 departures: int | None = None,
                 dead_end: bool | None = None,
                 no_disembark: bool = False,
                 fixed_points: bool = False,
                 in_perim: bool | None = None
                 ):
        self.challenge_type = challenge_type
        self.title = title
        self.description = description
        self.place = place
        self.kaffskala = kaffskala
        self.grade = grade
        self.zone = zone
        self.weight = weight
        self.bias_sat = bias_sat
        self.bias_sun = bias_sun
        self.walking_time = walking_time
        self.stationary_time = stationary_time
        self.additional_points = additional_points
        self.min_reps = min_reps
        self.max_reps = max_reps
        self.points_per_rep = points_per_rep
        self.station_distance = station_distance
        self.time_to_hb = time_to_hb
        self.departures = departures
        self.dead_end = dead_end
        self.no_disembark = no_disembark
        self.fixed_points = fixed_points
        self.in_perim = in_perim
        self.bias = 1  # will be changed in refine


    def __str__(self):
        return (f'ct "{self.challenge_type}" \n'
                f't "{self.title}" \n'
                f'd "{self.description}" \n'
                f'p "{self.place}" '
                f'ks "{self.kaffskala}" '
                f'g "{self.grade}" '
                f'z "{self.zone}" '
                f'w "{self.weight}" '
                f'sat "{self.bias_sat}" '
                f'sun "{self.bias_sun}" '
                f'wt "{self.walking_time}" '
                f'st "{self.stationary_time}" '
                f'ap "{self.additional_points}" '
                f'min "{self.min_reps}" '
                f'max "{self.max_reps}" '
                f'ppr "{self.points_per_rep}" '
                f'sd "{self.station_distance}" '
                f'hb "{self.time_to_hb}" '
                f'dep "{self.departures}" '
                f'de "{self.dead_end}" '
                f'nd "{self.no_disembark}" '
                f'f "{self.fixed_points}" '
                f'p "{self.in_perim}"')


    def valid(self) -> bool:
        # Type checks
        type_checks = [
            (isinstance(self.challenge_type, str), "challenge_type must be a string"),
            (isinstance(self.title, (str, type(None))), "title must be a string or None"),
            (isinstance(self.description, (str, type(None))), "description must be a string or None"),
            (isinstance(self.place, (str, type(None))), "place must be a string or None"),
            (isinstance(self.kaffskala, (int, type(None))), "kaffskala must be an int or None"),
            (isinstance(self.grade, (int, type(None))), "grade must be an int or None"),
            (isinstance(self.zone, (int, list, str, type(None))), "zone must be int, list, str, or None"),
            (isinstance(self.weight, int), "weight must be an int"),
            (isinstance(self.bias_sat, float), "bias_sat must be a float"),
            (isinstance(self.bias_sun, float), "bias_sun must be a float"),
            (isinstance(self.walking_time, int), "walking_time must be an int"),
            (isinstance(self.stationary_time, int), "stationary_time must be an int"),
            (isinstance(self.additional_points, int), "additional_points must be an int"),
            (isinstance(self.min_reps, (int, type(None))), "min_reps must be an int or None"),
            (isinstance(self.max_reps, (int, type(None))), "max_reps must be an int or None"),
            (isinstance(self.points_per_rep, (int, type(None))), "points_per_rep must be an int or None"),
            (isinstance(self.station_distance, (int, type(None))), "station_distance must be an int or None"),
            (isinstance(self.time_to_hb, (int, type(None))), "time_to_hb must be an int or None"),
            (isinstance(self.departures, (int, type(None))), "departures must be an int or None"),
            (isinstance(self.dead_end, (bool, type(None))), "dead_end must be a bool or None"),
            (isinstance(self.no_disembark, bool), "no_disembark must be a bool"),
            (isinstance(self.fixed_points, bool), "fixed_points must be a bool"),
            (isinstance(self.in_perim, (bool, type(None))), "in_perim must be a bool or None")
        ]
        for check, msg in type_checks:
            if not check:
                print(msg)
                return False

        # Challenge type validation
        valid_types = {"kaff", "z_kaff", "ortsspezifisch", "regionsspezifisch", "unspezifisch", "zoneable"}
        if self.challenge_type not in valid_types:
            print(f"Invalid challenge_type: {self.challenge_type}")
            return False

        # Title/description checks
        if self.challenge_type not in {"kaff", "z_kaff"}:
            if not self.title or not self.description:
                print("title and description are required for non-kaff type challenges")
                return False
        else:
            if not self.place:
                print("place is required for kaff or z_kaff challenges")
                return False

        # Orts-/Kaff-specific attributes
        if self.challenge_type in {"kaff", "ortsspezifisch"}:
            if self.kaffskala is None or self.grade is None or self.zone is None:
                print("kaffskala, grade, and zone are required for kaff or ortsspezifisch challenges")
                return False
        else:
            if any(attr is not None for attr in [self.kaffskala, self.grade, self.zone]):
                print("kaffskala, grade, and zone must be None for non-kaff challenges")
                return False

        # z_kaff attributes
        if self.challenge_type == "z_kaff":
            if any(attr is None for attr in [self.station_distance, self.time_to_hb, self.departures, self.dead_end]):
                print("station_distance, time_to_hb, departures, and dead_end are required for z_kaff challenges")
                return False
        else:
            if any(attr is not None for attr in [self.station_distance, self.time_to_hb, self.departures]) or self.dead_end:
                print("station_distance, time_to_hb, departures, and dead_end must be None for non-z_kaff challenges")
                return False

        # in_perim check
        if self.challenge_type not in {"kaff", "z_kaff"} and self.in_perim is None:
            print("in_perim is required for non-kaff and non-z_kaff challenges")
            return False

        return True


    def challenge(self, zoned: bool, id: int, specific: bool, current_zone: int, delta: int, zkaff: bool = False) -> Challenge | None: # TODO: handle None when its important
        if not self.valid():
            return None

        if (self.challenge_type == "zoneable" and zoned) or '%z' in self.description:
            out_zone = random.choice(zones)
        elif '%s' in self.description:
            out_zone = random.choice(s_bahn_zones)
        elif type(self.zone) == list:
            best = None
            for z in self.zone:
                if best is None or distance_dict[current_zone][z] < distance_dict[current_zone][best]:
                    best = z
            out_zone = best

            if type(out_zone) != int:
                print(f"Unexpected error with zone within list. Got {out_zone} of type {type(out_zone)} instead of int.")
                return None

        elif type(self.zone) == int:
            out_zone = self.zone
        else:
            print(f"Unexpected error with zone {self.zone}. Got {type(self.zone)} instead of int, list, %s, or %z.")
            return None

        out_reps = random.randint(self.min_reps, self.max_reps)

        out_points = pointcalc(self.kaffskala, self.grade, self.additional_points,
                           self.walking_time, self.stationary_time, self.points_per_rep,
                           out_reps, out_zone, self.bias, self.fixed_points, current_zone, delta,
                           (self.challenge_type == "zoneable" and zoned), self.dead_end,
                           self.station_distance, self.time_to_hb, self.departures)

        description = self.description
        description = description.replace('%r', str(out_reps))
        description = description.replace('%z', str(out_zone))
        description = description.replace('%s', str(out_zone))

        if zoned and self.challenge_type == "zoneable":
            description += f' Damit ihr Pünkt überchömed, mached das i de Zone {out_zone}.'

        if out_zone is None:
            out_zone = current_zone

        print(out_zone, perimeter_distances[out_zone], self.kaffskala, self.title)

        return Challenge(self.title, description, out_points, id, specific, out_zone, kaff=self.kaffskala,
                         perimeter_distance=perimeter_distances[zone], no_disembark=self.no_disembark,
                         regionspecific=(self.challenge_type == "regionsspezifisch"), in_perim=self.in_perim,
                         zkaff=zkaff, zoneable=(self.challenge_type == "zoneable"))

    def refine(self):
        if self.challenge_type == "z_kaff":
            if self.title is None:
                self.title = f'Tsüridrift nach {self.place}'
            if self.description is None:
                self.description = f'Gönd ad Station "{self.place}" in Züri.'

        if self.challenge_type == "kaff":
            if self.title is None:
                self.title = f'Usflug uf {self.place}'
            if self.description is None:
                self.description = f'Gönd nach {place}.'

        if date.today().weekday() == 6:
            self.bias = self.bias_sun
        elif date.today().weekday() == 5:
            self.bias = self.bias_sat
        else:
            self.bias = 1


print('Generating challenges')

for i in range(len(uc4)):
    row = uc4.loc[i]
    challenge_type = row['challenge_type']  # str
    status = row['status'] # str
    title = row['title']  # str | None
    description = row['description']  # str | None
    place = row['place']  # str | None
    kaffskala = row['kaffskala']  # int | None
    grade = row['grade']  # int | None
    zone = row['zone']  # int | list[int] | str | None
    weight = row['weight']  # int
    bias_sat = row['bias_sat']  # float
    bias_sun = row['bias_sun']  # float
    walking_time = row['walking_time']  # int
    stationary_time = row['stationary_time']  # int
    additional_points = row['additional_points']  # int
    min_reps = row['min_reps']  # int | None
    max_reps = row['max_reps']  # int | None
    points_per_rep= row['points_per_rep']  # int | None
    station_distance = row['station_distance']  # int | None
    time_to_hb = row['time_to_hb']  # int | None
    departures = row['departures']  # int | None
    dead_end = row['dead_end']  # bool | None
    no_disembark = row['no_disembark']  # bool
    fixed_points = row['fixed_points']  # bool
    in_perim = row['in_perim']  # bool | None

    status = str(status)
    challenge_type = str(challenge_type)
    title = None if pd.isna(title) else str(title)
    description = None if pd.isna(description) else str(description)
    place = None if pd.isna(place) else str(place)
    kaffskala = int(k) if pd.notna(k := pd.to_numeric(kaffskala, errors='coerce')) else None
    grade = int(g) if pd.notna(g := pd.to_numeric(grade, errors='coerce')) else None

    if status not in {'approved', 'refactor'}:
        continue

    if pd.isna(zone):
        zone = None
    elif isinstance(zone, str) and "," in zone:
        zone = [int(z) for z in zone.split(',')]
    elif not (isinstance(zone, str) and zone.startswith("%")):
        try:
            zone = int(zone)
        except:
            print(f"Unexpected error with zone: {zone}")
            zone = None

    weight = int(w) if pd.notna(w := pd.to_numeric(walking_time, errors='coerce')) else 1
    bias_sat = float(b) if pd.notna(b := pd.to_numeric(bias_sat, errors='coerce')) else 1.0
    bias_sun = float(b) if pd.notna(b := pd.to_numeric(bias_sun, errors='coerce')) else 1.0
    walking_time = int(w) if pd.notna(w := pd.to_numeric(walking_time, errors='coerce')) else 0
    stationary_time = int(s) if pd.notna(s := pd.to_numeric(stationary_time, errors='coerce')) else 0
    additional_points = int(a) if pd.notna(a := pd.to_numeric(additional_points, errors='coerce')) else 0
    min_reps = int(m) if pd.notna(m := pd.to_numeric(min_reps, errors='coerce')) else None
    max_reps = int(m) if pd.notna(m := pd.to_numeric(max_reps, errors='coerce')) else None
    points_per_rep = int(p) if pd.notna(p := pd.to_numeric(points_per_rep, errors='coerce')) else None
    station_distance = int(s) if pd.notna(s := pd.to_numeric(station_distance, errors='coerce')) else None
    time_to_hb = int(t) if pd.notna(t := pd.to_numeric(time_to_hb, errors='coerce')) else None
    departures = int(d) if pd.notna(d := pd.to_numeric(departures, errors='coerce')) else None
    dead_end = False if pd.isna(dead_end) else bool(dead_end)
    no_disembark = False if pd.isna(no_disembark) else bool(no_disembark)
    fixed_points = False if pd.isna(fixed_points) else bool(fixed_points)
    in_perim = None if pd.isna(in_perim) else bool(in_perim)

    challenge = RawChallenge(challenge_type, title, description, place, kaffskala, grade, zone, weight, bias_sat, bias_sun,
                 walking_time, stationary_time, additional_points, min_reps, max_reps, points_per_rep,
                 station_distance, time_to_hb, departures, dead_end, no_disembark, fixed_points, in_perim)
    challenge.refine()

    if not challenge.valid():
        print(f"Invalid challenge found at index {i}. Ignoreth :)")
        continue

    if challenge_type == "kaff" or challenge_type == "ortsspezifisch":
        specific_challenges.append(challenge)
    elif challenge_type == "zkaff":
        zurich_challenges.append(challenge)
    elif challenge_type == "regionsspezifisch": # TODO: doesn't a separate regio list make sense?
        unspecific_challenges.append(challenge)
    elif challenge_type == "unspezifisch":
        unspecific_challenges.append(challenge)
    elif challenge_type == "zoneable":
        specific_challenges.append(challenge)
        unspecific_challenges.append(challenge)
    else:
        print(f"Challenge Type Error: challenge type {challenge_type} is invalid.") # shouldn't be reachable even

# For both lists generate their lengths = amount of different challenges
specific_challenges_amount = len(specific_challenges)
unspecific_challenges_amount = len(unspecific_challenges)
zurich_challenges_amount = len(zurich_challenges)


def specific_challenge_generate(index, current_zone, delta: int) -> Challenge:
    return specific_challenges[index].challenge(zoned=True, id=index, specific=True, current_zone=current_zone, delta=delta)


def zurich_challenge_generate(index, current_zone, delta: int) -> Challenge:
    return zurich_challenges[index].challenge(zoned=True, id=index, specific=True, current_zone=current_zone, delta=delta, zkaff=True)


def unspecific_challenge_generate(index, current_zone, delta: int):
    return unspecific_challenges[index].challenge(zoned=False, id=index, specific=False, current_zone=current_zone, delta=delta)


if __name__ == '__main__':
    print(*unspecific_challenges, sep='\n')
    print('\n\n====\nspez\n====\n')
    print(*specific_challenges, sep='\n')
