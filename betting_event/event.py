import typing

from .bet import BET_T, Bet
from .bookmaker import BOOKMAKER_T, Bookmaker

EVENT_T = typing.TypeVar('EVENT_T', bound='Event')

class Event:
    _BOOKMAKER_CLASS = Bookmaker
    _BET_CLASS = Bet

    def __init__(self, 
                 wager_limit: float = -1.0,
                 bets: typing.Optional[typing.List[BET_T]] = None,
                 bookmakers: typing.Optional[typing.List[BOOKMAKER_T]] = None,
                 wager_precision: float = 0.01) -> None:
        self.wager_limit: float = wager_limit
        self.wager_precision: float = wager_precision

        if bets is None:
            bets = []
        if bookmakers is None:
            bookmakers = []

        self.bets: typing.List[BET_T] = bets
        self.bookmakers = bookmakers
        self.profit: float

    def add_bookmaker(self: EVENT_T, bookmaker) -> EVENT_T:
        """Adds a bookmaker to the event. If the bookmaker already exists, it will be updated.

        Args:
            bookmaker: The bookmaker to add.
        
        Returns:
            Event: This event object.
        """

        try:
            index = self.bookmakers.index(bookmaker)

        except ValueError:
            self.bookmakers.append(bookmaker)

        else:
            for attribute in bookmaker.__dict__:
                if getattr(self.bookmakers[index], attribute) != getattr(bookmaker, attribute):
                    setattr(self.bookmakers[index], attribute, getattr(bookmaker, attribute))

        return self

    def add_bet(self: EVENT_T, bet) -> EVENT_T:
        """Adds a bet to the event. If the bet already exists, it will be updated.

        Args:
            bet (Bet): The bet to add.
        
        Returns:
            Event: This event object.
        """

        if isinstance(bet.bookmaker, int):
            for bookmaker in self.bookmakers:
                if bookmaker._id == bet.bookmaker:
                    bet.bookmaker = bookmaker
                    break
            else:
                bet.bookmaker = bet.DefaultBookmaker

        try:
            index = self.bets.index(bet)
        except ValueError:
            if bet.bookmaker not in self.bookmakers:
                self.add_bookmaker(bet.bookmaker)
            self.bets.append(bet)
        else:
            for attribute in bet.__dict__:
                if getattr(self.bets[index], attribute) != getattr(bet, attribute):
                    setattr(self.bets[index], attribute, getattr(bet, attribute))

        return self

    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns the event as a dictionary, with values adjusted to match api formatting.

        Returns:
            dict: The event as a dictionary.
        """

        return {
            "wager_limit": self.wager_limit,
            "bets": [{key: val for key, val in bet.as_dict().items()} for bet in self.bets],
            "bookmakers": [bookmaker.as_dict() for bookmaker in self.bookmakers],
            "wager_precision": self.wager_precision
        }

    @classmethod
    def from_dict(cls: typing.Type[EVENT_T], __event_dict: dict) -> EVENT_T:
        """Creates an event from a dictionary.
        
        Args:
            __event_dict (dict): The dictionary to create the event from.
            
        Returns:
            Event: The event created from the dictionary.
        """

        current_inst= cls(
            wager_limit= __event_dict["wager_limit"],
            bookmakers= [cls._BOOKMAKER_CLASS.from_dict(bookmaker_dict) for bookmaker_dict in __event_dict["bookmakers"]],
            wager_precision= __event_dict["wager_precision"]
        )

        for bet_dict in __event_dict["bets"]:
            if isinstance(bet_dict["bookmaker"], int):
                for bookmaker in current_inst.bookmakers:
                    if bookmaker._id == bet_dict["bookmaker"]:
                        bet_dict["bookmaker"] = bookmaker
                        break
                else:
                    bet_dict["bookmaker"] = cls._BET_CLASS.DefaultBookmaker

            current_inst.add_bet(cls._BET_CLASS.from_dict(bet_dict))

        return current_inst
