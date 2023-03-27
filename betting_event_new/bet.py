import typing
import enum
import re
from .bookmaker import Bookmaker
# from .bet_types import MatchWinner, HomeAway
# from .type_hinting.bet_base import BetBase, BetType
X = 2

class BetType(enum.Enum):
    """Enum of currently accepted bet types:
    
    Attributes:
        MatchWinner: blah blah
        AsianHandicap: ASIAN DOC"""
    MatchWinner = 1
    f"""{X}"""
    # HomeAway = 2
    AsianHandicap = 4
    """ASIAN DOC"""
    Goals_OverUnder = 5       
    BothTeamsToScore = 8      
    ExactScore = 10
    DoubleChance = 12
    Team_Total = 16
    OddEven = 21
    Team_OddEven = 23
    Result_BothTeamsScore = 24
    Result_TotalGoals = 25
    TeamCleanSheet = 27
    Team_WinToNil = 29
    ExactGoalsNumber = 38
    Team_ExactGoalsNumber = 40
    Team_ScoreAGoal = 43

ValueCheck: typing.Dict[BetType, typing.Pattern] = {
    BetType.MatchWinner:            re.compile(r"^(home|draw|away)$"),
    BetType.AsianHandicap:          re.compile(r"^(home|away) ([+-]?[0-9\.]{1,5})$"),
    BetType.Goals_OverUnder:        re.compile(r"^(over|under) ([+-]?[0-9\.]{1,5})$"),
    BetType.BothTeamsToScore:       re.compile(r"^(yes|no)$"),
    BetType.ExactScore:             re.compile(r"^([0-9]{1,4}):([0-9]{1,4})$"),
    BetType.DoubleChance:           re.compile(r"^(home|draw|away)\/(home|draw|away)$"),
    BetType.Team_Total:             re.compile(r"^(home|away) (over|under) ([0-9]*)(.5)?$"),
    BetType.OddEven:                re.compile(r"^(odd|even)$"),
    BetType.Team_OddEven:           re.compile(r"^(home|away) (odd|even)$"),
    BetType.Result_BothTeamsScore:  re.compile(r"^(home|draw|away)\/(yes|no)$"),
    BetType.Result_TotalGoals:      re.compile(r"^(home|draw|away)\/(over|under) ([+-]?[0-9\.]{1,5})$"),
    BetType.TeamCleanSheet:         re.compile(r"^(home|away) (yes|no)$"),
    BetType.Team_WinToNil:          re.compile(r"^(home|away) (yes|no)$"),
    BetType.ExactGoalsNumber:       re.compile(r"^(over|under) ([+-]?[0-9\.]{1,5})$"),
    BetType.Team_ExactGoalsNumber:  re.compile(r"^(home|away) (over|under) ([+-]?[0-9\.]{1,5})$"),
    BetType.Team_ScoreAGoal:        re.compile(r"^(home|away) (yes|no)$")
}

class Bet:
    DefaultBookmaker = Bookmaker()

    def __init__(self,
                 bet_type: typing.Union[BetType, int],
                 value: str,
                 odds: float,
                 bookmaker: typing.Optional[Bookmaker] = None,
                 lay: bool = False,
                 volume: float = -1.0,
                 previous_wager: float = 0.0
                 ) -> None:
        """Bet class constructor

        Args:
            bet_type (BetType | int): Bet type or bet type int as defined in bet.BetType.
            value (str): Bet value. The accepted inputs of this is dependent on the bet_type.
            odds (float): The odds for the bet.
            bookmaker (Bookmaker, optional): The bookmaker for the bet. Defaults to Bookmaker(). If
            not provided, the default bookmaker with no limits will be used.
            volume (float, optional): The volume for the bet (only applies to exchanges). Defaults
            to -1.0.
            lay (bool): True if the bet is a lay bet, False if it is a back bet.
            previous_wager (float, optional): The sum of any previous wagers placed on this bet.
            Defaults to 0.0. Useful for when a bet has been partially matched and you want to
            recalculate to minaize the risk of a losses.
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

        if ValueCheck[self.bet_type].fullmatch(self.value) is None:
            raise ValueError(f"Bet value '{self.value}' is not valid for bet type " +
                             f"{self.bet_type.name} ({self.bet_type.value}).\nExpected format: " +
                             f"\"{ValueCheck[self.bet_type].pattern}\"")

    def __eq__(self, __value: 'Bet') -> bool:
        return self.bet_type == __value.bet_type and self.bookmaker == __value.bookmaker and \
            self.value == __value.value and self.odds == __value.odds and self.lay == __value.lay
