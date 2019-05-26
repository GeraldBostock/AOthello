from abc import ABCMeta, abstractmethod

class IPlayer():
    __metaclass__ = ABCMeta

    @classmethod
    def __init__(self):
        self.parent = None
        self.done = False

    @classmethod
    def run(self, board, viable_moves):
        move = self.make_move(self, board, viable_moves)
        if self.parent:
            self.parent.move_played_callback(move)

    @classmethod
    def abort(self):
        self.done = True

    @classmethod
    def get_color(self):
        return self.color

    @classmethod
    def set_parent(self, parent):
        self.parent = parent

    @classmethod
    def set_color(self, color):
        self.color = color

    @abstractmethod
    def make_move(self, board, viable_moves): raise NotImplementedError
