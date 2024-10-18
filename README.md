# tibia-market-tracker-bot
A discord bot for interacting with the tibia market tracker API

# Set-up
Depending on your OS, you might need to swap out `python` with `python3`, and `pip` with `pip3` for python3 support.
1. (Optionally) Create a virtual environment using `python -m venv venv` and use it's `pip` and `python` for the following steps
2. Install all required packages using `pip install -r requirements.txt`
3. Start the bot by running `python src/main.py`
   - Enter the tokens it asks for

# Testing
- Code conventions can be tested using `pylint $(git ls-files "*.py")`
  - Go through all things it complain about to keep your code clean
- Unit tests can be executed using `pytest`
  - If any test fails, resolve it
