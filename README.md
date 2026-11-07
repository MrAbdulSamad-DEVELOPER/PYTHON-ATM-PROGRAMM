# PYTHON-ATM-PROGRAMM

A simple ATM simulator written in Python.

## Features

- PIN authentication (default PIN: `1234`)
- Check balance
- Deposit and withdraw money
- Transaction history
- Balance saved to a JSON file so it persists between runs

## Run it

```bash
python atm.py
```

## Run the tests

```bash
python -m unittest test_atm.py -v
```

## Project structure

- `atm.py` — the ATM class and the command-line menu
- `test_atm.py` — unit tests (9 tests)
- `balance.json` — created automatically to store the balance
