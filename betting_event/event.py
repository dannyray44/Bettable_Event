import inspect
import itertools
import typing
import json
from .metadata import BetType

__child_values_dict: typing.Dict[typing.Type['__Processable'], typing.Tuple[itertools.count, typing.Mapping[str, inspect.Parameter]]] = {}

class __Processable:
    """A base class for objects that can be converted to and from dictionaries and json."""
    _required_attributes: typing.Optional[typing.List[str]] = None
    _nested_list: typing.Optional[typing.Tuple[str, typing.Type['__Processable']]] = None

    def __init__(self) -> None:
        cls: typing.Type[__Processable] = type(self)
        if cls not in __child_values_dict:
            __child_values_dict[cls] = (
                itertools.count(),
                inspect.signature(cls).parameters
                )
        if not hasattr(self, '__id'):
            self.__id = next(__child_values_dict[cls][0])

    def as_dict(self) -> typing.Dict[str, typing.Any]:
        """Returns a dictionary representation of the object, with the exception of the (privte) __id attribute
        """
        result = {}
        if self._required_attributes:
            for attribute in self._required_attributes:
                parameter = __child_values_dict[type(self)][1].get(attribute)
                if not parameter:
                    raise RuntimeError(f'Attribute {attribute} not found in {type(self)}')
                current_val = getattr(self, attribute)
                if current_val != parameter.default:
                    result[attribute] = current_val

        if self._nested_list:
            current_attr: typing.List[__Processable] = getattr(self, self._nested_list[0], [])
            # TODO: error catching
            result[self._nested_list[0]] = [val.as_dict() for val in current_attr]

        result['__id'] = self.__id
        return result

    def as_json(self, indent: typing.Optional[int] = None) -> str:
        """Returns a json representation of the object, with the exception of the (privte) __id attribute.
        
        Args:
            indent: If not None, the json will be indented by this amount.

        Returns:
            str: A json representation of the object.
        """
        return json.dumps(self.as_dict(), indent= indent)

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> '__Processable':
        """Creates an instance of the class from a dictionary representation of the object.
        
        Args:
            data: A dictionary representation of the object.
            
        Returns:
            __Processable: An instance of the class.
        """
        kwargs = {}
        if cls._required_attributes:
            for attribute in cls._required_attributes:
                if attribute in data:
                    kwargs[attribute] = data[attribute]

        if cls._nested_list:
            kwargs[cls._nested_list[0]] = [cls._nested_list[1].from_dict(val) for val in data[cls._nested_list[0]]]

        if not '__id' in data:
            return cls(**kwargs)
    
        result = cls(**kwargs)
        result.__id = data['__id']
        return result

    @classmethod
    def from_json(cls, json_str: str) -> '__Processable':
        """Creates an instance of the class from a json representation of the object.
        
        Args:
            json_str: A json representation of the object.
            
        Returns:
            __Processable: An instance of the class.
        """
        return cls.from_dict(json.loads(json_str))

    def update_from_dict(self, data: typing.Dict[str, typing.Any]) -> None:
        """Updates the object from a dictionary representation of the object. Any attributes not in 
        the dictionary will be left unchanged. Any nested lists will have there corosponding
        objects updated according to their __id attribute.
        
        Args:
            data: A dictionary representation of the object.
        """
        if self._nested_list and self._nested_list[0] in data:
            nested_data: typing.List[dict] = data.pop(self._nested_list[0])
            nested_attribute_list: typing.List[__Processable] = getattr(self, self._nested_list[0])
            for nested_dict in nested_data:
                for nested_attribute in nested_attribute_list:
                    if nested_attribute.__id == nested_dict['__id']:
                        nested_attribute.update_from_dict(nested_dict)
                        break
                else:
                    nested_attribute_list.append(self.from_dict(nested_dict))

        for key in data.keys():
            if key == '__id': 
                continue
            setattr(self, key, data[key])

    def update_from_json(self, json_str: str) -> None:
        """Updates the object from a json representation of the object. Any attributes not in
        the json will be left unchanged. Any nested lists will have there corosponding
        objects updated according to their __id attribute.
        
        Args:
            json_str: A json representation of the object.
        """
        self.update_from_dict(json.loads(json_str))


class BetValue(__Processable):
    _required_attributes = ['value', 'odds', 'lay', 'volume', 'previous_wager']

    def __init__(self, value: str, odds: float, lay: bool, volume: float = -1.0, previous_wager: float = 0.0, wager: float = 0.0) -> None:
        self.value: str = value
        self.odds: float = odds
        self.lay: bool = lay
        self.volume: float = volume
        self.previous_wager: float = previous_wager
        self.wager: float = wager
        super().__init__()


class Bet(__Processable):
    _required_attributes = ['id']
    _nested_list = 'values', BetValue

    def __init__(self, id: BetType, values: typing.Optional[typing.List[BetValue]] = None) -> None:
        self.id = id
        if values is None:
            values = []
        self.values = values
        super().__init__()

    def as_dict(self) -> typing.Dict[str, typing.Any]:
        result = super().as_dict()
        result['id'] = result['id'].value
        return result
    
    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> '__Processable':
        data['id'] = BetType(data['id'])
        return super().from_dict(data)


class Bookmaker(__Processable):
    _required_attributes = ['commission', 'wager_limit', 'wager_count']
    _nested_list = 'bets', Bet

    def __init__(self, commission: float = 0.0, wager_limit: float = -1.0, wager_count: int = 0, bets: typing.Optional[typing.List[Bet]] = None) -> None:
        self.commission = commission
        self.wager_limit = wager_limit
        self.wager_count = wager_count
        # self.wager_count_limit = -1
        if bets is None:
            bets = []
        self.bets = bets

        super().__init__()


class Event(__Processable):
    _required_attributes = ['total_bet_size', 'profit', 'wager_count']
    _nested_list = 'bookmakers', Bookmaker

    def __init__(self, total_bet_size: float = -1.0, profit: float = -1.0, wager_count: int = -1, bookmakers: typing.Optional[typing.List[Bookmaker]] = None) -> None:
        self.total_bet_size = total_bet_size
        self.profit = profit
        self.wager_count = wager_count
        if bookmakers is None:
            bookmakers = []
        self.bookmakers = bookmakers
        super().__init__()


range(,)