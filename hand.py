from card import Card, Card2
from typing import Union, Optional, List, cast, overload, Tuple, Any
from deck import Deck2
import sys


class Hand:
    def __init__(self, dealer_card: Card2, *cards: Card2) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))

    def __repr__(self) -> str:
        cards_text = ', '.join(map(repr, self.cards))
        return f"{self.__class__.__name__}({self.dealer_card!r}, {cards_text}"

    def __format__(self, spec) -> str:
        if spec == "":
            return str(self)
        return ", ".join(f"{c:{spec}}" for c in self.cards)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() == cast(int, other)
        try:
            return (
                self.cards == cast(Hand, other).cards
                and self.dealer_card == cast(Hand, other).dealer_card
            )
        except AttributeError:
            return NotImplemented

    def total(self) -> int:
        delta_soft = max(c.soft - c.hard for c in self.cards)
        hard = sum(c.hard for c in self.cards)
        if hard + delta_soft <= 21:
            return hard + delta_soft
        return hard


class FrozenHand(Hand):
    # only immutable (hashable) object can be a dictionary key
    def __init__(self, *args, **kw) -> None:
        if len(args) == 1 and isinstance(args[0], Hand):
            # Clone a hand
            other = cast(Hand, args[0])
            self.dealer_card = other.dealer_card
            self.cards = other.cards
        else:
            # Build a fresh Hand from Card instances
            super().__init__(*args, **kw)

    def __hash__(self) -> int:
        return sum(hash(c) for c in self.cards) % sys.hash_info.modulus


class Hand2:
    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)

    def card_append(self, card: Card) -> None:
        self.cards.append(card)

    def hard_total(self) -> int:
        return sum(c.hard for c in self.cards)

    def soft_total(self) -> int:
        return sum(c.soft for c in self.cards)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.dealer_card!r}, *{self.cards})"


# Multi-strategy __init__()
class Hand3:
    @overload
    def __init__(self, arg1: "Hand3"):
        ...

    @overload
    def __init__(self, arg1: Card, arg2: Card, arg3: Card) -> None:
        ...

    def __init__(self, arg1: Union[Card, "Hand3"], arg2: Optional[Card] = None, arg3: Optional[Card] = None) -> None:
        self.dealer_card: Card
        self.cards: List[Card]
        if isinstance(arg1, Hand3) and not arg2 and not arg3:
            # Clone an existing hand
            self.dealer_card = arg1.dealer_card
            self.cards = arg1.cards
        elif isinstance(arg1, Card) and isinstance(arg2, Card) and isinstance(arg3, Card):
            # Build a fresh , new hand.
            self.dealer_card = cast(Card, arg1)
            self.cards = [arg2, arg3]
        else:
            raise ValueError("Wrong types of arguments")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ({self.dealer_card!r}, *{self.cards}"


# More complex initialization alternatives
class Hand4:
    @overload
    def __init__(self, arg1: "Hand4") -> None:
        ...

    @overload
    def __init__(self, arg1: "Hand4", arg2: Card, *, split: int) -> None:
        ...

    @overload
    def __init__(self, arg1: Card, arg2: Card, arg3: Card) -> None:
        ...

    def __init__(self,
                 arg1: Union["Hand4", Card],
                 arg2: Optional[Card] = None,
                 arg3: Optional[Card] = None,
                 split: Optional[int] = None) -> None:
        self.dealer_card: Card
        self.cards: List[Card]
        if isinstance(arg1, Hand4):
            # Clone  an existing hand
            self.dealer_card = arg1.dealer_card
            self.cards = arg1.cards
        elif isinstance(arg1, Hand4) and isinstance(arg2, Card) and split is not None:
            # Split an existing hand
            self.dealer_card = arg1.dealer_card
            self.cards = [arg1.cards[split], arg2]
        elif isinstance(arg1, Card) and isinstance(arg2, Card) and isinstance(arg3, Card):
            # Build a fresh, new hand from three cards
            self.dealer_card = arg1
            self.cards = [arg2, arg3]
        else:
            raise TypeError(f"Invalid constructor {arg1!r} {arg2!r} {arg3!r}")

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))


# Initializing with static or class-level methods
# When we have multiple ways to create an object, it's sometimes clearer to use static methods to
# create and return instances rather than complex __init__() methods
# Python has three kinds of binding for method functions: bind to instance, bind to class with @staticmethod,
# bind to class with @classmethod with class as the first positional parameter

class Hand5:
    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)

    @staticmethod
    def freeze(other) -> "Hand5":
        hand = Hand5(other.dealer_card, *other.cards)
        return hand

    @staticmethod
    def split(other, card0, card1) -> Tuple["Hand5", "Hand5",]:
        hand0 = Hand5(other.dealer_card, other.cards[0], card0)
        hand1 = Hand5(other.dealer_card, other.cards[1], card1)
        return hand0, hand1

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))


if __name__ == "__main__":
    from deck import Deck
    from collections import defaultdict
    import random

    # random.seed(42)

    # d = Deck()
    # h = Hand(d.pop())
    # h.cards.append(d.pop())
    # h.cards.append(d.pop())

    # d = Deck()
    # h = Hand2(d.pop(), d.pop(), d.pop())

    # h = Hand3(d.pop(), d.pop(), d.pop())
    # memento = Hand3(h)

    # h = Hand4(d.pop(), d.pop(), d.pop())
    # s1 = Hand4(h, d.pop(), split=0)
    # s2 = Hand4(h, d.pop(), split=1)
    # print(f"Start {h}, Split1 {s1}, Split2 {s2}")

    # h = Hand5(d.pop(), d.pop(), d.pop())
    # s1, s2 = Hand5.split(h, d.pop(), d.pop())
    # print(f"Start {h}, Split1 {s1}, Split2 {s2}")

    # h = Hand(d.pop(), d.pop(), d.pop(), d.pop())
    # print("Player: {hand:%r%s}".format(hand=h))
    stats = defaultdict(int)

    d = Deck2()
    h = Hand(d.pop(), d.pop(), d.pop())
    h_f = FrozenHand(h)
    stats[h_f] += 1

