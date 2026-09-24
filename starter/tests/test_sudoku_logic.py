import sudoku_logic


def board_is_valid(board):
    expected = list(range(1, 10))

    for row in board:
        if sorted(row) != expected:
            return False

    for col in range(sudoku_logic.SIZE):
        if sorted(board[row][col] for row in range(sudoku_logic.SIZE)) != expected:
            return False

    for box_row in range(0, sudoku_logic.SIZE, 3):
        for box_col in range(0, sudoku_logic.SIZE, 3):
            values = []
            for row in range(box_row, box_row + 3):
                for col in range(box_col, box_col + 3):
                    values.append(board[row][col])
            if sorted(values) != expected:
                return False

    return True


def test_create_empty_board_has_correct_shape():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(value == sudoku_logic.EMPTY for row in board for value in row)


def test_is_safe_rejects_duplicates_and_allows_valid_move():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.is_safe(board, 0, 0, 5) is True
    board[0][1] = 5
    assert sudoku_logic.is_safe(board, 0, 0, 5) is False

    board = sudoku_logic.create_empty_board()
    board[1][0] = 5
    assert sudoku_logic.is_safe(board, 0, 0, 5) is False

    board = sudoku_logic.create_empty_board()
    board[0][0] = 5
    board[1][1] = 5
    assert sudoku_logic.is_safe(board, 2, 2, 5) is False

    board = sudoku_logic.create_empty_board()
    assert sudoku_logic.is_safe(board, 8, 8, 9) is True


def test_fill_board_solves_a_complete_grid_without_zeros():
    board = sudoku_logic.create_empty_board()
    solved = sudoku_logic.fill_board(board)

    assert solved is True
    assert board_is_valid(board)
    assert all(value != sudoku_logic.EMPTY for row in board for value in row)


def test_generate_puzzle_returns_valid_puzzle_and_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(35)

    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert len(solution) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in solution)
    assert board_is_valid(solution)

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if puzzle[row][col] != sudoku_logic.EMPTY:
                assert puzzle[row][col] == solution[row][col]


def test_generate_puzzle_has_exactly_one_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(35)

    assert board_is_valid(solution)
    assert sudoku_logic.count_solutions(puzzle, limit=2) == 1
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 35


def test_count_solutions_confirms_generated_puzzle_uniqueness():
    puzzle, _ = sudoku_logic.generate_puzzle(35)

    assert sudoku_logic.count_solutions(puzzle, limit=2) == 1


def test_generate_puzzle_respects_difficulty_levels():
    easy, _ = sudoku_logic.generate_puzzle('easy')
    medium, _ = sudoku_logic.generate_puzzle('medium')
    hard, _ = sudoku_logic.generate_puzzle('hard')

    easy_clues = sum(cell != sudoku_logic.EMPTY for row in easy for cell in row)
    medium_clues = sum(cell != sudoku_logic.EMPTY for row in medium for cell in row)
    hard_clues = sum(cell != sudoku_logic.EMPTY for row in hard for cell in row)

    assert easy_clues > medium_clues > hard_clues
    assert sudoku_logic.count_solutions(easy, limit=2) == 1
    assert sudoku_logic.count_solutions(medium, limit=2) == 1
    assert sudoku_logic.count_solutions(hard, limit=2) == 1


def test_is_valid_move_rejects_duplicate_values_and_allows_valid_move():
    board = sudoku_logic.create_empty_board()
    assert sudoku_logic.is_valid_move(board, 0, 0, 5) is True

    board[0][1] = 5
    assert sudoku_logic.is_valid_move(board, 0, 0, 5) is False

    board = sudoku_logic.create_empty_board()
    board[1][0] = 5
    assert sudoku_logic.is_valid_move(board, 0, 0, 5) is False

    board = sudoku_logic.create_empty_board()
    board[0][0] = 5
    board[1][1] = 5
    assert sudoku_logic.is_valid_move(board, 2, 2, 5) is False


def test_get_incorrect_cells_and_completion_status():
    solution = [[(row * 9 + col) % 9 + 1 for col in range(9)] for row in range(9)]
    board = [row[:] for row in solution]
    board[0][0] = 8

    incorrect = sudoku_logic.get_incorrect_cells(board, solution)
    assert (0, 0) in incorrect
    assert sudoku_logic.is_complete(board, solution) is False

    board = [row[:] for row in solution]
    assert sudoku_logic.get_incorrect_cells(board, solution) == []
    assert sudoku_logic.is_complete(board, solution) is True
