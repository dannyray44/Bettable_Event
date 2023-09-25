import unittest

from betting_event.bookmaker import Bookmaker, DEFAULTS


class TestBookmaker(unittest.TestCase):
    def test_init_defaults(self):
        bookmaker = Bookmaker()
        self.assertEqual(bookmaker.commission, DEFAULTS['commission'])
        self.assertEqual(bookmaker.wager_limit, DEFAULTS['wager_limit'])
        self.assertEqual(bookmaker.ignore_wager_precision, DEFAULTS['ignore_wager_precision'])
        self.assertEqual(bookmaker.max_wager_count, DEFAULTS['max_wager_count'])

    def test_init(self):
        bookmaker = Bookmaker(0.05, 1000, True, 100)
        self.assertEqual(bookmaker.commission, 0.05)
        self.assertEqual(bookmaker.wager_limit, 1000)
        self.assertEqual(bookmaker.ignore_wager_precision, True)
        self.assertEqual(bookmaker.max_wager_count, 100)

    def test_from_dict_full(self):
        bookmaker = Bookmaker.from_dict({
            "commission": 0.05,
            "wager_limit": 1000,
            "ignore_wager_precision": True,
            "max_wager_count": 100,
            "id": 0
        })
        self.assertEqual(bookmaker.commission, 0.05)
        self.assertEqual(bookmaker.wager_limit, 1000)
        self.assertEqual(bookmaker.ignore_wager_precision, True)
        self.assertEqual(bookmaker.max_wager_count, 100)

    def test_from_dict_partial(self):
        bookmaker = Bookmaker.from_dict({"id": 5})
        self.assertEqual(bookmaker.commission, DEFAULTS['commission'])
        self.assertEqual(bookmaker.wager_limit, DEFAULTS['wager_limit'])
        self.assertEqual(bookmaker.ignore_wager_precision, DEFAULTS['ignore_wager_precision'])
        self.assertEqual(bookmaker.max_wager_count, DEFAULTS['max_wager_count'])
        self.assertEqual(bookmaker._id, 5)

    def test_as_dict_partial(self):
        bookmaker = Bookmaker()
        self.assertEqual(bookmaker.as_dict(), {"id": 1})      # id: 0 is reserved for the Bet classes DefaultBookmaker
