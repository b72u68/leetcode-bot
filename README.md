# YeetCode-Bot

![YeetCode](https://github.com/b72u68/leetcode-bot/blob/master/yeetcode.png)

Yeet away from the unemployment with Leetcode problems in your Discord channel.

> "A LeetCode a day keeps the unemployment away"

## Instructions

- Python 3 is required for the bot to run
- Required Python libraries: requests, bs4, selenium. Run `pip install -r requirements.txt` to install these libraries
- Create Discord Bot on Discord Developer Portal and add token in `discord.ini` in `.config` directory

## Usage

- Run the bot LOCALLY. Simply run `python3 bot.py`
- Bot Commands
  - `!help` or `!`: Get command menu
  - `!yeet <difficulty>`: Send problem in difficulty level
  - `!md <problemID>`: Mark problem as done/completed
  - `!sl <problemTitleSlug> <language>`: Send solution

## TODO

- [ ] Add search feature for the bot (for learning Data Structures and Algorithms)
- [x] Add get solution feature
