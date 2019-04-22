from abc import ABCMeta, abstractmethod

class IPlayer():
    __metaclass__ = ABCMeta

    @classmethod
    def __init__(self):
        self.parent = None
        self.board = None

    @classmethod
    def run(self, board):
        move = self.get_move(self, board)
        if self.parent:
            self.parent.move_played_callback(move)

    @classmethod
    def set_parent(self, parent):
        self.parent = parent

    @classmethod
    def set_board(self, board):
        self.board = board

    @abstractmethod
    def get_move(self, board): raise NotImplementedError
