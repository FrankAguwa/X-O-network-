import socket
from _thread import *
import sys
import json

server = "10.140.124.28"  # Replace with your server IP
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

# Game board and state
board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'X'
game_over = False

def mark_square(board, row, col, player):
    board[row][col] = player

def available_square(board, row, col):
    return board[row][col] == ''

def is_board_full(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                return False
    return True

def check_win(board, player):
    # Vertical win check
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    # Horizontal win check
    for row in range(3):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    # Diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False

def threaded_client(conn, player):
    global board, current_player, game_over

    initial_data = json.dumps({'player': player, 'board': board, 'game_over': game_over})
    conn.send(str.encode(initial_data))

    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                break

            row, col = map(int, data.split(','))
            if available_square(board, row, col) and current_player == player and not game_over:
                mark_square(board, row, col, player)
                if check_win(board, player):
                    game_over = True
                elif is_board_full(board):
                    game_over = True  # handle a draw condition
                else:
                    current_player = 'O' if player == 'X' else 'X'

            game_state = json.dumps({'board': board, 'current_player': current_player, 'game_over': game_over})
            conn.sendall(str.encode(game_state))
        except:
            break

    conn.close()

# Main loop to accept connections
currentPlayer = 'X'
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer = 'O' if currentPlayer == 'X' else 'X'
