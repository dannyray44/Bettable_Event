# -*- coding: utf-8 -*-
import typing

from event_dataclass.metadata import BetTypeID
from processable import Processable


class BetValue(Processable):
    _required_attributes = ['value', 'odds', 'lay', 'volume', 'previous_wager']

    def __init__(self, value: str, odds: float, lay: bool, volume: float = -1.0, previous_wager: float = 0.0) -> None:
        self.value: str = value
        self.odds: float = odds
        self.lay: bool = lay
        self.volume: float = volume
        self.previous_wager: float = previous_wager
        self.wager: float = 0.0
        super().__init__()


class Bet(Processable):
    _required_attributes = ['id', 'values']

    def __init__(self, id: typing.Union[int, BetTypeID], values: typing.Union[typing.List[BetValue], typing.List[dict]] = None) -> None:
        if isinstance(id, int):
            id = BetTypeID(id)
        self.id = id

        if values is None:
            values = []
        else:
            values = [BetValue._from_dict(value) if isinstance(value, dict) else value for value in values]
        self.values = values
        super().__init__()


class Bookmaker(Processable):
    _required_attributes = ['commission', 'wager_limit', 'wager_count', 'bets']

    def __init__(self, commission: float = 0.0, wager_limit: float = -1.0, bets: typing.Union[typing.List[Bet], typing.List[dict]] = None, wager_count: int = 0) -> None:
        self.commission = commission
        self.wager_limit = wager_limit
        self.wager_count = wager_count
        # self.wager_count_limit = -1
        if bets is None:
            bets = []
        else:
            bets = [Bet._from_dict(bet) if isinstance(bet, dict) else bet for bet in bets]
        self.bets = bets

        super().__init__()


class Event(Processable):
    _required_attributes = ['bookmakers', 'total_bet_size', 'profit', 'wager_count']

    def __init__(self, bookmakers: typing.Union[typing.List[Bookmaker], typing.List[dict]] = None, total_bet_size: float = -1.0, profit: float = -1.0, wager_count: int = -1) -> None:
        if bookmakers is None:
            bookmakers = []
        else:
            bookmakers = [Bookmaker._from_dict(bookmaker) if isinstance(bookmaker, dict) else bookmaker for bookmaker in bookmakers]

        self.total_bet_size = total_bet_size
        self.profit = profit
        self.wager_count = wager_count
        self.bookmakers = bookmakers
        super().__init__()




ev = Event(bookmakers=[
    Bookmaker(
        wager_limit=135.50,
        bets=[
            Bet(
                1,
                values=[BetValue('home', 2.4, False), BetValue('away', 2.3, True)])
        ])
])

# ev_dict = ev.to_reduced_dict()
# new_ev = ev.uppdate_from_dict(ev_dict)
str_sjon =ev.to_json()
print(str_sjon)


ev.update_self_from_json(str_sjon)

print(ev)
print()
