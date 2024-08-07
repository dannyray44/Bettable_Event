import json
import typing
from enum import Enum
from os import path

from .bet import BET_T, Bet
from .bookmaker import BOOKMAKER_T, Bookmaker

GLOBAL_DEFAULTS: dict = json.load(open(path.join(path.dirname(__file__), "defaults.json"), "r"))["event"]

class MODES(Enum):
    GuaranteedProfit = 1
    # ExpectedResults = 2
    MaxProfit = 2
    ForceWager = 3

class Event:
    DEFAULTS = GLOBAL_DEFAULTS

    _BOOKMAKER_CLASS: typing.Type[BOOKMAKER_T] = Bookmaker
    _BET_CLASS: typing.Type[BET_T] = Bet

    def __init__(self,
                 wager_limit: typing.Optional[float] = None,
                 wager_precision: typing.Optional[float] = None,
                 profit: typing.Optional[typing.List[float]] = None,
                 no_draw: typing.Optional[bool] = None,
                 max_process_time: typing.Optional[float] = None,
                 total_max_wager_count: typing.Optional[int] = None,
                 mode: typing.Optional[typing.Union[int, str]] = None,
                 bookmakers: typing.Optional[typing.List[BOOKMAKER_T]] = None,
                 bets: typing.Optional[typing.List[BET_T]] = None,
                 **kwargs: typing.Any
                 ) -> None:

        self.wager_limit: float = self.DEFAULTS["wager_limit"] if wager_limit is None else float(wager_limit)
        self.wager_precision: float = self.DEFAULTS["wager_precision"] if wager_precision is None else float(wager_precision)
        self.profit: typing.List[float] = self.DEFAULTS["profit"] if profit is None else [float(p) for p in profit]
        self.no_draw: bool = self.DEFAULTS["no_draw"] if no_draw is None else bool(no_draw)
        self.max_process_time: float = self.DEFAULTS["max_process_time"] if max_process_time is None else float(max_process_time)
        self.total_max_wager_count: int = self.DEFAULTS["total_max_wager_count"] if total_max_wager_count is None else int(total_max_wager_count)
        if mode is None:
            mode = self.DEFAULTS["mode"]

        try:
            self.mode: MODES = MODES(mode) if not isinstance(mode, str) else MODES[mode]
        except ValueError:
            kwargs["errors"] = kwargs.get("errors", []) + [f'Inappropriate "mode": {mode}. Valid modes are: {", ".join([f"{mode.name}: {mode.value}" for mode in MODES])}']
            self.mode = MODES(1)

        self.bets: typing.List[BET_T] = []
        self.bookmakers: typing.List[BOOKMAKER_T] = []
        bets = bets if bets is not None else self.DEFAULTS["bets"]
        bookmakers = bookmakers if bookmakers is not None else self.DEFAULTS["bookmakers"]

        for bookmaker in bookmakers:
            self.add_bookmaker(bookmaker)
        self.add_bet(bets)

        self.errors: typing.List[str] = kwargs.pop("errors", [])
        self.__kwargs: typing.Dict[str, typing.Any] = kwargs

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
    def add_bet(self: 'EVENT_T', _new_bets: BET_T) -> 'EVENT_T': 
        """Adds a bet to the event. If the bet already exists, it will be updated.
        
        Args:
            new_bet (Bet): The bet to add.

        Returns:
            Event: This event object.
        """
        pass

    @typing.overload
    def add_bet(self: 'EVENT_T', _new_bets: typing.List[BET_T]) -> 'EVENT_T':
        """Adds multiple bets to the event. Faster that adding them individually.
        
        Args:
            new_bets (list[Bet]): The bets to add.

        Returns:
            Event: This event object.
        """
        pass

    def add_bet(self: 'EVENT_T', _new_bets: typing.Union[typing.List[BET_T], BET_T]) -> 'EVENT_T':
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
        result = self.__dict__.copy()
        # result["_Event__kwargs"]["errors"].extend(result["errors"])

        if "mode" in result:
            result["mode"] = result["mode"].value

        for key in list(result.keys()):
            if key == "_Event__kwargs" or key == "errors":
                continue
            if (not verbose and result[key] == self.DEFAULTS.get(key, None)) or (necessary_keys_only and key not in GLOBAL_DEFAULTS):
                del result[key]
        result.update(result.pop("_Event__kwargs", {}))
        if not result["errors"]:
            del result["errors"]

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
        for key in __event_dict:
            if key in ["bookmakers", "bets"]:
                continue
            if key in cls.DEFAULTS:
                clean_dict[key] = __event_dict[key]

        current_inst = cls(**clean_dict)

        if "bookmakers" in __event_dict:
            for bookmaker_dict in __event_dict["bookmakers"]:
                current_inst.add_bookmaker(cls._BOOKMAKER_CLASS.from_dict(bookmaker_dict))

        if "bets" in __event_dict:
            new_bets: typing.List[BET_T] = []
            for bet_dict in __event_dict["bets"]:
                if "bookmaker" in bet_dict:
                    if not issubclass(type(bet_dict["bookmaker"]), Bookmaker):
                        for bookmaker in current_inst.bookmakers:
                            if bookmaker.id == bet_dict["bookmaker"]:
                                bet_dict["bookmaker"] = bookmaker
                                break
                        else:
                            if isinstance(bet_dict["bookmaker"], dict):
                                new_bookmaker = Bookmaker.from_dict(bet_dict["bookmaker"])
                            else:
                                new_bookmaker = Bookmaker(id= bet_dict["bookmaker"])
                            current_inst.add_bookmaker(new_bookmaker)
                            bet_dict["bookmaker"] = new_bookmaker
                try:
                    new_bet = cls._BET_CLASS.from_dict(bet_dict)
                except Exception as err:
                    current_inst.errors.append(str(err))
                else:
                    new_bets.append(new_bet)

            current_inst.add_bet(new_bets)

        # if not current_inst.wager_limit:
        #     if all(bookmaker.wager_limit == -1 for bookmaker in current_inst.bookmakers):
        #         current_inst.wager_limit = 100.0
        #     else:
        #         current_inst.wager_limit = sum(bookmaker.wager_limit for bookmaker in current_inst.bookmakers if bookmaker.wager_limit != -1)

        if not isinstance(current_inst.wager_limit, float) or (current_inst.wager_limit < 0 and current_inst.wager_limit != -1):
            current_inst.errors.append(f'Inappropriate "wager_limit": {current_inst.wager_limit} must be a positive float or -1')
        if not isinstance(current_inst.wager_precision, float) or current_inst.wager_precision <= 0:
            current_inst.errors.append(f'Inappropriate "wager_precision": {current_inst.wager_precision} must be a positive float')
        if not isinstance(current_inst.profit, list) or len(current_inst.profit) != 2 or any(not isinstance(p, float) for p in current_inst.profit):
            current_inst.errors.append(f'Inappropriate "profit": {current_inst.profit} must be a list of two floats')
        if not isinstance(current_inst.no_draw, bool):
            current_inst.errors.append(f'Inappropriate "no_draw": {current_inst.no_draw} must be a bool. "false" also accepted')

        # print(current_inst.bets[0].bookmaker)
        return current_inst

EVENT_T = typing.Union[typing.TypeVar('EVENT_T', bound='Event'), Event]
