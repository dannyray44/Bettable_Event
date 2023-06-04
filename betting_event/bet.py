import typing
import enum
import re
from betting_event.bookmaker import Bookmaker


class BetType(enum.Enum):
    """Enum of currently accepted bet types"""
    MatchWinner = 1
    # HomeAway = 2
    AsianHandicap = 2
    Goals_OverUnder = 3  
    BothTeamsToScore = 4
    ExactScore = 5
    DoubleChance = 6
    Team_Total = 7
    OddEven = 8
    Team_OddEven = 9
    Result_BothTeamsScore = 10
    Result_TotalGoals = 11
    TeamCleanSheet = 12
    Team_WinToNil = 13
    ExactGoalsNumber = 14
    Team_ExactGoalsNumber = 15
    Team_ScoreAGoal = 16


ValueCheck: typing.Dict[BetType, typing.Tuple[typing.Pattern, str, typing.List[str]]] = {
    BetType.MatchWinner:            (re.compile(r"^(home|draw|away)$"), 
        "Value string must be `home` `draw` or `away`.",
        ["home", "draw", "away"]),

    BetType.AsianHandicap:          (re.compile(r"^(home|away) ([+-]?\d+(?:\.(?:0|25|5|75))?)$"),
        """Value string must be formatted as `TEAM NUMBER`:
            TEAM: Must be `home` or `away`.
            NUMBER: Must be a float divisible by 0.25 (Or 0.0). Negative and positive values are valid.""",
        ['home -0.75', 'away -3.0', 'home 4.25', 'away 1.75']),

    BetType.Goals_OverUnder:        (re.compile(r"^(over|under) ([+-]?\d+(?:\.(?:0|25|5|75))?)$"),
        """Value string must be formatted as `POSITION NUMBER`:
            POSITION: Must be `over` or `under`.
            NUMBER: Must be a float divisible by 0.25.""",
        ['over 0.75', 'under 3.0', 'over 4.25', 'under 1.75']),

    BetType.BothTeamsToScore:       (re.compile(r"^(yes|no)$"),
        "Value string must be either `yes` or `no`",
        ['yes', 'no']),

    BetType.ExactScore:             (re.compile(r"^([0-9]{1,4}):([0-9]{1,4})$"),
        """Value string must be formatted as `HOME_SCORE:AWAY_SCORE`:
            HOME_SCORE and AWAY_SCORE: Must be an integer number between 0 and 9999.""",
        ['2:1']),

    BetType.DoubleChance:           (re.compile(r"^(home|draw|away)\/(home|draw|away)$"),
        """Value string must be formatted as `RESULT_A/RESULT_B`
            RESULT_A and RESULT_B: Must be `home`, `draw` or `away`. And RESULT_A != RESULT_B""",
        ['home/draw', 'home/away', 'draw/home', 'draw/away', 'away/home', 'away/draw']),

    BetType.Team_Total:             (re.compile(r"^(home|away) (over |under )?([0-9]*)(.5)?$"),
        """Value string must be formatted as `TEAM POSITION NUMBER`:
            TEAM: Must be `home` or `away`.
            POSITION: Must be `over` or `under`.
            NUMBER: Must be either an integer number between 0 and 9999 or a float divisible by 0.5.
            Number must be greater than or equal to 0.5.""",
        ['home over 2.5', 'away under 3.5', 'home over 4', 'away under 0.5']),

    BetType.OddEven:                (re.compile(r"^(odd|even)$"),
        """Value string must be either `odd` or `even`""",
        ['odd', 'even']),

    BetType.Team_OddEven:           (re.compile(r"^(home|away) (odd|even)$"),
        """Value string must be formatted as `TEAM EVENNESS`:
            TEAM: Must be `home` or `away`.
            EVENNESS: Must be `odd` or `even`""",
        ['home odd', 'away even', 'home even', 'away odd']), 

    BetType.Result_BothTeamsScore:  (re.compile(r"^(home|draw|away)\/(yes|no)$"),
        """Value string must be formatted as `TEAM/SWITCH`:
            TEAM: Must be `home`, `draw` or `away`.
            SWITCH: Must be `yes` or `no`""",
        ['home/yes', 'draw/no', 'away/yes','home/no', 'draw/yes', 'away/no']),

    BetType.Result_TotalGoals:      (re.compile(r"^(home|draw|away)\/(over|under) (\d+(?:\.(?:0|5))?)$"),
        """Value string must be formatted as `TEAM/POSITION NUMBER`:
            TEAM: Must be `home`, `draw` or `away`.
            POSITION: Must be `over` or `under`.
            NUMBER: Must be a float divisible by 0.5 (Or 0.0). Only positive values are valid.""",
        ['home/over 2.5', 'draw/under 3.5', 'away/over 4.0', 'draw/under 0.5']),

    BetType.TeamCleanSheet:         (re.compile(r"^(home|away) (yes|no)$"),
        """Value string must be formatted as `TEAM CLEAN_SHEET`:
            TEAM: Must be `home` or `away`.
            CLEAN_SHEET: Must be `yes` or `no`""",
        ['home yes', 'away no']),

    BetType.Team_WinToNil:          (re.compile(r"^(home|away) (yes|no)$"),
        """Value string must be formatted as `TEAM WIN_TO_NIL`:
            TEAM: Must be `home` or `away`.
            WIN_TO_NIL: Must be `yes` or `no`""",
        ['home no', 'away yes', 'home yes', 'away no']),

    BetType.ExactGoalsNumber:       (re.compile(r"^(over |under )?(\d+)$"),
        """Value string must be formatted as `POSITION? NUMBER`:
            POSITION (Optional): Must be `over` or `under`.
            NUMBER: Must be an integer.""",
        ['2', '3.0', 'over 2.5', 'under 3.5', 'over 4.0', 'under 0.5']),

    BetType.Team_ExactGoalsNumber:  (re.compile(r"^(home|away) (over |under )?(\d+)$"),
        """Value string must be formatted as `TEAM POSITION? NUMBER`:
            TEAM: Must be `home` or `away`.
            POSITION (Optional): Must be `over` or `under`.
            NUMBER: Must be an integer.""",
            ['home 2', 'away 3.0']),

    BetType.Team_ScoreAGoal:        (re.compile(r"^(home|away) (yes|no)$"),
        """Value string must be formatted as `TEAM SWITCH`:
            TEAM: Must be `home` or `away`.
            SWITCH: Must be `yes` or `no`""",
        ['home yes', 'away no', 'home no', 'away yes']),
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
            bookmaker (Bookmaker | None): The bookmaker for the bet. Defaults to Bookmaker(). If
            not provided, the default bookmaker with no limits will be used.
            volume (float): The volume for the bet (only applies to exchanges). Defaults
            to -1.0, meaning no volume specified.
            lay (bool): True if the bet is a lay bet, False if it is a back bet.
            previous_wager (float): The sum of any previous wagers placed on this bet.
            Defaults to 0.0. Useful for when a bet has been partially matched and you want to
            recalculate.
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

        if ValueCheck[self.bet_type][0].fullmatch(self.value) is None:
            raise ValueError(f"Bet value '{self.value}' is not valid for bet type " +
                f"{self.bet_type.name} ({self.bet_type.value}).\nExpected regex format: " + 
                f"'{ValueCheck[self.bet_type][0].pattern}'\n{ValueCheck[self.bet_type][1]}\"")

    def __eq__(self, __new_bet: 'Bet') -> bool:
        return self.bet_type == __new_bet.bet_type and self.bookmaker == __new_bet.bookmaker and \
            self.value == __new_bet.value and self.odds == __new_bet.odds and self.lay == __new_bet.lay

    def as_dict(self) -> dict:
        """Returns the bet as a dictionary.

        Returns:
            dict: The bet as a dictionary.
        """

        return {
            "bet_type": self.bet_type.value,
            "value": self.value,
            "odds": self.odds,
            "bookmaker": self.bookmaker,
            "bookmaker_id": self.bookmaker._id, # type: ignore
            "lay": self.lay,
            "volume": self.volume,
            "previous_wager": self.previous_wager,
            "wager": self.wager
        }

    @classmethod
    def from_dict(cls, __bet_dict: dict) -> 'Bet':
        """Creates a bet from a dictionary.

        Args:
            __bet_dict (dict): The dictionary to create the bet from.

        Returns:
            Bet: The bet created from the dictionary.
        """

        keys = ["bet_type", "value", "odds", "bookmaker", "lay", "volume", "previous_wager"]
        return cls(**{key: __bet_dict[key] for key in keys if key in __bet_dict})
