import unittest

from ..betting_event import bet as bet_module


class TestBet(unittest.TestCase):
    def test_init(self):
        bet = bet_module.Bet(0, "home", 2.5)
        self.assertEqual(bet.wager_limit, bet_module.Bet.Defaults['wager_limit'])
        self.assertEqual(bet.wager_precision, bet_module.Bet.Defaults['wager_precision'])
        self.assertEqual(bet.profit, bet_module.Bet.Defaults['profit'])
        self.assertEqual(bet.bookmaker, bet_module.Bet.DefaultBookmaker)
        self.assertEqual(bet.lay, bet_module.Bet.Defaults['lay'])
        self.assertEqual(bet._id, 0)


if __name__ == "__main__":
    unittest.main()