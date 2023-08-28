# Only specifying required parameters

The only base parameters required by the API is `bets`. It must have a minimum of 2 bets in it. The only keys required in each bet are: `bet_type`, `value` and `odds`.

```json
{
    "bets": [
        {
            "bet_type": 1,
            "value": "Home",
            "odds": 3.2
        },
        {
            "bet_type": 1,
            "value": "Home",
            "odds": 3.1,
            "lay": true
        }
    ]
}
```