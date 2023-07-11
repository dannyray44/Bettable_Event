import itertools
import typing

BOOKMAKER_T = typing.TypeVar('BOOKMAKER_T', bound='Bookmaker')

class Bookmaker:
    """"""
    __ID_COUNTER = itertools.count()

    def __init__(self, commission: float = 0.0, wager_limit: float = -1.0, ignore_wager_precision: bool = False, max_wager_count: int = -1) -> None:
        """
        Args:
            commission (float): The commission the bookmaker takes (e.g. 5% = 0.05). Defaults to 0.0.
            wager_limit (float): The maximum sum of all wagers with this bookmaker, usually set to balance at bookmaker. Defaults to -1.0 (no limit).
            ignore_wager_precision (bool): If True, Event.wager_precision will be ignored for wagers with this bookmaker. Defaults to False.
            max_wager_count (int): The maximum number of wagers with this bookmaker. Defaults to -1 (no limit).
        """
        self.commission = commission
        self.wager_limit = wager_limit
        self.ignore_wager_precision = ignore_wager_precision
        self.max_wager_count = max_wager_count

        self._id = next(self.__ID_COUNTER)

    def as_dict(self) -> typing.Dict[str, typing.Union[float, int, bool]]:
        """Returns the bookmaker as a dictionary.

        Returns:
            dict: The bookmaker as a dictionary.
        """
        return {
            "commission": self.commission,
            "wager_limit": self.wager_limit,
            "ignore_wager_precision": self.ignore_wager_precision,
            "max_wager_count": self.max_wager_count,
            "id": self._id
        }

    @classmethod
    def from_dict(cls: typing.Type[BOOKMAKER_T], __bookmaker_dict: dict) -> BOOKMAKER_T:
        """Creates a bookmaker from a dictionary.

            Args:
                __bookmaker_dict (dict): The dictionary to create the bookmaker from.
        
            Returns:
                Bookmaker: The bookmaker created from the dictionary.
        """
        bookmaker = cls(__bookmaker_dict["commission"], __bookmaker_dict["wager_limit"], __bookmaker_dict["ignore_wager_precision"], __bookmaker_dict["max_wager_count"])
        bookmaker._id = __bookmaker_dict["id"]  # override the generated id
        return bookmaker

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Bookmaker):
            raise NotImplementedError
        return self._id == __value._id
