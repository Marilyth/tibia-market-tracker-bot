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
 
# Contributing
1. **Fork the Repository**
   - Go [here](https://github.com/Marilyth/tibia-market-tracker-bot/fork) to create your own copy of the repository
2. **Clone your fork**
   - Clone your forked repository to your local machine using
     ```sh
     git clone https://github.com/YOUR-USERNAME/tibia-market-tracker-bot.git
     ```
3. **Create a new branch**
   - Before making any changes, create a new branch
     ```sh
     git checkout -b my-feature-branch
     ```
4. **Make your changes**
   - Implement your changes and push them
     ```sh
     git add .
     git commit -m "Description of my changes"
     git push origin my-feature-branch
     ```
5. **Create a Pull Request**
   - Go [here](https://github.com/Marilyth/tibia-market-tracker-bot/compare) and select your feature branch
   - Provide a description of your changes and submit the pull request
