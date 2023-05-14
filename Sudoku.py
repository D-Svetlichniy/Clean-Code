import PySimpleGUI as sg
import numpy as np
import random


def generate_sudoku(mask_rate, n):
    solution = np.zeros((n, n), np.int32)
    rg = np.arange(1, n + 1)
    solution[0, :] = np.random.choice(rg, n, replace=False)
    for r in range(1, n):
        for c in range(n):
            col_rest = np.setdiff1d(rg, solution[:r, c])
            row_rest = np.setdiff1d(rg, solution[r, :c])
            available_numbers_col = np.intersect1d(col_rest, row_rest)
            subgrid_row, subgrid_col = r // 3, c // 3
            available_numbers_subgrid = np.setdiff1d(np.arange(0, n + 1),
                                                     solution[subgrid_row * 3:(subgrid_row + 1) * 3,
                                                     subgrid_col * 3:(subgrid_col + 1) * 3].ravel())
            available_numbers = np.intersect1d(available_numbers_col, available_numbers_subgrid)
            solution[r, c] = np.random.choice(available_numbers, size=1)
    puzzle = solution.copy()
    puzzle[np.random.choice([True, False], size=solution.shape, p=[mask_rate, 1 - mask_rate])] = 0
    return puzzle, solution


def check_progress(window, solution):
    solved = True
    for r, row in enumerate(solution):
        for c, col in enumerate(row):
            value = window[r, c].get()
            if value:
                value = int(value)
            if value != solution[r][c]:
                window[r, c].update(background_color='red')
                solved = False
            else:
                window[r, c].update(background_color=sg.theme_input_background_color())
        else:
            solved = False
            window[r, c].update(background_color='yellow')
    return solved


def create_and_show_puzzle(window, rate_flag, mask_rate, n):
    if window[rate_flag].get():
        try:
            mask_rate = float(window[rate_flag].get())
        except:
            pass
    puzzle, solution = generate_sudoku(mask_rate, n)
    for r, row in enumerate(puzzle):
        for c, col in enumerate(row):
            window[r, c].update(puzzle[r][c] if puzzle[r][c] else '',
                                background_color=sg.theme_input_background_color())
    return puzzle, solution


def main(mask_rate, n, rate_flag, grid_size, solve_flag, check_flag, hint_flag, new_game_flag, mask_rate_flag):
    window_layout = [
        [sg.Frame('', [
            [sg.I(random.randint(1, 9), justification='r', size=(grid_size, 1), enable_events=True,
                  key=(fr * grid_size + r, fc * grid_size + c)) for c in range(grid_size)]
            for r in range(grid_size)])
         for fc in range(grid_size)]
        for fr in range(grid_size)],[
                sg.B(solve_flag),
                sg.B(check_flag),
                sg.B(hint_flag),
                sg.B(new_game_flag),
                sg.T(mask_rate_flag),
                sg.In(str(mask_rate), size=(grid_size, 1), key=rate_flag)
            ]

    window = sg.Window('Sudoku', window_layout, finalize=True)

    puzzle, solution = create_and_show_puzzle(window)
    check_showing = False
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == solve_flag:
            for r, row in enumerate(solution):
                for c, col in enumerate(row):
                    window[r, c].update(solution[r][c], background_color=sg.theme_input_background_color())
        elif event == check_flag:
            check_showing = True
            solved = check_progress(window, solution)
            if solved:
                sg.popup('Solved! You have solved the puzzle correctly.')
        elif event == hint_flag:
            elem = window.find_element_with_focus()
            try:
                elem.update(solution[elem.Key[0]][elem.Key[1]], background_color=sg.theme_input_background_color())
            except:
                pass
        elif event == new_game_flag:
            puzzle, solution = create_and_show_puzzle(window, rate_flag, mask_rate, n)
        elif check_showing:
            check_showing = False
            for r, row in enumerate(solution):
                for c, col in enumerate(row):
                    window[r, c].update(background_color=sg.theme_input_background_color())
    window.close()


if __name__ == "__main__":
    DEFAULT_MASK_RATE = 0.1
    n = 9
    MASK_RATE_FLAG = 'Mask rate (0-1)'
    RATE_FLAG = '-RATE-'
    GRID_SIZE = 3
    SOLVE_FLAG = 'Solve'
    CHECK_FLAG = 'Check'
    HINT_FLAG = 'Hint'
    NEW_GAME_FLAG = 'New game'
    main(DEFAULT_MASK_RATE, n, RATE_FLAG, GRID_SIZE, SOLVE_FLAG, CHECK_FLAG, HINT_FLAG, NEW_GAME_FLAG, MASK_RATE_FLAG)
