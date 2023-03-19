# from typing import Dict, Tuple

from enum import Enum

# BET_TYPE_TABLE: Dict[int, Tuple[str, str, int]] = {
# #   ID: (NAME,                      REGEX MATCH FOR VALUE                           RESULT SPACE TYPE: [0: full time])
#     1:  ("Match Winner",            "^(home|draw|away)$",                           0),
#     2:  ("Home/Away",               "^(home|away)$",                                0),
#     4:  ("Asian Handicap",          "^(home|away) ([+-]?[0-9\.]{1,5})$",            0),
#     5:  ("Goals Over/Under",        "^(over|under) ([+-]?[0-9\.]{1,5})$",           0),
#     8:  ("Both Teams To Score",     "^(yes|no)$",                                   0),
#     # 9:  ("Handicap Result",         "^(home|draw|away) ([+-]?\d+)$",              0),
#     10: ("Exact Score",             "^([0-9]{1,2}):([0-9]{1,2})$",                  0),
#     12: ("Double Chance",           "^(home|draw|away)\/(home|draw|away)$",         0),
#     16: ("Team Total",              "^(home|away) (over|under) ([0-9]*)(.5)?$",     0),
#     21: ("Odd/Even",                "^(odd|even)$",                                 0),
#     23: ("Team Odd/Even",           "^(home|away) (odd|even)$",                     0),
#     24: ("Result/Both Teams Score", "^(home|draw|away)\/(yes|no)$",                 0),
#     25: ("Result/Total Goals",      "^(home|draw|away)\/(over|under) ([0-9]*).5$",  0),
#     27: ("Team Clean Sheet",        "^(home|away) (yes|no)$",                       0),
#     29: ("Team Win To Nil",         "^(home|away) (yes|no)$",                       0),
#     38: ("Exact Goals Number",      "^(more )?([0-9]*)$",                           0),
#     40: ("Team Exact Goals Number", "^(home|away) (more )?([0-9]*)$",               0),
#     43: ("Team Score A Goal",       "^(home|away) (yes|no)$",                       0)
# }

class BetType(Enum):
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
