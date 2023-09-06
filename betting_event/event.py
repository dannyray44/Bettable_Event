import json
import typing
from os.path import dirname, join

from .bet import BET_T, Bet
from .bookmaker import BOOKMAKER_T, Bookmaker

EVENT_T = typing.TypeVar('EVENT_T', bound='Event')

class Event:
    _BOOKMAKER_CLASS = Bookmaker
    _BET_CLASS = Bet
    DEFAULTS: dict = json.load(open(join(dirname(__file__), "defaults.json"), "r"))["event"]
    DEFAULTS["profit"] = tuple(DEFAULTS["profit"])

    def __init__(self,
                 wager_limit: float = DEFAULTS['wager_limit'],
                 wager_precision: float = DEFAULTS['wager_precision'],
                 profit: list[float] = DEFAULTS['profit'],
                 no_draw: bool = DEFAULTS['no_draw'],
                 bookmakers: typing.Optional[typing.List[BOOKMAKER_T]] = None,
                 bets: typing.Optional[typing.List[BET_T]] = None
                 ) -> None:
    
        self.wager_limit: float = wager_limit
        self.wager_precision: float = wager_precision
        self.profit: tuple[float, float] = tuple(profit) # type: ignore
        self.no_draw: bool = no_draw

        if bets is None:
            bets = []
        if bookmakers is None:
            bookmakers = []

        self.bets: typing.List[BET_T] = bets
        self.bookmakers: typing.List[BOOKMAKER_T] = bookmakers

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
            bet (Bet): The bet to add/update.
        
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

    def as_dict(self, wagers_only: bool = False) -> typing.Dict[str, typing.Any]:
        """Returns the event as a dictionary, with values adjusted to match api formatting.

        Returns:
            dict: The event as a dictionary.
        """
        result = {}
        for default_key, default_value in self.DEFAULTS.items():
            if default_key in ["bookmakers", "bets"]:
                continue
            current_value = getattr(self, default_key)
            if current_value != default_value:
                result[default_key] = current_value

        result["bookmakers"] = [bookmaker.as_dict() for bookmaker in self.bookmakers]
        result["bets"] = [{key: val for key, val in bet.as_dict().items()} for bet in self.bets if not(wagers_only) or bet.wager != 0]
        return result

    @classmethod
    def from_dict(cls: typing.Type[EVENT_T], __event_dict: dict) -> EVENT_T:
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
            if key in __event_dict: # and __event_dict[key] != cls.DEFAULTS[key]:
                clean_dict[key] = __event_dict[key]
                if key == "profit" and isinstance(clean_dict[key], list):
                    clean_dict[key] = tuple(clean_dict[key])

        # clean_dict["profit"] = tuple(clean_dict["profit"])

        if "bookmakers" in __event_dict:
            clean_dict["bookmakers"] = [cls._BOOKMAKER_CLASS.from_dict(bookmaker_dict) for bookmaker_dict in __event_dict["bookmakers"]]

        current_inst = cls(**clean_dict)

        if "bets" in __event_dict:
            for bet_dict in __event_dict["bets"]:
                if "bookmaker" in bet_dict and isinstance(bet_dict["bookmaker"], int):
                    for bookmaker in current_inst.bookmakers:
                        if bookmaker._id == bet_dict["bookmaker"]:
                            bet_dict["bookmaker"] = bookmaker
                            break
                    else:
                        bet_dict["bookmaker"] = cls._BET_CLASS.DefaultBookmaker

                current_inst.add_bet(cls._BET_CLASS.from_dict(bet_dict))
        else:
            raise ValueError("No bets in event dictionary.")

        return current_inst

    def send_to_RapidAPI(self, api_key: str) -> 'Event':
        """Sends the event to the multi-market calculator at RapidAPI to calculate the optimal
        wagers.

        Args:
            api_key (str): Your 'X-RapidAPI-Key' provided when you signed up.

        Returns:
            Event: The event with the wagers updated.
        """
        
        url = "https://multi-market-calculator.p.rapidapi.com/MultiMarket"
        payload = json.dumps(self.as_dict())
        headers = {
            'content-type': "application/json",
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': "multi-market-calculator.p.rapidapi.com"
        }

        res = requests.post(url, json=payload, headers=headers)

        print(res.json())

        if res.status_code != 200:
            print("Error sending event to RapidAPI: ", res.json())
            return self

        updated_event = Event.from_dict(json.loads(res.json()))

        for updated_bet in updated_event.bets:
            self.add_bet(updated_bet)

        self.profit = updated_event.profit

        return self
