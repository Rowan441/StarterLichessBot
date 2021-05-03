
<h1 align="center">Starter Lichess Bot </h3>

<p align="center"> 🤖 A Customizable Python Chess Bot
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Try it out](#try)
- [Getting Started](#getting_started)
- [Building Your Own Bot](#build_your_own)
- [Built Using](#built_using)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

This is a simple python script that listens to the Event stream for a Lichess.org BOT account and accepts/rejects challenges, plays games using fully customizable engine, responds to users in the game's chat.

There is already a sample chessbot implementation RandomMoveBot() which randomly plays a legal move.

This project was made using [berserk-downstream](https://github.com/ZackClements/berserk). A client library for the [Lichess API](https://lichess.org/api)

## 🎈 Try it out <a name = "try"></a>

Check out my [BOT account](https://lichess.org/@/WeirdChessBot) you can play against here.

## 🏁 Getting Started <a name = "getting_started"></a>

### Prerequisite 

Make sure you have a Lichess account that you have [upgraded to a BOT account](https://lichess.org/api#operation/botAccountUpgrade) and [created a PAT](https://lichess.org/account/oauth/token) for your account

First clone the repository:

```
git clone https://github.com/Rowan441/WeirdChessBot.git
```

Then install virtualenv:
```
pip install virtualenv
```

cd into the project directory and create a virtual environment:
```
virtualenv .venv
```

And install the required libraries:
```
pip install -r requirements.txt
```

**Important**: then you need to create a file named `api.token` in the home directory of the project add your BOT account's [Personal API token](https://lichess.org/account/oauth/token) to the file

```
echo YOURAPITOKEN > api.token
```

## 🔨 Build Your Own Bot <a name = "build_your_own"></a>

You can create your own Bots. In this program, a Bot is defined as a class that implements: `getBestMove(self, gameState, variant)` and `getResponseToMessage(self, chatLine)` methods

Checkout the `ChessBotInterface()` class in the `chessbots.py` file which you can create subclasses from and override its methods with your own funcitonality.

Once you have a working bot you can tell the program to use it by:
1. Importing the bot in `lichess-bot-manager.py`:
```
 6|  from chessbots import MyBotClass # Import your bot
```
2. instantiating the bot on line 17 of `lichess-bot-manager.py`
```
17|  bot = MyBotClass()
```
In the source code this has already been done with `RandomChessBot`, so just replace `RandomChessBot` with your bot class.

## ⛏️ Built Using <a name = "built_using"></a>

- Python
- [berserk-downstream](https://github.com/ZackClements/berserk) - Lichess Client Library 
- [python-chess](https://python-chess.readthedocs.io/en/latest/) - Python Chess Library

## ✍️ Authors <a name = "authors"></a>

- [@Rowan441](https://github.com/Rowan441)
