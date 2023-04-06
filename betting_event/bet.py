import typing
import enum
import re
from .bookmaker import Bookmaker


class BetType(enum.Enum):
    """Enum of currently accepted bet types"""
    MatchWinner = 1
    # HomeAway = 2
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


ValueCheck: typing.Dict[BetType, typing.Tuple[typing.Pattern, str]] = {
    BetType.MatchWinner:            (re.compile(r"^(home|draw|away)$"), 
        """Value string must be `home` `draw` or `away`.\nExample: `home`"""),
    BetType.AsianHandicap:          (re.compile(r"^(home|away) ([+-]?\d+(?:\.(?:0|25|5|75))?)$"),
        """Value string must be formatted as `TEAM NUMBER`:
            TEAM: Must be `home` or `away`.
            NUMBER: Must be a float divisible by 0.25 (Or 0.0). Negative and positive values are valid.
        Examples: `home -0.75`, `away -3.0`, `home 4.25`, `away 1.75`"""),
    BetType.Goals_OverUnder:        (re.compile(r"^(over|under) ([+-]?\d+(?:\.(?:0|25|5|75))?)$"),
        """Value string must be formatted as `POSITION NUMBER`:
            POSITION: Must be `over` or `under`.
            NUMBER: Must be a float divisible by 0.25 (Or 0.0). Negative and positive values are valid.
        Examples: `over -0.75`, `under -3.0`, `over 4.25`, `under 1.75`"""),
    BetType.BothTeamsToScore:       (re.compile(r"^(yes|no)$"),
        "Value string must be either `yes` or `no`\nExample: `yes`"),
    BetType.ExactScore:             (re.compile(r"^([0-9]{1,4}):([0-9]{1,4})$"),
        """Value string must be formatted as `HOME_SCORE:AWAY_SCORE`:
            HOME_SCORE and AWAY_SCORE: Must be an integer number between 0 and 9999.
        Example: `2:1`"""),
    BetType.DoubleChance:           (re.compile(r"^(home|draw|away)\/(home|draw|away)$"),
        """Value string must be formatted as `RESULT_A/RESULT_B`
            RESULT_A and RESULT_B: Must be `home`, `draw` or `away`. And RESULT_A != RESULT_B
        Example: `home/draw`"""),
    BetType.Team_Total:             (re.compile(r"^(home|away) (over |under )?([0-9]*)(.5)?$"),
        """Value string must be formatted as `TEAM POSITION NUMBER`:
            TEAM: Must be `home` or `away`.
            POSITION: Must be `over` or `under`.
            NUMBER: Must be either an integer number between 0 and 9999 or a float divisible by 0.5.
            Number must be greater than or equal to 0.5.
        Examples: `home over 2.5`, `away under 3.5`, `home over 4`, `away under 0.5`"""),
    BetType.OddEven:                (re.compile(r"^(odd|even)$"),
        """Value string must be either `odd` or `even`\nExample: `odd`"""),
    BetType.Team_OddEven:           (re.compile(r"^(home|away) (odd|even)$"),
        """Value string must be formatted as `TEAM EVENES`:
            TEAM: Must be `home` or `away`.
            EVENES: Must be `odd` or `even`
        Example: `home odd`"""),
    BetType.Result_BothTeamsScore:  (re.compile(r"^(home|draw|away)\/(yes|no)$"),
        """Value string must be formatted as `TEAM/SWITCH`:
            TEAM: Must be `home`, `draw` or `away`.
            SWITCH: Must be `yes` or `no`
        Example: `home/yes`"""),
    BetType.Result_TotalGoals:      (re.compile(r"^(home|draw|away)\/(over|under) (\d+(?:\.(?:0|5))?)$"),
        """Value string must be formatted as `TEAM/POSITION NUMBER`:
            TEAM: Must be `home`, `draw` or `away`.
            POSITION: Must be `over` or `under`.
            NUMBER: Must be a float divisible by 0.5 (Or 0.0). Only positive values are valid.
        Examples: `home/over 2.5`, `draw/under 3.5`, `away/over 4.0`, `draw/under 0.5`"""),
    BetType.TeamCleanSheet:         (re.compile(r"^(home|away) (yes|no)$"),
        """Value string must be formatted as `TEAM SWITCH`:
            TEAM: Must be `home` or `away`.
            SWITCH: Must be `yes` or `no`
        Example: `home yes`"""),
    BetType.Team_WinToNil:          (re.compile(r"^(home|away) (yes|no)$"),
        """Value string must be formatted as `TEAM SWITCH`:
            TEAM: Must be `home` or `away`.
            SWITCH: Must be `yes` or `no`
        Example: `home yes`"""),
    BetType.ExactGoalsNumber:       (re.compile(r"^(\d+)$"),
        """Value string must be formatted as `POSITION? NUMBER`:
            POSITION: Is optional if present it must be `over` or `under`.
            NUMBER: Must be an integer.
        Examples: `over 2.5`, `under 3.5`, `over 4.0`, `under 0.5`"""),
    BetType.Team_ExactGoalsNumber:  (re.compile(r"^(home|away) (\d+)$"),
        """Value string must be formatted as `TEAM POSITION? NUMBER`:
            TEAM: Must be `home` or `away`.
            NUMBER: Must be an integer.
        """),
    BetType.Team_ScoreAGoal:        (re.compile(r"^(home|away) (yes|no)$"),
        """Value string must be formatted as `TEAM SWITCH`:
            TEAM: Must be `home` or `away`.
            SWITCH: Must be `yes` or `no`
        Example: `home yes`"""),
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

        if ValueCheck[self.bet_type][0].fullmatch(self.value) is None:
            raise ValueError(f"Bet value '{self.value}' is not valid for bet type " +
                f"{self.bet_type.name} ({self.bet_type.value}).\nExpected regex format: " + 
                f"'{ValueCheck[self.bet_type][0].pattern}'\n{ValueCheck[self.bet_type][1]}\"")

    def __eq__(self, __value: 'Bet') -> bool:
        return self.bet_type == __value.bet_type and self.bookmaker == __value.bookmaker and \
            self.value == __value.value and self.odds == __value.odds and self.lay == __value.lay

    def as_dict(self) -> dict:
        """Returns the bet as a dictionary.

        Returns:
            dict: The bet as a dictionary.
        """
        return {
            "bet_type": self.bet_type.value,
            "value": self.value,
            "odds": self.odds,
            "bookmaker": self.bookmaker.as_dict(),
            "lay": self.lay,
            "volume": self.volume,
            "previous_wager": self.previous_wager,
            "wager": self.wager
        }

    @classmethod
    def from_dict(cls, bet_dict: dict) -> 'Bet':
        """Creates a bet from a dictionary.

        Args:
            bet_dict (dict): The dictionary to create the bet from.

        Returns:
            Bet: The bet created from the dictionary.
        """
        return cls(
            bet_dict["bet_type"],
            bet_dict["value"],
            bet_dict["odds"],
            Bookmaker.from_dict(bet_dict["bookmaker"]),
            bet_dict["lay"],
            bet_dict["volume"],
            bet_dict["previous_wager"]
        )
