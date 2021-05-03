import chess
import chess.variant
import random

class ChessBotInterface():

    def getBestMove(self, gameState, variant):
        '''
        return the best move for a given position using the 'variant' ruleset
        as a UCI formatted string (e.g "e2e4")
        params:
            gameState (Type: models.GameState) - The current state of the game
            variant - a string representing one of the following variants
                    "standard", "chess960", "crazyhouse", "antichess", "atomic"
                    "horde", "kingOfTheHill", "racingKings", "threeCheck"
        '''
        raise NotImplementedError

    def getResponseToMessage(self, chatLine):
        '''
        Return the response to a message as a string or None for no response
        params:
            chatline (Type: models.ChatLine) - The incoming message to respond to
        '''
        return None

    @staticmethod
    def getBoardObject(variant):
        '''
        Helper function that returns the proper python-chess Board object for the given variant
        '''
        if variant == "chess960":
            return chess.Board(chess960=True)

        possibleBoards = {
            "standard": chess.Board,
            "crazyhouse": chess.variant.CrazyhouseBoard,
            "antichess": chess.variant.AntichessBoard,
            "atomic": chess.variant.AtomicBoard,
            "horde": chess.variant.HordeBoard,
            "kingOfTheHill": chess.variant.KingOfTheHillBoard,
            "racingKings": chess.variant.RacingKingsBoard,
            "threeCheck": chess.variant.ThreeCheckBoard
        }

        return possibleBoards[variant]()


class RandomMoveBot(ChessBotInterface):

    def getBestMove(self, gameState, variant):
        '''
        Picks a random legal move and plays it
        '''
        board = self.getBoardObject(variant)

        for move in gameState.move_list:
            board.push_uci(move)

        return random.choice(list(board.legal_moves)).uci()
