from player import IPlayer

class AIPlayer(IPlayer):
    def get_move(self, board):
        if board.is_move_viable((3, 2)):
            return (3, 2)