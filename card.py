from typing import Tuple
from enum import Enum


class Suit(str, Enum):  # as a subclass of Enum, it makes Suit class immutable and iterable
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


class Card:
    def __init__(self, rank: str, suit: str) -> None:
        self.suit = suit
        self.rank = rank
        self.hard, self.soft = self._points()

    def _points(self) -> Tuple[int, int]:
        return int(self.rank), int(self.rank)


class AceCard(Card):
    def _points(self) -> Tuple[int, int]:
        return 1, 11


class FaceCard(Card):
    def _points(self) -> Tuple[int, int]:
        return 10, 10


def card(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    elif 11 <= rank < 14:
        name = {11: "J", 12: "Q", 13: "K"}[rank]
        return FaceCard(name, suit)
    raise Exception("Design Failure")


def card2(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    else:  # It is important to avoid a vague else clause. This will catch rank == 0, but only provides KeyError
        name = {11: "J", 12: "Q", 13: "K"}[rank]
        return FaceCard(name, suit)


def card3(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    # Replaced a mapping (the previous implementation of card) with elif sequence.
    # We can always replace a mapping with elif, but the reverse is not necessarily true
    # This has the advantage of being more consistent than the previous version
    elif rank == 11:
        return FaceCard("J", suit)
    elif rank == 12:
        return FaceCard("Q", suit)
    elif rank == 13:
        return FaceCard("K", suit)
    else:
        raise Exception("Rank out of range")


# In some cases, we can use mapping instead a chain of elif conditions. It is possible to find conditions that are so
# complex that a chain of elif conditions is the only sensible way to express them. For simple cases, however, a mapping
# often works better and can be easier to read.
def card4(rank: int, suit: Suit) -> Card:
    # This implementation has a serious deficiency. It lacks the translation from 1 to A, 11 to J, 12 to Q and 13 to K
    # Some sort of double mapping is required
    class_ = {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard}.get(rank, Card)
    return class_(str(rank), suit)


if __name__ == '__main__':
    deck = [card(rank, suit)
            for rank in range(1, 14) for suit in iter(Suit)]  # iter suppresses error message from mypy
    deck2 = [card2(rank, suit) for rank in range(13) for suit in iter(Suit)]  # fails when rank is 0, throws KeyError
    deck4 = [card4(rank, suit) for rank in range(1, 14) for suit in iter(Suit)]
    for card in deck4:
        print(f"{card.rank} of {card.suit}")
