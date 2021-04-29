import threading
import berserk
from models import GameState, ChatLine, GameFull

class Game(threading.Thread):
    def __init__(self, client, game_id, bot, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.bot = bot
        self.client = client
        self.bot_id = client.account.get()['id']

        self.stream = client.bots.stream_game_state(game_id)
        self.full_state = GameFull(next(self.stream)) # Gets all game data from lichess API (GameFull object)
        self.playing_as = "white" if self.full_state.white_id == self.bot_id else "black"

        print("Playing as:", self.playing_as)

        gameState = self.full_state.gameState
        if self.bots_turn(gameState):
            print("So I should move")
            self.handle_move(gameState)

    def run(self):
        print("Okay I'm starting!")
        while True:
            for event in self.stream:
                print("I got a game event: ", event)
                if event['type'] == 'gameState':
                    gameState = GameState(event)
                    if gameState.is_finished:
                        print("Game #{} has finished!".format(self.game_id))
                        return
                    self.handle_move(gameState)
                elif event['type'] == 'chatLine':
                    chatline = ChatLine(event)
                    response = self.bot.getResponseToMessage(chatline)
                    if response:
                        self.client.bots.post_message(self.game_id, response)

        
    def handle_move(self, gameState):
        if not self.bots_turn(gameState):
            # Not our move so we can ignore
            return
        bestMove = self.bot.getBestMove(gameState)
        print("Making move:", bestMove)
        self.client.bots.make_move(self.game_id, bestMove)

    def bots_turn(self, gameState):
        pairity = 0 if self.playing_as == "white" else 1
        print("pair", pairity)
        print("mivoes", gameState.num_moves)
        return gameState.num_moves % 2 == pairity
            
        