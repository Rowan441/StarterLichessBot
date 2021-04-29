import chess
import random

class ChessBotInterface():

    def getBestMove(self, gameState):
        '''
        return the best move for a given position as a UCI formatted string (e.g "e2e4")
        params:
            gameState (Type: models.GameState) - The current state of the game
        '''
        raise NotImplementedError

    def getResponseToMessage(self, chatLine):
        '''
        Return the response to a message as a string or None for no response
        params:
            chatline (Type: models.ChatLine) - The incoming message to respond to
        '''
        return None


class RandomMoveBot(ChessBotInterface):

    def getBestMove(self, gameState):

        board = chess.Board()

        for move in gameState.move_list:
            board.push_uci(move)

        return random.choice(list(board.legal_moves)).uci()
