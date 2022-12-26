class Challenge:
    def __init__(self, title, description, points, id):
        self.title = title
        self.description = description
        self.points = points
        self.id = id

    def __str__(self):
        return f"\033[1m{self.title}\033[0m \n  {self.description}"
