from deck import Deck
from hand import Hand2


class Table:
    def __init__(self) -> None:
        self.hole_card = None
        self.hand = None
        self.deck = Deck()

    def place_bet(self, amount: int) -> None:
        print("Bet", amount)

    def get_hand(self) -> Hand2:
        try:
            self.hand = Hand2(self.deck.pop(), self.deck.pop(), self.deck.pop())
            self.hole_card = self.deck.pop()
        except IndexError:
            # Out of cards: need to shuffle and try again
            self.deck = Deck()
            return self.get_hand()
        print('Deal', self.hand)
        return self.hand
