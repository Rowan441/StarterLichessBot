import berserk
import json
from Game import Game
from ChessBot import RandomMoveBot # Import your bot
import logging

def main():
    with open('./api.token') as f:
        token = f.read()

    session = berserk.TokenSession(token)
    client = berserk.Client(session)

    #  Instantiate the bot of choice
    bot = RandomMoveBot()

    logging.info("Starting WeirdChessBot...")

    while True:
        try:
            for event in client.bots.stream_incoming_events():
                if event['type'] == 'challenge':
                    challengeData = event['challenge']
                    if should_accept(event):
                        logging.info("Accepting Challenge from {}".format(challengeData['challenger']['name']))
                        client.bots.accept_challenge(challengeData['id'])
                    else:
                        logging.info("Declining Challenge from {}".format(challengeData['challenger']['name']))
                        client.bots.decline_challenge(challengeData['id'], reason=berserk.enums.Reason.CASUAL)
                elif event['type'] == 'gameStart':
                    gameData = event['game']
                    game = Game(client, gameData['id'], bot)
                    logging.info("Starting game ID:{}".format(gameData['id']))
                    game.start()
        except Exception:
            logging.exception("Error handling event stream")

def should_accept(event):

    return event['challenge']['rated'] == False

logging.getLogger().setLevel(logging.INFO)

main()
