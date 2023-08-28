import unittest

import betting_event.betting_event as b_event


class TestEvent(unittest.TestCase):
    def test_build(self):
        betfair = b_event.Bookmaker(commission=0.05)
        coral = b_event.Bookmaker()

        new_event = b_event.Event()

        over_under_bets = [
            b_event.Bet(bet_type=b_event.BetType.Goals_OverUnder, value="over 2.5", odds=1.5, bookmaker=betfair, lay=False),
            b_event.Bet(bet_type=b_event.BetType.Goals_OverUnder, value="under 2.5", odds=2.5, bookmaker=coral, lay=False),
        ]

        for bet in over_under_bets:
            new_event.add_bet(bet)
        
        self.assertEqual(len(new_event.bookmakers), 2)
        self.assertEqual(len(new_event.bets), 2)
        self.assertIs(new_event.bets[0].bookmaker, new_event.bookmakers[0])

        return new_event
