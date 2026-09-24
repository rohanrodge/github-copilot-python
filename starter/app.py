import time

from flask import Flask, jsonify, render_template, request, session

import sudoku_logic

app = Flask(__name__)
app.secret_key = 'starter-secret-key'


def reset_game():
    session.clear()


@app.route('/')
def index():
    reset_game()
    return render_template('index.html')


@app.route('/new')
def new_game():
    difficulty = sudoku_logic.normalize_difficulty(
        request.args.get('difficulty') or session.get('difficulty') or 'medium'
    )

    clues_value = request.args.get('clues')
    clues = None
    if clues_value is not None:
        try:
            clues = int(clues_value)
        except (TypeError, ValueError):
            clues = None

    if clues is None:
        clues = sudoku_logic.get_clues_for_difficulty(difficulty)

    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    session['puzzle'] = [row[:] for row in puzzle]
    session['solution'] = [row[:] for row in solution]
    session['difficulty'] = difficulty
    session['hints_used'] = 0
    session['completed'] = False
    session['timer_started_at'] = time.time()
    session['elapsed_seconds'] = 0
    return jsonify({
        'puzzle': session['puzzle'],
        'difficulty': session['difficulty'],
        'hints_used': session['hints_used'],
        'elapsed_seconds': 0,
    })


@app.route('/check', methods=['POST'])
def check_solution():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'No game in progress'}), 400

    board = data.get('board')
    solution = session.get('solution')
    if solution is None or board is None:
        return jsonify({'error': 'No game in progress'}), 400

    incorrect = [[row, col] for row, col in sudoku_logic.get_incorrect_cells(board, solution)]
    complete = sudoku_logic.is_complete(board, solution)
    if complete:
        session['completed'] = True
    return jsonify({'incorrect': incorrect, 'complete': complete})


@app.route('/hint', methods=['POST'])
def give_hint():
    data = request.get_json(silent=True) or {}
    board = data.get('board')
    solution = session.get('solution')

    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    if board is None:
        board = session.get('puzzle')
    if board is None:
        return jsonify({'error': 'No game in progress'}), 400

    if sudoku_logic.is_complete(board, solution):
        return jsonify({'error': 'Puzzle already completed', 'complete': True})

    hint = sudoku_logic.get_hint(board, solution)
    if hint is None:
        return jsonify({'error': 'No hints available', 'complete': True})

    row, col, value = hint
    board[row][col] = value
    session['puzzle'] = [board_row[:] for board_row in board]
    session['hints_used'] = int(session.get('hints_used', 0)) + 1

    return jsonify({
        'row': row,
        'col': col,
        'value': value,
        'hints_used': session['hints_used'],
        'complete': sudoku_logic.is_complete(session['puzzle'], solution),
    })

if __name__ == '__main__':
    app.run(debug=True)