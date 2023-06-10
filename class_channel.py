class Channel:
    def __init__(self, name: str, id: int):
        # note that the name of a channel doesn't have to correspond to it's name on the server
        self.name = name
        self.id = id