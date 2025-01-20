from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Initialize the game board
def init_board():
    return ['' for _ in range(9)]

# Check for a win or draw
def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != '':
            return board[condition[0]]
    if '' not in board:
        return 'Draw'
    return None

# Computer move logic
def computer_move(board):
    available_moves = [i for i in range(9) if board[i] == '']
    return random.choice(available_moves)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    board = data['board']
    user_move = data['user_move']

    # User's move
    if board[user_move] == '':
        board[user_move] = 'X'
    else:
        return jsonify({'error': 'Invalid move'})

    # Check if user wins
    result = check_winner(board)
    if result:
        return jsonify({'board': board, 'result': result})

    # Computer's move
    comp_move = computer_move(board)
    board[comp_move] = 'O'

    # Check if computer wins
    result = check_winner(board)
    return jsonify({'board': board, 'result': result})

if __name__ == '__main__':
    app.run(debug=True)