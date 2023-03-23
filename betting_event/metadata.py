from enum import Enum

class BetType(Enum):
    """Bet type enum
    
    ID: | Name:                     Acce
    ----|-----------------------|
    1   | Team_ExactGoalsNumber |
    1 - Match Winner
    """
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
