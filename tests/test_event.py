import unittest

import betting_event as b_event


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

    def test_from_dict_full(self):
        event = b_event.Event.from_dict({
            "wager_limit": 1000,
            "wager_precision": 5,
            "profit": 101.5,
            "bookmakers": [
                {
                    "commission": 0.05,
                    "wager_limit": 1000,
                    "ignore_wager_precision": True,
                    "max_wager_count": 100,
                    "id": 0
                },
                {
                    "commission": 0.05,
                    "wager_limit": 1000,
                    "ignore_wager_precision": True,
                    "max_wager_count": 100,
                    "id": 1
                }
            ],
            "bets": [
                {
                    "bet_type": 3,
                    "value": "over 2.5",
                    "odds": 1.5,
                    "bookmaker": 0,
                    "lay": False
                },
                {
                    "bet_type": 3,
                    "value": "under 2.5",
                    "odds": 2.5,
                    "bookmaker": 1,
                    "lay": False
                }
            ]
        })

        self.assertEqual(event.wager_limit, 1000)
        self.assertEqual(event.wager_precision, 5)
        self.assertEqual(event.profit, 101.5)
        self.assertEqual(len(event.bookmakers), 2)
        self.assertEqual(len(event.bets), 2)
        self.assertIs(event.bets[0].bookmaker, event.bookmakers[0])

    def test_from_dict_partial(self):
        event = b_event.Event.from_dict({
            "bets": [
                {
                    "bet_type": 3,
                    "value": "over 2.5",
                    "odds": 1.5
                },
                {
                    "bet_type": 3,
                    "value": "under 2.5",
                    "odds": 2.5
                }
            ]
        })
        self.assertEqual(len(event.bookmakers), 1)
        self.assertEqual(len(event.bets), 2)
        self.assertIs(event.bets[0].bookmaker, event.bookmakers[0])
        self.assertIs(event.bets[1].bookmaker, event.bookmakers[0])

    def test_as_dict_partial(self):
        event = b_event.Event()
        event.add_bet(b_event.Bet(bet_type=b_event.BetType.Goals_OverUnder, value="over 2.5", odds=1.5))
        event.add_bet(b_event.Bet(bet_type=b_event.BetType.Goals_OverUnder, value="under 2.5", odds=2.5))
        self.assertEqual(event.as_dict(), {
            "bets": [
                {
                    "bet_type": 3,
                    "value": "over 2.5",
                    "odds": 1.5
                },{
                    "bet_type": 3,
                    "value": "under 2.5",
                    "odds": 2.5
                }
            ],
            "bookmakers": [{'id': 0}]
        })
