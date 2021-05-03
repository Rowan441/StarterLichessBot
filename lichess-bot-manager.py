import json
import berserk
from berserk.exceptions import ResponseError

from game import Game
from chessbots import RandomMoveBot # Import your bot

import argparse
import logging
import time

def main(token):
    session = berserk.TokenSession(token)
    client = berserk.Client(session)

    #  Instantiate the bot of choice
    bot = RandomMoveBot()

    logging.info("Starting 'Starter Lichess Bot'...")

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
        except ResponseError as error:
            if error.status_code == 401:
                logging.critical("AUTHOIRZATION ERROR: check your API Token's scope's. Token must have bot:play and challenge:write scopes.")
                logging.critical("Quiting program due authorization error.")
                exit()
            if error.status_code == 429:
                logging.warn("RATE LIMIT ERROR: waiting 60 seconds before querying lichess again to avoid rate limiting")
                time.sleep(60)
            else:
                logging.exception("{} ERROR: while handling event stream".format(error.status_code))

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
    try:
        with open('./api.token') as f:
            token = f.read()
    except FileNotFoundError:
        print("Could not find api.token file, make sure you have an api.token file containing your lichess account's API token")
        exit()

    main(token)
