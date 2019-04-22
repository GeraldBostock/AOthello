import pygame

import colors

from board import Board

import threading

class Game:
    def __init__(self, screen_width, screen_height):
            pygame.init()
            pygame.font.init()
            pygame.display.set_caption('AOthello')

            self.screen = pygame.display.set_mode((screen_width, screen_height))
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.board_offset = 20

            self.board = Board(8, 8, self.board_offset, self.screen_width - self.board_offset * 2, self.screen_height - self.board_offset * 2)

            # Index 0 is black player, 1 is white player
            self.players = [None] * 2
            self.current_player_index = 0

            self.player_currently_playing = False
            self.board.calculate_viable_positions_for_player('black')

            self.font = pygame.font.Font(None, 20)

    def run(self):
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            
            self.screen.fill(colors.WHITE)

            if not self.player_currently_playing:
                self.player_currently_playing = True
                thread = threading.Thread(target=self.players[self.current_player_index].run, args=(self.board,))
                thread.start()

            self.board.render_board(self.screen, (self.board_offset, self.board_offset))

            textsurface = self.font.render('Turn: ' + str(self.get_player_color()), False, (0, 0, 0))
            self.screen.blit(textsurface,(5, 5))

            pygame.display.flip()

    def move_played_callback(self, move):
        if self.board.is_move_viable(move):
            player_color = self.get_player_color()
            self.board.make_move(player_color, move)
            self.current_player_index += 1
            self.current_player_index %= 2
            player_color = self.get_player_color()
            self.board.calculate_viable_positions_for_player(player_color)
            self.player_currently_playing = False

    def get_player_color(self):
        if self.current_player_index == 0:
            return 'black'
        else:
            return 'white'

    def set_black_player(self, player):
        self.players[0] = player
        self.players[0].set_parent(self)

    def set_white_player(self, player):
        self.players[1] = player
        self.players[1].set_parent(self)
