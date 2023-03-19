from event_alt.event import Event, Bookmaker, Bet, BetValue
from event_alt.metadata import BetType

ev = Event(
        bookmakers=[
            Bookmaker(
                wager_limit=135.50,
                bets=[
                    Bet(
                        BetType.MatchWinner,
                        values=[
                            BetValue('home', 2.4, False),
                            BetValue('away', 2.3, True)
                        ]
                    )
                ]
            )
        ]
    )


json_str = ev.to_json(2)
print(json_str)

