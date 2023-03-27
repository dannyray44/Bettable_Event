import enum
import typing
from ..bookmaker import Bookmaker


class BetType(enum.Enum):
    """Enum of currently accepted bet types:"""
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

# class BetBase:
#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.MatchWinner, 1]) -> typing.Type[b_type.MatchWinner]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.AsianHandicap, 4]) -> typing.Type[b_type.AsianHandicap]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.Goals_OverUnder, 5]) -> typing.Type[b_type.Goals_OverUnder]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.BothTeamsToScore, 8]) -> typing.Type[b_type.BothTeamsToScore]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.ExactScore, 10]) -> typing.Type[b_type.ExactScore]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.DoubleChance, 12]) -> typing.Type[b_type.DoubleChance]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.Team_Total, 16]) -> typing.Type[b_type.Team_Total]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.OddEven, 21]) -> typing.Type[b_type.OddEven]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.Team_OddEven, 23]) -> typing.Type[b_type.Team_OddEven]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.Result_BothTeamsScore, 24]) -> typing.Type[b_type.Result_BothTeamsScore]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.Result_TotalGoals, 25]) -> typing.Type[b_type.Result_TotalGoals]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.TeamCleanSheet, 27]) -> typing.Type[b_type.TeamCleanSheet]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.Team_WinToNil, 29]) -> typing.Type[b_type.Team_WinToNil]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.ExactGoalsNumber, 38]) -> typing.Type[b_type.ExactGoalsNumber]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.Team_ExactGoalsNumber, 40]) -> typing.Type[b_type.Team_ExactGoalsNumber]: ...

#     @typing.overload
#     @classmethod
#     def with_bet_type(cls, type: typing.Literal[BetType.Team_ScoreAGoal, 43]) -> typing.Type[b_type.Team_ScoreAGoal]: ...


#     @classmethod
#     def with_bet_type(cls, type: typing.Union[BetType, int]):
#         return getattr(b_type, BetType(type).name)

class BetBase:
    def __init__(self, bet_type: BetType, value: str, odds: float, bookmaker: typing.Optional[Bookmaker] = None, lay: bool = False, volume: float = -1, previous_wager: float = 0):
        self.bet_type = bet_type
        self.value = value
        self.odds = odds
        self.bookmaker = bookmaker
        self.lay = lay
        self.volume = volume
        self.previous_wager = previous_wager

    @typing.overload
    @classmethod
    def from_type(cls, bet_type: typing.Literal[BetType.MatchWinner, 1]) -> 'MatchWinner': ...

    @typing.overload
    @classmethod
    def from_type(cls, bet_type: typing.Literal[BetType.AsianHandicap, 4]) -> 'AsianHandicap': ...

    @classmethod
    def from_type(cls, bet_type: typing.Union[BetType, int]):
        return getattr(__name__, BetType(bet_type).name)


class BetConstructor:
    def __init__(self, bet_type: BetType):
        self.bet_type = BetType(bet_type)

    def __call__(self, *args, **kwargs):
        raise NotImplementedError
    
class MatchWinner(BetConstructor):
    def __call__(self, value: typing.Literal['home', 'draw', 'away'], odds: float, bookmaker: typing.Optional[Bookmaker] = None, lay: bool = False, volume: float = -1, previous_wager: float = 0):
        return BetBase(BetType.MatchWinner, value, odds, bookmaker, lay, volume, previous_wager)
    
class AsianHandicap(BetConstructor):
    def __call__(self, value: str, odds: float, bookmaker: typing.Optional[Bookmaker] = None, lay: bool = False, volume: float = -1, previous_wager: float = 0):
        return BetBase(BetType.AsianHandicap, value, odds, bookmaker, lay, volume, previous_wager)