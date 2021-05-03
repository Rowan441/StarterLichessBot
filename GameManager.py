import json
import berserk

from Game import Game
from ChessBots import RandomMoveBot # Import your bot

import argparse
import logging

def main(token):
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
    '''
    Determine if a challenge should be accepted or declined from the challenge 'event'
    '''
    return event['challenge']['rated'] == False



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play on Lichess with your bot')
    parser.add_argument('-l', '--logfile', help="Log file to append logs to.", default=None)
    args = parser.parse_args()
    
    logging.basicConfig(filename=args.logfile, 
                        filemode='w', 
                        level=logging.INFO, 
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', 
                        datefmt='%m-%d %H:%M',)

    # Read token
    with open('./api.token') as f:
        token = f.read()

    main(token)
