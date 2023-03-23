import enum
import typing
from .bookmaker import Bookmaker

class BetType(enum.Enum):
    MatchWinner = 1
    HomeAway = 2
    AsianHandicap = 4
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


class Bet:

    @typing.overload
    def __init__(self, bet_type: typing.Union[typing.Literal[1], typing.Literal[BetType.MatchWinner]], value: typing.Literal['home', 'draw', 'away'], odds: float, lay: bool, bookmaker: Bookmaker = Bookmaker(), volume: float = -1.0, previous_wager: float = 0.0) -> None: ...
    @typing.overload
    def __init__(self, bet_type: typing.Union[typing.Literal[2], typing.Literal[BetType.HomeAway]], value: typing.Literal['home', 'away'], odds: float, lay: bool, bookmaker: Bookmaker = Bookmaker(), volume: float = -1.0, previous_wager: float = 0.0) -> None: ...
    def __init__(self,
                 bet_type: typing.Union[BetType, int],
                 value: str,
                 odds: float,
                 lay: bool,
                 bookmaker: Bookmaker = Bookmaker(),
                 volume: float = -1.0,
                 previous_wager: float = 0.0
                 ) -> None:
        
        self.bookmaker = bookmaker
        
        if isinstance(bet_type, int):
            bet_type = BetType(bet_type)
        self.bet_type: BetType = bet_type

        self.value: str = value
        self.odds: float = odds
        self.lay: bool = lay
        self.volume: float = volume
        self.previous_wager: float = previous_wager
        self.wager: float = -1.0

    def __eq__(self, __value: 'Bet') -> bool:
        return self.bet_type == __value.bet_type and self.bookmaker == __value.bookmaker and \
            self.value == __value.value and self.odds == __value.odds and self.lay == __value.lay