import random

from card import card, card2, Card, Suit, display_cards


# Wrap: This design pattern surrounds an existing collection definition with a simplified interface. This is an example
# of the more general Facade design pattern
class Deck:
    def __init__(self) -> None:
        self._cards = [card(r + 1, s) for r in range(13) for s in iter(Suit)]
        random.shuffle(self._cards)

    # The pop() method of the Deck class delegates to the wrapped list object.
    def pop(self) -> Card:
        return self._cards.pop()


# Extend: This design pattern starts with an existing collection class and extends it to add features
# The pop() method is directly inherited from list and works perfectly. While simpler, this exposes methods
# such as delete() and remove(). If these additional features are undesirable, a wrapped object might be a better idea.
class Deck2(list):
    def __init__(self) -> None:
        super().__init__(card2(r + 1, s) for r in range(13) for s in iter(Suit))
        random.shuffle(self)


class Deck3(list):
    def __init__(self, decks: int = 1) -> None:
        super().__init__(
            card(r + 1, s)
            for r in range(13)
            for s in iter(Suit)
            for d in range(decks)
        )

        random.shuffle(self)
        burn = random.randint(1, 52)
        for i in range(burn):
            self.pop()


if __name__ == "__main__":
    d = Deck()
    hand = [d.pop(), d.pop()]
    display_cards(hand)
