import sys
import random

import constant
import datetime
from move_generator import generate_moves
from GenerateBoard import generate_result_board
from visualize_board import show_board
import copy

MAX_DEPTH = 3

def text_to_matrix_board(text_board_format):
    location_matrix = copy.deepcopy(constant.EMPTY_BOARD)
    for value in text_board_format:
        row = constant.LOCATION_DICT[value[0]]
        col = int(value[1]) - constant.LETTER_AND_NUM_OFFSET[row][1]
        if value[2] == 'w':
            location_matrix[row][col] = 1
        elif value[2] == 'b':
            location_matrix[row][col] = 2
        else:
            location_matrix[row][col] = 0

    return location_matrix

def translate_board_format_to_text(selected_board):
    text_board_format = []
    for row in range(len(selected_board)):
        for col in range(len(selected_board[row])):
            if selected_board[row][col] == 1 or selected_board[row][col] == 2:
                text_board_format.append(coordinates_to_notation(row, col) + ("b" if selected_board[row][col] == 2 else 'w'))

    return text_board_format

def coordinates_to_notation(row, col):
    """
    change matrix row, col to notation used in class
    :param row: int
    :param col: int
    :return: string E.g. "A1"
    """
    return str(constant.LETTER_AND_NUM_OFFSET[row][0]) + str(col + constant.LETTER_AND_NUM_OFFSET[row][1])

def notation_to_coordinates(s):
    """
    change notation used in class to matrix row and col
    :param s: notation E.g. A5
    :return: coordinates in tuple (row, col)
    """
    return (
        int(constant.LOCATION_DICT[s[0]]), int(s[1]) - constant.LETTER_AND_NUM_OFFSET[constant.LOCATION_DICT[s[0]]][1])

def tanslate_move_notation_to_with_color(move_notation, location_matrix):

    for i in range(len(move_notation[1])):
        if location_matrix[notation_to_coordinates(move_notation[1][i])[0]][notation_to_coordinates(move_notation[1][i])[1]] == 1:
            move_notation[1][i] = move_notation[1][i] + 'w'
            move_notation[2][i] = move_notation[2][i] + 'w'
        if location_matrix[notation_to_coordinates(move_notation[1][i])[0]][notation_to_coordinates(move_notation[1][i])[1]] == 2:
            move_notation[1][i] = move_notation[1][i] + 'b'
            move_notation[2][i] = move_notation[2][i] + 'b'

    return move_notation


# TODO: CONSCIENCE SEARCH

# TODO: transposition table

# TODO: implement Iterative deepening
def iterative_deepening(state, color, start_time, time_limit, first_move):

    if first_move:
        moves = generate_moves(state[2], color)
        moves = sort_moves(moves)
        move_num = random.randint(0, len(moves)-1)
        color_txt = ('w' if color == 1 else 'b')
        for i in range(len(moves[move_num][1])):
            moves[move_num][1][i] = moves[move_num][1][i] + color_txt
            moves[move_num][2][i] = moves[move_num][2][i] + color_txt

        return 0, moves[move_num]

    depth = 0
    val = -sys.maxsize - 1
    b = ""
    while depth < MAX_DEPTH:
        # if depth >= MAX_DEPTH:
        #     break
        # start Time here
    #     current_time = datetime.datetime.now()
    #     if current_time>= time_limit:
    #         break
        v, best_move = minimax(state, color, start_time, time_limit, depth)
        if v >= val:
            val = v
            b = best_move
        depth += 1
    return val, b



def minimax(state, color, start_time, time_limit, depth):

    v = max_value(state, -sys.maxsize - 1, sys.maxsize - 1, color, start_time, time_limit, depth, "")
    return v

def max_value(state, alpha, beta, color, start_time, time_limit, depth, best_move):
    """
    :param state:  [# of marbles out for competitor, # of marbles out for player,matrix]
    :param alpha:
    :param beta:
    :param color:
    :param start_time:
    :param time_limit:
    :return:
    """
    print('\nmax', "Color is: " , color)
    if terminal_test(state):
        return eval(state), best_move
    if depth >= MAX_DEPTH:
        return eval(state), best_move
    if datetime.datetime.now().second - start_time >= time_limit:
        return eval(state), best_move
    v = -sys.maxsize - 1
    best_move = ""
    moves = generate_moves(state[2], color)
    sorted_moves = sort_moves(moves) # sorting the nodes

    for m in sorted_moves:
        m_with_color = tanslate_move_notation_to_with_color(m, state[2])
        user_num_out = state[0]
        txt_board = translate_board_format_to_text(state[2])
        print("text board: ",txt_board)
        result_board = generate_result_board(m_with_color, txt_board)
        matrix_board = text_to_matrix_board(result_board['board'])
        opp_num_out = ((state[1] + 1) if result_board['isScore'] else state[1])
        new_state = [user_num_out, opp_num_out, matrix_board, state[3], state[4]]
        print("The move: ", m_with_color, "\nprevious state: ", state[:2], "\ncurrent state after move: ", new_state[:2], "\nmarble pushed: ", result_board['isScore'], "board: ", matrix_board)
        new_val, best_move = min_value(new_state, alpha, beta, (2 if color == 1 else 1) ,start_time, time_limit, depth+1, m_with_color)
        print("current value: ", v, "new value: " ,new_val)
        v = max( v, new_val)
        if v > beta:
            return v, best_move
        alpha = max(alpha, v)
    return v, best_move


def min_value(state, alpha, beta, color, start_time, time_limit, depth, best_move):
    """
    :param state:  [# of marbles out for competitor, # of marbles out for player,matrix]
    :param alpha:
    :param beta:
    :param color:
    :param start_time:
    :param time_limit:
    :return:
    """
    # best_move = ""
    print("\nmin", "Color is: " , color)
    if terminal_test(state):
        return eval(state), best_move
    if depth >= MAX_DEPTH:
        return eval(state), best_move
    if datetime.datetime.now() - start_time >= time_limit:
        return eval(state), best_move
    v = sys.maxsize - 1
    best_move = ""
    moves = generate_moves(state[2], color)
    sorted_moves = sort_moves(moves)  # sorting the nodes
    for m in sorted_moves:
        m_with_color = tanslate_move_notation_to_with_color(m, state[2])
        user_num_out = state[1]
        txt_board = translate_board_format_to_text(state[2])
        result_board = generate_result_board(m_with_color, txt_board)
        matrix_board = text_to_matrix_board(result_board['board'])
        opp_num_out = ((state[0] + 1) if result_board['isScore'] else state[0])
        new_state = [user_num_out, opp_num_out, matrix_board,state[3], state[4]]
        print("The move: ", m_with_color, "\nprevious state: ", state[:2], "\ncurrent state after move: ", new_state[:2], "\nmarble pushed: ", result_board['isScore'])
        new_val, best_move = max_value(new_state, alpha, beta, (2 if color == 1 else 1), start_time, time_limit, depth +1, m_with_color)
        print("current value: ", v, "new value: " ,new_val)
        v = min(v, new_val)
        if v <= beta:
            return v, best_move
        beta = min(beta, v)
    return v, best_move

def sort_moves(moves):
    # Ordering of moves:
    # 1. Inline
    # 2. Side step
    # 3. single marble
    # TODO future consideration: more detail move ordering e.g inlines moves that's closer to edge first
    inline_two = []
    inline_three = []
    side_step_two = []
    side_step_three = []
    single = []
    for m in moves['inline_ply_moves']:
        if m[0] == 'I' and len(m[1]) == 1:
            single.append(m)
        elif m[0] == 'I' and len(m[1]) == 2:
            inline_two.append(m)
        elif m[0] == 'I' and len(m[1]) == 3:
            inline_three.append(m)
    for m in moves['sidestep_ply_moves']:
        if m[0] == 'SS' and len(m[1]) == 2:
            side_step_two.append(m)
        elif m[0] == 'SS' and len(m[1]) == 3:
            side_step_three.append(m)

    sorted_moves = inline_three + inline_two + side_step_three + side_step_two + single
    return sorted_moves

def terminal_test(state):
    # check if opponent has 6 marbles out
    if state[0] == 6 or state[1] == 6:
        return True # game over
    else:
        return False

def eval(state):
    """

    :param state:
    :return:
    """

    if state[0] == 6:
        return sys.maxsize  # return highest value
    elif state[1] == 6:
        return -sys.maxsize
    else:
        user_edge, opponent_edge = getEdge(state[2], state[3])
        value = state[0] * (-100) + state[1] * 100 + user_edge * (-50) + opponent_edge * 50

        return value
    #TODO finish implemetning
    # the higher the number of enemy at edge and number of pushed off it should get more points

def getEdge(matrix, color):
    user_edge = 0
    opponent_edge = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if row == 0 or row == 8 or col == 0 or col == len(matrix[row]) - 1:
                if matrix[row][col] == color:
                    user_edge +=1
                elif matrix[row][col] != 0:
                    opponent_edge +=1
    return user_edge, opponent_edge