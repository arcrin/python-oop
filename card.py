from typing import Tuple, List, Any, cast
from enum import Enum
import sys


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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__!s}(suit={self.suit!r}, rank={self.rank!r}"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __format__(self, format_spec: str) -> str:
        if format_spec == "":
            return str(self)
        return_string = (
            format_spec.replace("%r", self.rank).replace("%s", self.suit).replace("%%", "%")
        )
        return return_string


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


class Card2:
    insure = False

    def __init__(self, rank: str, suit: "Suit", hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(suit={self.suit!r}, rank={self.rank!r}"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __eq__(self, other: Any) -> bool:
        return (
            self.suit == cast(Card2, other).suit
            and self.rank == cast(Card2, other).rank
        )

    def __hash__(self) -> int:
        return (hash(self.suit) + 4 * hash(self.rank)) % sys.hash_info.modulus

    def __format__(self, format_spec: str) -> str:
        if format_spec == "":
            return str(self)
        rs = (
            format_spec.replace("%r", self.rank).replace("%s", self.suit).replace("%%", "%")
        )
        return rs


class NumberCard2(Card2):
    def __init__(self, rank: int, suit: "Suit") -> None:
        super().__init__(str(rank), suit, rank, rank)


class AceCard2(Card2):
    insure = True

    def __init__(self, rank: int, suit: "Suit") -> None:
        super().__init__("A", suit, 1, 11)


class FaceCard2(Card2):
    def __init__(self, rank: int, suit: "Suit") -> None:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank_str, suit, 10, 10)


def card2(rank: int, suit: Suit) -> Card2:
    class_ = {1: AceCard2, 11: FaceCard2, 12: FaceCard2, 13: FaceCard2}.get(
        rank, NumberCard2
    )
    return class_(rank, suit)


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


# This is not desirable. It involves a repetition of the sequence of the mapping keys 1, 11, 12, 13. Repetition is bad,
# because parallel structures never seem to stay that way after the software has been updated or revised.
def card5(rank: int, suit: Suit) -> Card:
    class_ = {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard}.get(rank, Card)
    rank_str = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(rank, str(rank))
    return class_(rank_str, suit)


def card6(rank: int, suit: Suit) -> Card:
    class_, rank_str = {
        1: (AceCard, "A"),
        11: (FaceCard, "J"),
        12: (FaceCard, "Q"),
        13: (FaceCard, "K")
    }.get(rank, (Card, str(rank),))
    return class_(rank_str, suit)


# In general, partial functions aren't helpful for most object-oriented programming. When building complex objects,
# it is common to define methods that accept arguments incrementally. Instead of using rank to create a partial
# function, a more bo object-oriented approach is to use separate methods to set rank and suit
def card7(rank: int, suit: Suit) -> Card:
    class_rank = {
        1: lambda suit: AceCard("A", suit),
        11: lambda suit: FaceCard("J", suit),
        12: lambda suit: FaceCard("Q", suit),
        13: lambda suit: FaceCard("K", suit),
    }.get(rank, lambda suit: Card(str(rank), suit))
    return class_rank(suit)


class CardFactory:
    def rank(self, rank: int) -> "CardFactory":
        self.class_, self.rank_str = {
            1: (AceCard, "A"),
            11: (FaceCard, "J"),
            12: (FaceCard, "Q"),
            13: (FaceCard, "K"),
        }.get(rank, (Card, str(rank)))
        return self

    def suit(self, suit: Suit) -> Card:
        return self.class_(self.rank_str, suit)


class Card3:
    # due to the lack of __hash__ function, this class is mutable
    def __init__(self, rank: str, suit: Suit, hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(suit={self.suit!r}, rank={self.rank!r}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(suit={self.suit!r}, rank={self.rank!r}"

    def __eq__(self, other: Any) -> bool:
        return (
            self.suit == cast(Card3, other).suit
            and self.rank == cast(Card3, other).rank
        )


class NumberCard3(Card3):
    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(str(rank), suit, rank, rank)


class AceCard3(Card3):
    def __init__(self, rank: int, suit: "Suit") -> None:
        super().__init__("A", suit, 1, 11)


class FaceCard3(Card3):
    def __init__(self, rank: int, suit: Suit) -> None:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank_str, suit, 10, 10)


def card10(rank: int, suit: Suit) -> Card3:
    if rank == 1:
        return AceCard3(rank, suit)
    elif 2 <= rank < 11:
        return NumberCard3(rank, suit)
    elif 11 <= rank < 14:
        return FaceCard3(rank, suit)
    else:
        raise Exception("Rank out of range")


def display_cards(list_of_cards: List[Card]):
    for entry in list_of_cards:
        print(f"{entry.rank} of {entry.suit}")


if __name__ == '__main__':
    # deck = [card(rank, suit)
    #         for rank in range(1, 14) for suit in iter(Suit)]  # iter suppresses error message from mypy
    # deck2 = [card2(rank, suit) for rank in range(13) for suit in iter(Suit)]  # fails when rank is 0, throws KeyError
    # deck4 = [card4(rank, suit) for rank in range(1, 14) for suit in iter(Suit)]
    # card8 = CardFactory()
    # deck8 = [card8.rank(r + 1).suit(s) for r in range(13) for s in iter(Suit)]
    # for card in deck8:
    #     print(f"{card.rank} of {card.suit}")

    # c = Card('2', Suit.Spade)
    # print("Dealer has {0:%r of %s}".format(c))

    print('test')

