from game import Game
from human_player import HumanPlayer
from ai_player import AIPlayer

def main():
        game = Game(600, 600)
        game.set_black_player(HumanPlayer())
        game.set_white_player(AIPlayer())
        game.run()

if __name__ == "__main__":
    main()