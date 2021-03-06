import player
import time
import pygame

class HumanPlayer(player.IPlayer):

    def make_move(self, board, viable_moves):

        while not self.done:
            pos = pygame.mouse.get_pos()
            pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
            if pressed1:
                cell_index = board.get_cell_index_from_position(pos)

                if cell_index and board.is_move_viable(cell_index):
                    return cell_index
                
        return False