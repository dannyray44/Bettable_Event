

from betting_event_new import Event, Bet, BetType

ev = Event()

ev.add_bet(Bet(1, '1', 1.1, False))
ev.add_bet(Bet(1, '1', 1.1, False))
ev.add_bet(Bet(1, '1', 1.1, True))

Bet(BetType.MatchWinner, 'home', 1.1, False)

print(ev.bets)