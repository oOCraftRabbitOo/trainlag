import copy

class Shop:
    def __init__(self, name, prize, discount):
        self.name = name
        self.prize = prize
        if discount > 500:
            self.first_prize = 0
        elif discount < 100:
            self.first_prize = None
        else:
            self.first_prize = 500 - discount

    def __str__(self) -> str:
        if self.first_prize is not None:
            if self.first_prize == 0:
                appendix = ', *ersti Trophäe **GRATIS!***'
            else:
                appendix = f', *ersti Trophäe **nur {self.first_prize}p!***'
        else:
            appendix = ''
        return f'Shop **{self.name}**: *{self.prize}p* pro Trophäe{appendix}'

    def disdiscounted(self):
        returnal = copy.deepcopy(self)
        returnal.first_prize = None
        return returnal

    def buy(self, points) -> tuple[int, int] | None:
        """
        Calculates how many trophies can be bought in the shop for an amount of points.
        
        ## Parameters
        points: The amount of points that will be spent.

        ## Returns
        The amount of trophies and the leftover points as a tuple (trophies, points) or None if no trophies can be bought.
        """
        if self.first_prize is not None:
            first_prize = self.first_prize
        else:
            first_prize = self.prize

        if points < first_prize:
            return None

        self.first_prize = None
        
        return ((points - first_prize) // self.prize + 1, (points - first_prize) % self.prize)

if __name__ == '__main__':
    shoppi_tivoli = Shop("tivioli", 400, 250)
    hand = Shop("hand", 69, 0)
    franz = Shop("kalus", 400, 600)
    print(shoppi_tivoli, hand, franz, sep='\n')
    print(shoppi_tivoli.buy(1000))
    print(shoppi_tivoli.buy(1000))
    print(hand.buy(1000))
    print(franz.buy(1000))
