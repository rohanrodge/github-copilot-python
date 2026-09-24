import copy
import random

SIZE = 9
EMPTY = 0
DIFFICULTY_SETTINGS = {
    'easy': {'clues': 40},
    'medium': {'clues': 35},
    'hard': {'clues': 30},
}


def deep_copy(board):
    return copy.deepcopy(board)


def normalize_difficulty(value):
    if value is None:
        return 'medium'
    normalized = str(value).strip().lower()
    if normalized not in DIFFICULTY_SETTINGS:
        return 'medium'
    return normalized


def get_clues_for_difficulty(difficulty):
    return DIFFICULTY_SETTINGS[normalize_difficulty(difficulty)]['clues']


def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_valid_move(board, row, col, num):
    if not isinstance(board, list) or len(board) != SIZE:
        return False
    if not isinstance(row, int) or not isinstance(col, int):
        return False
    if not 0 <= row < SIZE or not 0 <= col < SIZE:
        return False
    if num < 1 or num > SIZE:
        return False

    if board[row][col] == num:
        return True

    for x in range(SIZE):
        if x != col and board[row][x] == num:
            return False

    for y in range(SIZE):
        if y != row and board[y][col] == num:
            return False

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if (r != row or c != col) and board[r][c] == num:
                return False

    return True


def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def count_solutions(board, limit=2):
    if limit <= 0:
        return 0

    if not isinstance(board, list) or len(board) != SIZE:
        return 0

    for row in board:
        if not isinstance(row, list) or len(row) != SIZE:
            return 0
        seen = set()
        for value in row:
            if value == EMPTY:
                continue
            if value in seen or value < 1 or value > SIZE:
                return 0
            seen.add(value)

    for col in range(SIZE):
        seen = set()
        for row in range(SIZE):
            value = board[row][col]
            if value == EMPTY:
                continue
            if value in seen or value < 1 or value > SIZE:
                return 0
            seen.add(value)

    for box_row in range(0, SIZE, 3):
        for box_col in range(0, SIZE, 3):
            seen = set()
            for row in range(box_row, box_row + 3):
                for col in range(box_col, box_col + 3):
                    value = board[row][col]
                    if value == EMPTY:
                        continue
                    if value in seen or value < 1 or value > SIZE:
                        return 0
                    seen.add(value)

    def backtrack():
        best_row = -1
        best_col = -1
        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] == EMPTY:
                    best_row = row
                    best_col = col
                    break
            if best_row != -1:
                break

        if best_row == -1:
            return 1

        solutions = 0
        for candidate in range(1, SIZE + 1):
            if not is_safe(board, best_row, best_col, candidate):
                continue
            board[best_row][best_col] = candidate
            solutions += backtrack()
            if solutions >= limit:
                board[best_row][best_col] = EMPTY
                return solutions
            board[best_row][best_col] = EMPTY

        return solutions

    return backtrack()


def remove_cells(board, clues):
    target = max(0, min(SIZE * SIZE, clues))
    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)

    while sum(cell != EMPTY for row in board for cell in row) > target:
        removed = False
        for row, col in cells:
            if board[row][col] == EMPTY:
                continue
            current_value = board[row][col]
            board[row][col] = EMPTY
            if count_solutions(board, limit=2) == 1:
                removed = True
                break
            board[row][col] = current_value

        if not removed:
            break


def get_incorrect_cells(board, solution):
    if not isinstance(board, list) or not isinstance(solution, list):
        return []

    incorrect = []
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                continue
            if board[row][col] != solution[row][col]:
                incorrect.append((row, col))
    return incorrect


def is_complete(board, solution):
    if not isinstance(board, list) or not isinstance(solution, list):
        return False
    return all(board[row][col] == solution[row][col] for row in range(SIZE) for col in range(SIZE))


def get_hint(board, solution):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                return row, col, solution[row][col]
    return None


def generate_puzzle(clues=35, difficulty=None):
    if difficulty is not None:
        difficulty = normalize_difficulty(difficulty)
        clues = get_clues_for_difficulty(difficulty)
    elif isinstance(clues, str):
        normalized = normalize_difficulty(clues)
        if normalized in DIFFICULTY_SETTINGS:
            clues = get_clues_for_difficulty(normalized)
        else:
            try:
                clues = int(clues)
            except (TypeError, ValueError):
                clues = get_clues_for_difficulty('medium')

    if isinstance(clues, str):
        clues = int(clues)

    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)

    puzzle = deep_copy(board)
    remove_cells(puzzle, clues)

    if count_solutions(puzzle, limit=2) != 1:
        raise ValueError('Generated puzzle does not have exactly one solution.')

    return puzzle, solution
