"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 28, 2022
"""

def is_empty(board):
    for y_i in range(len(board[0])):
        for x_i in range(len(board)):
            if board[x_i][y_i] != " ":
                return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    counter = 0

    if board[y_end][x_end] == " ":
        return None
    if y_end - d_y*(length-1) < 0 or y_end - d_y*(length-1) >= len(board) or x_end - d_x*(length-1) < 0 or x_end - d_x*(length-1) >= len(board[0]):
        return None
    # Checks bounds
    if y_end + d_y < 0 or y_end + d_y >= len(board) or x_end + d_x < 0 or x_end + d_x >= len(board[0]):
        counter += 1
    elif y_end - d_y < 0 or y_end - d_y >= len(board) or x_end - d_x < 0 or x_end - d_x >= len(board[0]):
        counter += 1
    # Checks if coord is inside a sequence
    elif board[y_end + d_y][x_end + d_x] != " " and board[y_end - d_y][x_end - d_x] != " ":
        if board[y_end][x_end] == board[y_end - d_y][x_end - d_x]:
            if board[y_end + d_y][x_end + d_x] == board[y_end - d_y][x_end - d_x]:
                return None
            counter += 1

    # Goes to the start of the sequence - 1
    for i in range(length):
        if (y_end - d_y) >= 0 and (x_end - d_x) >= 0 and (y_end - d_y) < len(board) and (x_end - d_x) < len(board[0]):
            if i != length - 1:
                if board[y_end][x_end] != board[y_end - d_y][x_end - d_x]:
                    return None
        y_end -= d_y
        x_end -= d_x

    # Checks bounds
    if y_end < 0 or x_end < 0 or y_end >= len(board) or x_end >= len(board[0]):
        counter += 1
    # Checks if the start is in inside a sequence already
    elif board[y_end][x_end] != " ":
        if board[y_end][x_end] == board[y_end + d_y][x_end + d_x]:
            return None
        counter += 1

    if counter == 0:
        return 'OPEN'
    elif counter == 1:
        return 'SEMIOPEN'
    elif counter == 2:
        return 'CLOSED'


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    y_end = y_start + d_y*(length - 1)
    x_end = x_start + d_x*(length - 1)

    # Finds [y_end][x_end] from [y_start][x_start] to use fnc is_bounded()
    while y_end < len(board) and y_end >= 0 and x_end < len(board[0]) and x_end >= 0:
        if board[y_end][x_end] == col:
            if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
                open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == 'SEMIOPEN':
                semi_open_seq_count += 1
        y_end += d_y
        x_end += d_x

    return (open_seq_count, semi_open_seq_count)


def detect_rows(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0

    for y in range(len(board)):
        # Checks horizontals
        new_row = detect_row(board, col, y, 0, length, 0, 1)
        # Checks bottom triangle diagonals -> v
        new_row2 = detect_row(board, col, y, 0, length, 1, 1)
        # Checks upper triangle diagonals -> ^
        new_row3 = detect_row(board, col, y, 0, length, -1, 1)

        open_seq_count += (new_row[0] + new_row2[0] + new_row3[0])
        semi_open_seq_count += (new_row[1] + new_row2[1] + new_row3[1])

    for x in range(len(board[0])):
        # Checks verticals
        new_row = detect_row(board, col, 0, x, length, 1, 0)
        # Checks upper triangle diagonals -> v
        new_row2 = detect_row(board, col, 0, x + 1, length, 1, 1)
        # Checks upper triangle diagonals -> ^
        new_row3 = detect_row(board, col, len(board) - 1, x + 1, length, -1, 1)

        open_seq_count += (new_row[0] + new_row2[0] + new_row3[0])
        semi_open_seq_count += (new_row[1] + new_row2[1] + new_row3[1])

    return (open_seq_count, semi_open_seq_count)


def search_max(board):
    import copy # Apologies... I realize it is inefficient, but it is also simple :')
    best_board = copy.deepcopy(board)
    count = len(board) * len(board[0])

    # Compares and finds the best move by testing each possible location
    for y in range(len(board)):
        for x in range(len(board[0])):
            count -= 1
            temp_board = copy.deepcopy(board)
            if temp_board[y][x] == " ":
                count += 1
                temp_board[y][x] = "b"
                if score(temp_board) > score(best_board):
                    move_y = y
                    move_x = x
                    best_board = copy.deepcopy(temp_board)
                # Checks if there is only one move available and forces it
                elif count == 1:
                    return y, x

    return move_y, move_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    c_tot = 0
    p_tot = 0

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == "b":
                if is_bounded(board, y, x, 5, 0, 1) == "CLOSED":
                    c_tot += 1
                    print(1, c_tot)
                if is_bounded(board, y, x, 5, 1, 0) == "CLOSED":
                    c_tot += 1
                if is_bounded(board, y, x, 5, 1, 1) == "CLOSED":
                    c_tot += 1
                if is_bounded(board, y, x, 5, -1, 1) == "CLOSED":
                    c_tot += 1
            elif board[y][x] == "w":
                if is_bounded(board, y, x, 5, 0, 1) == "CLOSED":
                    p_tot += 1
                if is_bounded(board, y, x, 5, 1, 0) == "CLOSED":
                    p_tot += 1
                if is_bounded(board, y, x, 5, 1, 1) == "CLOSED":
                    p_tot += 1
                if is_bounded(board, y, x, 5, -1, 1) == "CLOSED":
                    p_tot += 1

    # Checks board for any winning sequences from prev fnc
    c_dr = detect_rows(board, "b", 5)
    p_dr = detect_rows(board, "w", 5)

    # Adds total sequences of 5
    c_tot += (c_dr[0] + c_dr[1])
    p_tot += (p_dr[0] + p_dr[1])

    # Simultaneously compares potential winners
    if c_tot > 0 and p_tot == 0:
        return "Black won"
    elif c_tot == 0 and p_tot > 0:
        return "White won"
    else:
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == " ":
                    return "Continue playing"
        return "Draw"

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x =2; y = 3; d_x = 1; d_y = -1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 1
    x_end = 4

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")
    print(is_bounded(board, y_end, x_end, length, d_y, d_x))

def test_detect_row():
    board = make_empty_board(8)
    x =2; y = 3; d_x = 1; d_y = -1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, 5, 5, 1, 1, 3, "b")
    print_board(board)
    if detect_row(board, "w", 4,1,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 3; d_x = 0; d_y = -1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, y, 6, d_y, d_x, length, "b")
    print_board(board)
    if detect_rows(board, col,length) == (0,1):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0



if __name__ == '__main__':
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()
    some_tests()
    print(play_gomoku(8))
