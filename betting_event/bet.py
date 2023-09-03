import enum
import json
import re
import typing
from os.path import dirname, join

from .bookmaker import Bookmaker

BET_T = typing.TypeVar('BET_T', bound='Bet')

class BetType(enum.Enum):
    """Enum of currently accepted bet types"""
    MatchWinner = 1
    AsianHandicap = 2
    Goals_OverUnder = 3  
    BothTeamsToScore = 4
    ExactScore = 5
    DoubleChance = 6
    Team_OverUnder = 7
    OddEven = 8
    Team_OddEven = 9
    Result_BothTeamsScore = 10
    Result_OverUnder = 11
    TeamCleanSheet = 12
    Team_WinToNil = 13
    TotalGoals = 14
    Team_ExactGoals = 15
    Team_ScoreAGoal = 16

ValueCheck: typing.Dict[BetType, typing.Tuple[typing.Pattern, str, typing.List[str]]] = {
    BetType.MatchWinner:            (re.compile(r"^(home|draw|away)$"), 
        "Value string must be `home` `draw` or `away`.",
        ['home', 'draw', 'away']),

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

    BetType.Team_OverUnder:         (re.compile(r"^(home|away) (over|under) ([0-9]{1,4}).5$"),
        """Value string must be formatted as `TEAM POSITION NUMBER`:
            TEAM: Must be `home` or `away`.
            POSITION: Must be `over` or `under`.
            NUMBER: Must a float divisible by 0.5 between 0.5 and 9999.5.""",
        ['home over 2.5', 'away under 0.5']),

    BetType.OddEven:                (re.compile(r"^(odd|even)$"),
        """Value string must be either `odd` or `even`""",
        ['odd', 'even']),

    BetType.Team_OddEven:           (re.compile(r"^(home|away) (odd|even)$"),
        """Value string must be formatted as `TEAM EVENNESS`:
            TEAM: Must be `home` or `away`.
            EVENNESS: Must be `odd` or `even`""",
        ['home odd', 'away even', 'home even', 'away odd']), 

    BetType.Result_BothTeamsScore:  (re.compile(r"^(home|draw|away)\/(yes|no)$"),
        """Value string must be formatted as `RESULT/SWITCH`:
            RESULT: Must be `home`, `draw` or `away`.
            SWITCH: Must be `yes` or `no`""",
        ['home/yes', 'draw/no', 'away/yes','home/no', 'draw/yes', 'away/no']),

    BetType.Result_OverUnder:       (re.compile(r"^(home|draw|away)\/(over|under) ([0-9]{1,4}).5$"),
        """Value string must be formatted as `RESULT/POSITION NUMBER`:
            RESULT: Must be `home`, `draw` or `away`.
            POSITION: Must be `over` or `under`.
            NUMBER: Must be a float divisible by 0.5. Only positive values are valid.""",
        ['home/over 2.5', 'draw/under 3.5', 'away/over 4.5', 'draw/under 0.5']),

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

    BetType.TotalGoals:             (re.compile(r"^([0-9]{1,4})$"),
        """Value string must be formatted as an integer.""",
        ['2', '3', '4']),

    BetType.Team_ExactGoals:        (re.compile(r"^(home|away) ([0-9]{1,4})$"),
        """Value string must be formatted as `TEAM NUMBER`:
            TEAM: Must be `home` or `away`.
            NUMBER: Must be a positive integer.""",
            ['home 2', 'away 3']),

    BetType.Team_ScoreAGoal:        (re.compile(r"^(home|away) (yes|no)$"),
        """Value string must be formatted as `TEAM SWITCH`:
            TEAM: Must be `home` or `away`.
            SWITCH: Must be `yes` or `no`""",
        ['home yes', 'away no', 'home no', 'away yes']),
}

class Bet:
    DefaultBookmaker = Bookmaker()
    Defaults = json.load(open(join(dirname(__file__), "defaults.json"), "r"))["bet"]

    def __init__(self,
                 bet_type: typing.Union[BetType, str, int],
                 value: str,
                 odds: float,
                 bookmaker: typing.Optional[Bookmaker] = None,
                 lay: bool = Defaults["lay"],
                 volume: float = Defaults["volume"],
                 previous_wager: float = Defaults["previous_wager"], 
                 wager: float = Defaults["wager"]
                 ) -> None:
        """Bet class constructor

        Args:
            bet_type (BetType | int): Bet type or bet type int as defined in bet.BetType.
            value (str): Bet value. The accepted inputs of this is dependent on the bet_type.
            odds (float): The odds for the bet.
            bookmaker (Bookmaker | None): The bookmaker for the bet. If
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

        self.bet_type: BetType = BetType[bet_type] if isinstance(bet_type, str) else BetType(bet_type)
        self.value: str = value
        self.odds: float = odds
        self.lay: bool = lay
        self.volume: float = volume
        self.previous_wager: float = previous_wager
        self.wager: float = wager

        if ValueCheck[self.bet_type][0].fullmatch(self.value.lower()) is None:
            raise ValueError(f"Bet value '{self.value}' is not valid for bet type " +
                f"{self.bet_type.name} ({self.bet_type.value}).\nExpected regex format: " + 
                f"'{ValueCheck[self.bet_type][0].pattern}'\n{ValueCheck[self.bet_type][1]}\"")

    def __eq__(self, __new_bet: object) -> bool:
        if not isinstance(__new_bet, Bet):
            raise NotImplementedError
        return self.bet_type == __new_bet.bet_type and self.bookmaker == __new_bet.bookmaker and \
            self.value == __new_bet.value and self.odds == __new_bet.odds and self.lay == __new_bet.lay

    def as_dict(self) -> dict:
        """Returns the bet as a dictionary.

        Returns:
            dict: This bet represented as a dictionary.
        """
        defaults_removed_dict = {}
        for default_key, default_value in self.Defaults.items():
            current_value = getattr(self, default_key)
            if isinstance(current_value, Bookmaker):
                current_value = current_value._id
            if current_value != default_value:
                defaults_removed_dict[default_key] = current_value

        return {
            **{"bet_type": self.bet_type.name, "value": self.value, "odds": self.odds},
            **defaults_removed_dict
        }

    @classmethod
    def from_dict(cls: typing.Type[BET_T], __bet_dict: dict) -> BET_T:
        """Creates a bet from a dictionary.

        Args:
            __bet_dict (dict): The dictionary to create the bet from.

        Returns:
            Bet: The bet created from the dictionary.
        """

        return cls(**{key: __bet_dict[key] for key in ["bet_type", "value", "odds"]},
                   **{key: __bet_dict[key] for key in cls.Defaults if key in __bet_dict})

    def wager_placed(self):
        "Sets the wager placed to the previous wager + the current wager. Also resets the current wager."
        self.previous_wager += self.wager
        self.wager = 0.0
