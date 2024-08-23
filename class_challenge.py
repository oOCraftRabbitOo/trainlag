class Challenge:
    def __init__(self, title: str, description: str, points: int, id: int, specific: bool, zone: int, kaff: int, perimeter_distance: int, no_disembark: bool, regionspecific: bool = False, in_perim: bool = True, zkaff: bool = False):
        self.title: str = title
        self.description: str = description
        self.points: int = points
        self.id: int = id
        self.specific: bool = specific
        self.zone: int = zone
        self.kaff: int = kaff
        self.perimeter_distance: int = perimeter_distance
        self.no_disembark: bool = no_disembark
        self.regionspecific = regionspecific
        self.in_perim = in_perim
        self.zkaff = zkaff

    def __str__(self):
        return f"**{self.title}** \n{self.description}"

    def __eq__(self, other):
        return self.specific == other.specific and self.id == other.id and self.zkaff == other.zkaff
