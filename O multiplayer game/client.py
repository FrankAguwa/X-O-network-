import pygame
from network import Network
from game import draw_lines, draw_figures, screen, BOARD_ROWS, BOARD_COLS
import sys
import json

# Initialize Pygame and Network
pygame.init()
n = Network()

# Initialize the game board

board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

player = 'X'  # This should be assigned based on the server's response
game_over = False
draw_lines(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = int(mouseY // 100)
            clicked_col = int(mouseX // 100)

            n.send(f"{clicked_row},{clicked_col}")

        game_state_str = n.receive()
        if game_state_str:
            game_state = json.loads(game_state_str)
            board = game_state['board']
            player = game_state['current_player']
            game_over = game_state['game_over']

            draw_figures(screen, board)

    pygame.display.update()
