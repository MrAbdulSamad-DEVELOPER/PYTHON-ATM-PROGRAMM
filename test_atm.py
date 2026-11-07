"""Tests for the ATM simulator."""

import os
import tempfile
import unittest

from atm import ATM


class TestATM(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp.close()
        os.unlink(self.tmp.name)
        self.atm = ATM(balance_file=self.tmp.name)

    def tearDown(self):
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    def test_authenticate_correct_pin(self):
        self.assertTrue(self.atm.authenticate("1234"))

    def test_authenticate_wrong_pin(self):
        self.assertFalse(self.atm.authenticate("0000"))

    def test_deposit_increases_balance(self):
        self.assertEqual(self.atm.deposit(500), 500)
        self.assertEqual(self.atm.check_balance(), 500)

    def test_withdraw_decreases_balance(self):
        self.atm.deposit(500)
        self.assertEqual(self.atm.withdraw(200), 300)

    def test_withdraw_more_than_balance_fails(self):
        self.atm.deposit(100)
        with self.assertRaises(ValueError):
            self.atm.withdraw(200)

    def test_deposit_negative_fails(self):
        with self.assertRaises(ValueError):
            self.atm.deposit(-50)

    def test_deposit_non_numeric_fails(self):
        with self.assertRaises(TypeError):
            self.atm.deposit("100")

    def test_history_records_transactions(self):
        self.atm.deposit(500)
        self.atm.withdraw(200)
        history = self.atm.get_history()
        self.assertEqual(len(history), 2)
        self.assertIn("Deposited 500", history[0])
        self.assertIn("Withdrew 200", history[1])

    def test_balance_persists_to_file(self):
        self.atm.deposit(700)
        fresh = ATM(balance_file=self.tmp.name)
        self.assertEqual(fresh.check_balance(), 700)


if __name__ == "__main__":
    unittest.main()
