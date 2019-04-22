from game import Game
from human_player import HumanPlayer

def main():
        game = Game(600, 600)
        game.set_black_player(HumanPlayer())
        game.set_white_player(HumanPlayer())
        game.run()

if __name__ == "__main__":
    main()