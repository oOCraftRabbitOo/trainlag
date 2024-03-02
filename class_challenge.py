class Challenge:
    def __init__(self, title: str, description: str, points: int, id: int, specific: bool, zone: int):
        self.title = title
        self.description = description
        self.points = points
        self.id = id
        self.specific = specific
        self.zone = zone

    def __str__(self):
        return f"**{self.title}** \n{self.description}"

    def __eq__(self, other):
        return self.specific == other.specific and self.id == other.id
