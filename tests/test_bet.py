import unittest

from betting_event.bet import Bet, BetType, ValueCheck


class TestBet(unittest.TestCase):
    def test_init(self):
        bet = Bet(BetType.MatchWinner, "home", 2.5)
        self.assertEqual(bet.bet_type, BetType.MatchWinner)
        self.assertEqual(bet.value, "home")
        self.assertEqual(bet.odds, 2.5)
        self.assertEqual(bet.bookmaker, Bet.DefaultBookmaker)
        self.assertEqual(bet.lay, Bet.Defaults['lay'])
        self.assertEqual(bet.volume, Bet.Defaults['volume'])
        self.assertEqual(bet.wager, Bet.Defaults['wager'])

    def test_from_dict_full(self):
        bet = Bet.from_dict({
            "bet_type": 1,
            "value": "home",
            "odds": 2.5,
            "lay": False,
            "volume": 10,
            "wager": 10
        })
        self.assertEqual(bet.bet_type, BetType.MatchWinner)
        self.assertEqual(bet.value, "home")
        self.assertEqual(bet.odds, 2.5)
        self.assertEqual(bet.bookmaker, Bet.DefaultBookmaker)
        self.assertEqual(bet.lay, False)
        self.assertEqual(bet.volume, 10)
        self.assertEqual(bet.wager, 10)

    def test_from_dict_partial(self):
        bet = Bet.from_dict({
            "bet_type": 1,
            "value": "home",
            "odds": 2.5,
        })
        self.assertEqual(bet.bet_type, BetType.MatchWinner)
        self.assertEqual(bet.value, "home")
        self.assertEqual(bet.odds, 2.5)
        self.assertEqual(bet.bookmaker, Bet.DefaultBookmaker)
        self.assertEqual(bet.lay, Bet.Defaults['lay'])
        self.assertEqual(bet.volume, Bet.Defaults['volume'])
        self.assertEqual(bet.wager, Bet.Defaults['wager'])

    def test_as_dict_partial(self):
        bet = Bet(BetType.MatchWinner, "home", 2.5)
        self.assertEqual(bet.as_dict(), {
            "bet_type": "MatchWinner",
            "value": "home",
            "odds": 2.5
        })

    def test_as_dict_full(self):
        bet = Bet(BetType.MatchWinner, "home", 2.5, lay=True, volume=10, wager=10)
        self.assertEqual(bet.as_dict(), {
            "bet_type": "MatchWinner",
            "value": "home",
            "odds": 2.5,
            "lay": True,
            "volume": 10,
            "wager": 10
        })

    def test_regex_len(self):
        self.assertEqual(len(ValueCheck), len(BetType))
