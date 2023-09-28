import itertools
import json
import typing
from os.path import dirname, join

BOOKMAKER_T = typing.TypeVar('BOOKMAKER_T', bound='Bookmaker')

DEFAULTS = json.load(open(join(dirname(__file__), "defaults.json"), "r"))["bookmaker"]

class Bookmaker:
    __ID_COUNTER = itertools.count()

    def __init__(self,
                 commission: float = DEFAULTS['commission'],
                 wager_limit: float = DEFAULTS['wager_limit'],
                 ignore_wager_precision: bool = DEFAULTS['ignore_wager_precision'],
                 max_wager_count: int = DEFAULTS['max_wager_count'],
                 lowest_valid_wager: float = DEFAULTS['lowest_valid_wager']
                 ) -> None:
        """
        Args:
            commission (float): The commission the bookmaker takes (e.g. 5% = 0.05). Defaults to 0.0.
            wager_limit (float): The maximum sum of all wagers with this bookmaker, usually set to balance at bookmaker. Defaults to -1.0 (no limit).
            ignore_wager_precision (bool): If True, Event.wager_precision will be ignored for wagers with this bookmaker. Defaults to False.
            max_wager_count (int): The maximum number of wagers with this bookmaker. Defaults to -1 (no limit).
            lowest_valid_wager (float): The minimum wager size accepted by this bookmaker. Defaults to 0.01.
        """
        self.commission = commission
        self.wager_limit = wager_limit
        self.ignore_wager_precision = ignore_wager_precision
        self.max_wager_count = max_wager_count
        self.lowest_valid_wager = lowest_valid_wager

        self._id = next(self.__ID_COUNTER)

    def as_dict(self) -> typing.Dict[str, typing.Union[float, int, bool]]:
        """Returns the bookmaker as a dictionary.

        Returns:
            dict: The bookmaker as a dictionary.
        """
        result = {}
        for key in DEFAULTS.keys():
            current_value = getattr(self, key)
            if current_value != DEFAULTS[key]:
                result[key] = getattr(self, key)

        return {**result, **{"id": self._id}}

    @classmethod
    def from_dict(cls: typing.Type[BOOKMAKER_T], __bookmaker_dict: dict) -> BOOKMAKER_T:
        """Creates a bookmaker from a dictionary.

            Args:
                __bookmaker_dict (dict): The dictionary to create the bookmaker from.
        
            Returns:
                Bookmaker: The bookmaker created from the dictionary.
        """
        __bookmaker_dict = {**DEFAULTS, **__bookmaker_dict} # Ensure default keys are present
        bookmaker = cls(__bookmaker_dict["commission"], __bookmaker_dict["wager_limit"], __bookmaker_dict["ignore_wager_precision"], __bookmaker_dict["max_wager_count"], __bookmaker_dict["lowest_valid_wager"])
        bookmaker._id = __bookmaker_dict["id"]  # override the generated id
        return bookmaker

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Bookmaker):
            raise NotImplementedError
        return self._id == __value._id
