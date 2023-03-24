import enum
import typing
from .bookmaker import Bookmaker
# from .bet_types import MatchWinner, HomeAway
from .type_hinting.bet_base import BetBase, BetType

class Bet(BetBase):
    DefaultBookmaker = Bookmaker()

    def __init__(self,
                 bet_type: typing.Union[BetType, int],
                 value: str,
                 odds: float,
                 lay: bool,
                 bookmaker: typing.Optional[Bookmaker] = None,
                 volume: float = -1.0,
                 previous_wager: float = 0.0
                 ) -> None:
        """Bet class constructor

        Args:
            bet_type (BetType | int): Bet type or bet type int as defined in bet.BetType.
            value (str): Bet value. The accepted inputs of this is dependent on the bet_type.       #TODO: specify where to find
            odds (float): The odds for the bet.
            lay (bool): True if the bet is a lay bet, False if it is a back bet.
            bookmaker (Bookmaker, optional): The bookmaker for the bet. Defaults to Bookmaker(). If not provided, the default bookmaker with no limits will be used.
            volume (float, optional): The volume for the bet (only applies to exchanges). Defaults to -1.0.
            previous_wager (float, optional): The sum of any previous wagers placed on this bet. Defaults to 0.0. Useful for when a bet has been partially matched and you want to recalculate to minaize the risk of a losses.
        """
        if bookmaker is None:
            bookmaker = self.DefaultBookmaker
        self.bookmaker = bookmaker

        self.bet_type: BetType = BetType(bet_type)
        self.value: str = value
        self.odds: float = odds
        self.lay: bool = lay
        self.volume: float = volume
        self.previous_wager: float = previous_wager
        self.wager: float = -1.0

    def __eq__(self, __value: 'Bet') -> bool:
        return self.bet_type == __value.bet_type and self.bookmaker == __value.bookmaker and \
            self.value == __value.value and self.odds == __value.odds and self.lay == __value.lay
