import typing
from ..bet import Bet, BetType
from ..bookmaker import Bookmaker

class MatchWinner(Bet):
    ID = 1
    def __init__(self, value: typing.Literal['home', 'draw', 'away'], odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.MatchWinner, value, odds, lay, bookmaker, volume, previous_wager)

class HomeAway(Bet):
    ID = 2
    def __init__(self, value: typing.Literal['home', 'away'], odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.HomeAway, value, odds, lay, bookmaker, volume, previous_wager)

class AsianHandicap(Bet):
    ID = 4
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.AsianHandicap, value, odds, lay, bookmaker, volume, previous_wager)

class Goals_OverUnder(Bet):
    ID= 5
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.Goals_OverUnder, value, odds, lay, bookmaker, volume, previous_wager)

class BothTeamsToScore(Bet):
    ID= 8
    def __init__(self, value: typing.Literal['yes', 'no'], odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.BothTeamsToScore, value, odds, lay, bookmaker, volume, previous_wager)

class ExactScore(Bet):
    ID= 10
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.ExactScore, value, odds, lay, bookmaker, volume, previous_wager)

class DoubleChance(Bet):
    ID= 12
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.DoubleChance, value, odds, lay, bookmaker, volume, previous_wager)

class Team_Total(Bet):
    ID= 16
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.Team_Total, value, odds, lay, bookmaker, volume, previous_wager)

class OddEven(Bet):
    ID= 21
    def __init__(self, value: typing.Literal['odd', 'even'], odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.OddEven, value, odds, lay, bookmaker, volume, previous_wager)

class Team_OddEven(Bet):
    ID= 23
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.Team_OddEven, value, odds, lay, bookmaker, volume, previous_wager)

class Result_BothTeamsScore(Bet):
    ID= 24
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.Result_BothTeamsScore, value, odds, lay, bookmaker, volume, previous_wager)

class Result_TotalGoals(Bet):
    ID= 25
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.Result_TotalGoals, value, odds, lay, bookmaker, volume, previous_wager)

class TeamCleanSheet(Bet):
    ID= 27
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.TeamCleanSheet, value, odds, lay, bookmaker, volume, previous_wager)

class Team_WinToNil(Bet):
    ID= 29
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.Team_WinToNil, value, odds, lay, bookmaker, volume, previous_wager)

class ExactGoalsNumber(Bet):
    ID= 38
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.ExactGoalsNumber, value, odds, lay, bookmaker, volume, previous_wager)

class Team_ExactGoalsNumber(Bet):
    ID= 40
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.Team_ExactGoalsNumber, value, odds, lay, bookmaker, volume, previous_wager)

class Team_ScoreAGoal(Bet):
    ID= 43
    def __init__(self, value: str, odds: float, lay: bool, bookmaker: typing.Optional[Bookmaker] = None, volume: float = -1, previous_wager: float = 0) -> None:
        super().__init__(BetType.Team_ScoreAGoal, value, odds, lay, bookmaker, volume, previous_wager)

