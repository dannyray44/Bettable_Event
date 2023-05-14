import typing
from betting_event.bet import Bet
from betting_event.bookmaker import Bookmaker

class Event:
    def __init__(self, 
                 wager_limit: float = -1.0,
                 bets: typing.Optional[typing.List[Bet]] = None,
                 bookmakers: typing.Optional[typing.List[Bookmaker]] = None) -> None:
        self.wager_limit: float = wager_limit

        if bets is None:
            bets = []
        if bookmakers is None:
            bookmakers = []

        self.bets: typing.List[Bet] = bets
        self.bookmakers: typing.List[Bookmaker] = bookmakers
        self.profit: float
    
    def add_bookmaker(self, bookmaker: Bookmaker) -> 'Event':
        """Adds a bookmaker to the event. If the bookmaker already exists, it will be updated.

        Args:
            bookmaker (Bookmaker): The bookmaker to add.
        
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

    def add_bet_from_dict(self, bet_dict: dict) -> 'Event':
        """Builds a bet from a dict and add it to this event. If the bet already exists, it will be updated.

        Args:
            bet_dict (dict): The bet to add.
        
        Returns:
            Event: This event object.
        """
        id = bet_dict.pop("bookmaker_id", 0)    # Checks bet_dict for valid bookmaker_id
        if not "bookmaker" in bet_dict:
            for bookmaker in self.bookmakers:   
                if bookmaker.__id == id:
                    bet_dict["bookmaker"] = bookmaker   
                    break
            else:
                raise ValueError("The bookmaker with the id {} does not exist in {}".format(id, [bookmaker.as_dict() for bookmaker in self.bookmakers]))

        return self.add_bet(Bet.from_dict(bet_dict))

    def add_bet(self, bet: Bet) -> 'Event':
        """Adds a bet to the event. If the bet already exists, it will be updated.

        Args:
            bet (Bet): The bet to add.
        
        Returns:
            Event: This event object.
        """

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

    def as_dict(self) -> dict:
        """Returns the event as a dictionary, with values adjusted to match api formatting.

        Returns:
            dict: The event as a dictionary.
        """

        return {
            "wager_limit": self.wager_limit,
            "bets": [{key: val for key, val in bet.as_dict().items() if key != "bookmaker"} for bet in self.bets],
            "bookmakers": [bookmaker.as_dict() for bookmaker in self.bookmakers]
        }
    
    @classmethod
    def from_dict(cls, __event_dict: dict) -> 'Event':
        """Creates an event from a dictionary.
        
        Args:
            __event_dict (dict): The dictionary to create the event from.
            
        Returns:
            Event: The event created from the dictionary.
        """

        current_inst= cls(
            wager_limit= __event_dict["wager_limit"],
            bookmakers= [Bookmaker.from_dict(bookmaker_dict) for bookmaker_dict in __event_dict["bookmakers"]]
        )

        for bet in __event_dict["bets"]:
            current_inst.add_bet(Bet.from_dict(bet))

        return current_inst
