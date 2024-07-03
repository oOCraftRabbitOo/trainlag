class Challenge:
    def __init__(self, title: str, description: str, points: int, id: int, specific: bool, zone: int, kaff: int, in_perim: bool, no_disembark: bool):
        self.title: str = title
        self.description: str = description
        self.points: int = points
        self.id: int = id
        self.specific: bool = specific
        self.zone: int = zone
        self.kaff: int = kaff
        self.in_perim: bool = in_perim
        self.no_disembark: bool = no_disembark

    def __str__(self):
        return f"**{self.title}** \n{self.description}"

    def __eq__(self, other):
        return self.specific == other.specific and self.id == other.id
