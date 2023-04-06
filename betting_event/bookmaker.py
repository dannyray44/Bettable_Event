import itertools


class Bookmaker:
    __ID_COUNTER = itertools.count()

    def __init__(self, commision: float = 0.0, wager_limit: float = -1.0) -> None:
        self.commision = commision
        self.wager_limit = wager_limit

        self.__id = next(self.__ID_COUNTER)

    def as_dict(self) -> dict:
        """Returns the bookmaker as a dictionary.
        
        Returns:
            dict: The bookmaker as a dictionary."""
        return {
            "commision": self.commision,
            "wager_limit": self.wager_limit,
            "id": self.__id
        }

    @classmethod
    def from_dict(cls, __bookmaker_dict: dict) -> 'Bookmaker':
        """Creates a bookmaker from a dictionary.
        
            Args:
                __bookmaker_dict (dict): The dictionary to create the bookmaker from.
        
            Returns:
                Bookmaker: The bookmaker created from the dictionary.
        """
        bookmaker = cls(__bookmaker_dict["commision"], __bookmaker_dict["wager_limit"])
        bookmaker.__id = __bookmaker_dict["id"]
        return bookmaker

    def __eq__(self, __value: 'Bookmaker') -> bool:
        return self.__id == __value.__id
