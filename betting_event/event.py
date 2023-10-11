import json
import typing
from os import path

from .bet import BET_T, Bet
from .bookmaker import BOOKMAKER_T, Bookmaker

GLOBAL_DEFAULTS: dict = json.load(open(path.join(path.dirname(__file__), "defaults.json"), "r"))["event"]

class Event:
    DEFAULTS = GLOBAL_DEFAULTS

    _BOOKMAKER_CLASS: typing.Type[BOOKMAKER_T] = Bookmaker
    _BET_CLASS: typing.Type[BET_T] = Bet

    def __init__(self,
                 wager_limit: typing.Optional[float] = None,
                 wager_precision: typing.Optional[float] = None,
                 profit: typing.Optional[typing.List[float]] = None,
                 no_draw: typing.Optional[bool] = None,
                 bookmakers: typing.Optional[typing.List[BOOKMAKER_T]] = None,
                 bets: typing.Optional[typing.List[BET_T]] = None,
                 ) -> None:
    
        self.wager_limit: float = wager_limit if wager_limit is not None else self.DEFAULTS["wager_limit"]
        self.wager_precision: float = wager_precision if wager_precision is not None else self.DEFAULTS["wager_precision"]
        self.profit: typing.List[float] = profit if profit is not None else self.DEFAULTS["profit"]
        self.no_draw: bool = no_draw if no_draw is not None else self.DEFAULTS["no_draw"]

        self.bets: typing.List[BET_T] = []
        self.bookmakers: typing.List[BOOKMAKER_T] = []
        bets = bets if bets is not None else self.DEFAULTS["bets"]
        bookmakers = bookmakers if bookmakers is not None else self.DEFAULTS["bookmakers"]

        for bookmaker in bookmakers:
            self.add_bookmaker(bookmaker)
        self.add_bet(bets)

    def add_bookmaker(self: 'EVENT_T', bookmaker: BOOKMAKER_T) -> 'EVENT_T':
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

    @typing.overload
    def add_bet(self: 'EVENT_T', _new_bets: BET_T) -> 'EVENT_T': pass
    @typing.overload
    def add_bet(self: 'EVENT_T', _new_bets: typing.List[BET_T]) -> 'EVENT_T': pass
    def add_bet(self: 'EVENT_T', _new_bets: typing.Union[typing.List[BET_T], BET_T]) -> 'EVENT_T':
        """Adds multiple bets to the event. Faster that adding them individually.

        Args:
            new_bets (list[Bet] | Bet): The bet or bets to add.

        Returns:
            Event: This event object.
        """
        if not isinstance(_new_bets, list):
            _new_bets = [_new_bets]
        _new_bets = list(set(_new_bets))

        for new_bet in _new_bets[::-1]:
            if new_bet.bookmaker not in self.bookmakers:
                self.add_bookmaker(new_bet.bookmaker)
            else:
                new_bet.bookmaker = self.bookmakers[self.bookmakers.index(new_bet.bookmaker)]

            if new_bet in self.bets:
                self.bets[self.bets.index(new_bet)].update_from_bet(new_bet)
                _new_bets.remove(new_bet)

        self.bets.extend(_new_bets)
        return self

    def as_dict(self, wagers_only: bool = False, verbose: bool = False, necessary_keys_only: bool = True) -> typing.Dict[str, typing.Any]:
        """Returns the event as a dictionary, with values adjusted to match api formatting.

        Returns:
            dict: The event as a dictionary.
        """
        result = self.__dict__
        for key in list(result.keys()):
            if (not verbose and result[key] == self.DEFAULTS.get(key, None)) or (necessary_keys_only and key not in GLOBAL_DEFAULTS):
                del result[key]

        result["bookmakers"] = [bookmaker.as_dict(verbose= verbose, necessary_keys_only= necessary_keys_only) for bookmaker in self.bookmakers]
        result["bets"] = [bet.as_dict(verbose= verbose, necessary_keys_only= necessary_keys_only) for bet in self.bets if not(wagers_only) or bet.wager != 0 or bet.previous_wager != 0]
        return result

    @classmethod
    def from_dict(cls: typing.Type['EVENT_T'], __event_dict: dict) -> 'EVENT_T':
        """Creates an event from a dictionary.

        Args:
            __event_dict (dict): The dictionary to create the event from.

        Returns:
            Event: The event created from the dictionary.
        """

        clean_dict = {}
        for key in cls.DEFAULTS.keys():
            if key in ["bookmakers", "bets"]:
                continue
            if key in __event_dict:
                clean_dict[key] = __event_dict[key]

        current_inst = cls(**clean_dict)

        if "bookmakers" in __event_dict:
            for bookmaker_dict in __event_dict["bookmakers"]:
                current_inst.add_bookmaker(cls._BOOKMAKER_CLASS.from_dict(bookmaker_dict))

        if "bets" in __event_dict:
            new_bets = []
            for bet_dict in __event_dict["bets"]:
                if "bookmaker" in bet_dict:
                    if isinstance(bet_dict["bookmaker"], int):
                        for bookmaker in current_inst.bookmakers:
                            if bookmaker._id == bet_dict["bookmaker"]:
                                bet_dict["bookmaker"] = bookmaker
                                break
                new_bets.append(cls._BET_CLASS(**bet_dict))
            current_inst.add_bet(new_bets)
        else:
            raise ValueError("No bets in event dictionary.")

        return current_inst

EVENT_T = typing.Union[typing.TypeVar('EVENT_T', bound='Event'), Event]
