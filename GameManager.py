import berserk
# from berserk.clients import Bots
import json
from Game import Game
from ChessBot import RandomMoveBot
import logging

def main():
    with open('./api.token') as f:
        token = f.read()

    session = berserk.TokenSession(token)
    client = berserk.Client(session)

    # Apply fixed Bots client
    client.bots = fixBots(session)

    bot = RandomMoveBot()

    logging.info("Starting WeirdChessBot...")

    while True:
        for event in client.bots.stream_incoming_events():
            if event['type'] == 'challenge':
                challengeData = event['challenge']
                if should_accept(event):
                    logging.info("Accepting Challenge from {}".format(challengeData['challenger']['name']))
                    client.bots.accept_challenge(challengeData['id'])
                else:
                    logging.info("Declining Challenge from {}".format(challengeData['challenger']['name']))
                    client.bots.decline_challenge(challengeData['id'], reason='rated')
            elif event['type'] == 'gameStart':
                gameData = event['game']
                game = Game(client, gameData['id'], bot)
                logging.info("Starting game ID:{}".format(gameData['id']))
                game.run()

def should_accept(event):
    return event['challenge']['rated'] == False

# Override Beserks's Bots client because it's api doesn't support provding a reason for declining a challenge
class fixBots(berserk.clients.Bots):
    def decline_challenge(self, challenge_id, reason='generic'):
        """Decline an incoming challenge.
        :param str challenge_id: ID of a challenge
        :return: success
        :rtype: bool
        """
        path = f'api/challenge/{challenge_id}/decline'
        payload = {
            'reason': reason
        }
        return self._r.post(path, json=payload)['ok']


logging.getLogger().setLevel(logging.INFO)

main()
