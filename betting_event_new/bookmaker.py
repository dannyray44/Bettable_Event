import itertools


class Bookmaker:

    __ID_COUNTER = itertools.count()

    def __init__(self, commision: float = 0.0, wager_limit: float = -1.0) -> None:
        self.commision = commision
        self.wager_limit = wager_limit

        self.__id = next(self.__ID_COUNTER)

