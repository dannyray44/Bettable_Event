import typing
from .bet import Bet

class Event:
    def __init__(self, wager_limit: float = -1.0, bets: typing.Optional[typing.List[Bet]] = None) -> None:
        self.wager_limit: float = wager_limit
        if bets is None:
            bets = []
        self.bets: typing.List[Bet] = bets
        self.profit: float

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
            self.bets.append(bet)

        else:
            for attribute in bet.__dict__:
                if getattr(self.bets[index], attribute) != getattr(bet, attribute):
                    setattr(self.bets[index], attribute, getattr(bet, attribute))

        return self

    def as_dict(self) -> dict:
        """Returns the event as a dictionary.

        Returns:
            dict: The event as a dictionary.
        """
        return {
            "wager_limit": self.wager_limit,
            "bets": [bet.as_dict() for bet in self.bets]
        }
    
    @classmethod
    def from_dict(cls, __event_dict: dict) -> 'Event':
        """Creates an event from a dictionary.
        
        Args:
            __event_dict (dict): The dictionary to create the event from.
            
        Returns:
            Event: The event created from the dictionary.
        """
        return cls(
            __event_dict["wager_limit"],
            [Bet.from_dict(bet_dict) for bet_dict in __event_dict["bets"]]
        )
