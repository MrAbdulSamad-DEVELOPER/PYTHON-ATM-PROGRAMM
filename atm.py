"""Simple ATM simulator.

Features:
- PIN authentication (default PIN 1234)
- Check balance, deposit, withdraw
- Transaction history
- Persistent balance saved to a JSON file
"""

import json
import os

DEFAULT_PIN = "1234"
BALANCE_FILE = "balance.json"


class ATM:
    def __init__(self, pin=DEFAULT_PIN, balance_file=BALANCE_FILE):
        self._pin = pin
        self.balance_file = balance_file
        self.balance = self._load_balance()
        self.history = []

    def _load_balance(self):
        if os.path.exists(self.balance_file):
            with open(self.balance_file) as f:
                data = json.load(f)
                return data.get("balance", 0)
        return 0

    def _save_balance(self):
        with open(self.balance_file, "w") as f:
            json.dump({"balance": self.balance}, f)

    def authenticate(self, pin):
        return pin == self._pin

    def check_balance(self):
        return self.balance

    def deposit(self, amount):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Amount must be a number.")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.history.append(f"Deposited {amount}")
        self._save_balance()
        return self.balance

    def withdraw(self, amount):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Amount must be a number.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.history.append(f"Withdrew {amount}")
        self._save_balance()
        return self.balance

    def get_history(self):
        return list(self.history)


def main():
    atm = ATM()
    pin = input("Enter your PIN: ")
    if not atm.authenticate(pin):
        print("Wrong PIN. Access denied.")
        return
    print("Welcome!")
    while True:
        print("\n1. Check Balance  2. Deposit  3. Withdraw  4. History  5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            print(f"Balance: {atm.check_balance()}")
        elif choice == "2":
            try:
                amount = float(input("Deposit amount: "))
                print(f"New balance: {atm.deposit(amount)}")
            except (ValueError, TypeError) as e:
                print(f"Error: {e}")
        elif choice == "3":
            try:
                amount = float(input("Withdraw amount: "))
                print(f"New balance: {atm.withdraw(amount)}")
            except (ValueError, TypeError) as e:
                print(f"Error: {e}")
        elif choice == "4":
            for entry in atm.get_history():
                print(entry)
            if not atm.get_history():
                print("No transactions yet.")
        elif choice == "5":
            print("Thank you. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
