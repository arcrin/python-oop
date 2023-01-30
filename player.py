from table import Table
from strategy import BettingStrategy, GameStrategy
from typing import Optional


class Player:
    # This does little more than bookkeeping. We are simply transferring named parameters to instance variables with
    # same name. In many cases @dataclass decorator can simplify this.
    def __init__(self,
                 table: Table,
                 bet_strategy: BettingStrategy,
                 game_strategy: GameStrategy) -> None:
        self.hand = None
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table = table

    def game(self):
        self.table.place_bet(self.bet_strategy.bet())
        self.hand = self.table.get_hand()
        if self.table.can_insure(self.hand):
            if self.game_strategy.insurance(self.hand):
                self.table.insure(self.bet_strategy.bet())


class Player2:
    # using the ** construct to collect all keywords into a single variable makes the class easily extendable
    def __init__(self, **kw) -> None:
        """
        Must provide table, bet-strategy, game_strategy
        :param kw:
        """
        self.hand = None
        self.bet_strategy: BettingStrategy = kw['bet_strategy']
        self.game_strategy: GameStrategy = kw['game_strategy']
        self.table: Table = kw['table']

    def game(self) -> None:
        self.table.place_bet(self.bet_strategy.bet())
        self.hand = self.table.get_hand()


class Player2x:
    # disadvantage of this technique is the obscure parameter name, which aren't formally documented
    def __init__(self, **kw) -> None:
        """
        Must provide table, bet-strategy, game_strategy
        :param kw:
        """
        self.hand = None
        self.bet_strategy: BettingStrategy = kw['bet_strategy']
        self.game_strategy: GameStrategy = kw['game_strategy']
        self.table: Table = kw['table']
        self.log_name: Optional[str] = kw.get('log_name')


class Player3:
    # hybridize with a mixed positional and keyword implementation
    def __init__(self,
                 table: Table,
                 bet_strategy: BettingStrategy,
                 game_strategy: GameStrategy,
                 **extras) -> None:
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table = table
        # The known parameter values are popped from the "extras" dictionary. After this is finished, any other
        # parameter names represent a type error.
        self.log_name: str = extras.pop('log_name', self.__class__.__name__)
        if extras:
            raise TypeError(f'Extra arguments: {extras!r}')


# Initialization with type validation
# Runtime type validation is rarely a sensible requirement. In a way, this might be a failure to fully understand
# Python. Python's type system permits numerous extensions. Runtime type checking tends to defeat this. Using "mypy"
# provides extensive type checking without the runtime overheads0
class ValidPlayer:
    def __init__(self, table, bet_strategy, game_strategy):
        assert isinstance(table, Table)
        assert isinstance(bet_strategy, BettingStrategy)
        assert isinstance(game_strategy, GameStrategy)

        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table = table

