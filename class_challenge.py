class Challenge:
    def __init__(self, title, description, points, id, type):
        self.title = title
        self.description = description
        self.points = points
        self.id = id
        self.type = type

    def __str__(self):
        return f"**{self.title}** \n{self.description}"

    def __eq__(self, other):
        return self.type == other.type and self.id == other.id
