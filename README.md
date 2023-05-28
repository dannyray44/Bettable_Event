Bettable event handler for WinWise betting calculator.
======================================================
A simple class structure designed to help construct bettable events for the WinWise betting calculator.

# Installation
## Using git
```bash
git clone https://github.com/dannyray44/betting_event.git
cd betting_event
python setup.py install
```
## Using pip
```bash
python3 -m pip install git+https://github.com/dannyray44/betting_event
```

# Data Structure
## Example:
------------
Constructing a simple event with two bookmakers and two bets.
```python
import betting_event

betfair = betting_event.Bookmaker(commission=0.05)
coral = betting_event.Bookmaker()

new_event = betting_event.Event()

over_under_bets = [
    betting_event.Bet(bet_type=betting_event.BetType.Goals_OverUnder, value="over 2.5", odds=1.5, bookmaker=betfair, lay=False),
    betting_event.Bet(bet_type=betting_event.BetType.Goals_OverUnder, value="under 2.5", odds=2.5, bookmaker=coral, lay=False),
]

for bet in over_under_bets:
    new_event.add_bet(bet)

```

Printing the event as a dictionary, this dictionary matches the formatting expected by WinWise API.
```python
# print(new_event.as_dict())
import json                                     # not required. Just for pretty printing
print(json.dumps(new_event.as_dict(), indent=4))

```

```json
{
    "wager_limit": -1.0,
    "bets": [
        {
            "bet_type": 5,          // bet_type is an enum. This is the enum value for 'Goals_OverUnder'
            "value": "over 2.5",
            "odds": 1.5,
            "bookmaker_id": 1,      // bookmaker_id is used to link the bet to a bookmaker in the event.
            "lay": false,
            "volume": -1.0,         // default value for volume is -1.0, meaning no limit to this bets size.
            "previous_wager": 0.0,
            "wager": -1.0
        },
        {
            "bet_type": 5,
            "value": "under 2.5",
            "odds": 2.5,
            "bookmaker_id": 2,
            "lay": false,
            "volume": -1.0,
            "previous_wager": 0.0,
            "wager": -1.0
        }
    ],
    "bookmakers": [
        {
            "commission": 0.05,
            "wager_limit": -1.0,
            "id": 1
        },
        {
            "commission": 0.0,
            "wager_limit": -1.0,
            "id": 2
        }
    ]
}
```

## Structure Overview:
------------
- Each Event contains a list of Bookmakers and a list of Bets.
- Each Bet contains a attribute `bookmaker` which is a reference to the bookmaker that the bet is placed with.

```json
"event": {
    "wager_limit": "float: Maximum total wager for the event",

    "bookmakers": [
        {
            "commission": "float: Commission rate for this bookmaker. e.g. 5% = 0.05",
            "wager_limit": "float: Maximum wager at this bookmaker"
        },
        {...},
        ...
    ],

    "bets": [
        {
            "bet_type": "Enum (BetType): The general type of bet. e.g. 'over_under'",
            "value": "string: Describes specifics of the bet. e.g. 'over 2.5'",
            "odds": "float: The odds of the bet. e.g. 1.5",
            "bookmaker": "Bookmaker: Act as a link to a bookmaker in the event.",
            "lay": "bool: Is this a lay bet. e.g. False",   //
            "volume": "float: The volume available for this bet. aka maximum wager."
        },
        {...},
        ...
    ]
}
```