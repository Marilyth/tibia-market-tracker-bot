# tibia-market-tracker-bot
A discord bot for the tibia market tracker API

# Set-up
1. Optionally, create a virtual environment using `python -m venv venv`
2. Install all required packages using `python -m pip install -r requirements.txt`
  - Or use `pip` directly if available
3. Copy & paste the `example_config.json` inside the `config/` folder and rename it to `config.json`
4. Fill out the `config.json` with your tokens
5. Start the bot by running `python src/main.py`

# Testing
- Code conventions can be tested using `pylint $(git ls-files "*.py")`
  - Go through all things it complain about to keep your code clean
- Unit tests can be executed using `pytest`
  - If any test fails, resolve it
