import sys
import constant
import datetime
from move_generator import generate_moves
from GenerateBoard import generate_result_board
from visualize_board import show_board
import copy

def text_to_matrix_board(text_board_format):
    location_matrix = copy.deepcopy(constant.EMPTY_BOARD)
    print(location_matrix[8][0])
    for value in text_board_format:
        row = constant.LOCATION_DICT[value[0]]
        col = int(value[1]) - constant.LETTER_AND_NUM_OFFSET[row][1]
        if value[2] == 'w':
            location_matrix[row][col] = 1
        elif value[2] == 'b':
            location_matrix[row][col] = 2
        else:
            location_matrix[row][col] = 0
    print(location_matrix)
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
    color = location_matrix[notation_to_coordinates(move_notation[1][0])[0]][notation_to_coordinates(move_notation[1][0])[1]]
    for i in range(len(move_notation[1])):
        if location_matrix[notation_to_coordinates(move_notation[1][i])[0]][notation_to_coordinates(move_notation[1][i])[1]] == 1:
            move_notation[1][i] = move_notation[1][i] + 'w'
            if location_matrix[notation_to_coordinates(move_notation[2][i])[0]][notation_to_coordinates(move_notation[2][i])[1]] == 0:
                move_notation[2][i] = move_notation[2][i] + 'w'
        if location_matrix[notation_to_coordinates(move_notation[1][i])[0]][notation_to_coordinates(move_notation[1][i])[1]] == 2:
            move_notation[1][i] = move_notation[1][i] + 'b'
            if location_matrix[notation_to_coordinates(move_notation[2][i])[0]][notation_to_coordinates(move_notation[2][i])[1]] == 0:
                move_notation[2][i] = move_notation[2][i] + 'b'
        if location_matrix[notation_to_coordinates(move_notation[2][i])[0]][notation_to_coordinates(move_notation[2][i])[1]] == 2:
            move_notation[2][i] = move_notation[2][i] + 'b'
        if location_matrix[notation_to_coordinates(move_notation[2][i])[0]][notation_to_coordinates(move_notation[2][i])[1]] == 1:
            move_notation[2][i] = move_notation[2][i] + 'w'
        # if location_matrix[notation_to_coordinates(move_notation[2][i])[0]][notation_to_coordinates(move_notation[2][i])[1]] == 0:
        #     if color == 1:
        #         move_notation[2][i] = move_notation[2][i] + 'w'
        #     else:
        #         move_notation[2][i] = move_notation[2][i] + 'b'
    return move_notation

# TODO: transposition table

# TODO: implement Iterative deepening
def iterative_deepening(state, color, start_time, time_limit):
    # while True:
    #     # start Time here
    #     current_time = datetime.datetime.now()
    #     if current_time>= time_limit:
    #         break
    val = -sys.maxsize - 1
    for i in range(1, 2):
        v = minimax(state, color, start_time, time_limit)
        if v > val:
            print(v)
            val = v
    return val



def minimax(state, color, start_time, time_limit):

    v = max_value(state, -sys.maxsize - 1, sys.maxsize - 1, color, start_time, time_limit)
    return v

def max_value(state, alpha, beta, color, start_time, time_limit):
    """
    :param state:  [# of marbles out for competitor, # of marbles out for player,
                    [all player 1 marbles’ position(eg. A1,A2…)],[all player 2 marbles’ position],
                    # of marbles near the edge for opponent, # of marbles near the edge for player]

    :param alpha:
    :param beta:
    :param color:
    :param start_time:
    :param time_limit:
    :return:
    """
    print('max', color)
    if terminal_test(state):
        return eval(state)
    v = -sys.maxsize - 1
    moves = generate_moves(state[2], color)
    sorted_moves = sort_moves(moves) # sorting the nodes
    # print(sorted_moves)
    for m in sorted_moves:
        # TODO: update state that is being passed in min_value, currently it's only a location matrix
        # Get the board
        # Update number of outs
        m_with_color = tanslate_move_notation_to_with_color(m, state[2])

        user_num_out = state[0]
        txt_board = translate_board_format_to_text(state[2])
        print(m_with_color)
        # print(state[2])
        # print(txt_board)
        show_board(txt_board)
        result_board = generate_result_board(m_with_color, txt_board)
        print(result_board)
        # print(translate_board_format_to_text(text_to_matrix_board(result_board['board'])))
        matrix_board = text_to_matrix_board(result_board['board'])
        show_board(result_board['board'])
        opp_num_out = ((state[2] + 1) if result_board['isScore'] else state[2])
        new_state = [user_num_out, opp_num_out, matrix_board]
        v = max(v, min_value(new_state, alpha, beta, (2 if color == 1 else 1) ,start_time, time_limit))
        if v > beta:
            return v
        alpha = max(alpha, v)
    return v


def min_value(state, alpha, beta, color, start_time, time_limit):
    """
    :param state:  [# of marbles out for competitor, # of marbles out for player,
                    [all player 1 marbles’ position(eg. A1,A2…)],[all player 2 marbles’ position],
                    # of marbles near the edge for opponent, # of marbles near the edge for player]

    :param alpha:
    :param beta:
    :param color:
    :param start_time:
    :param time_limit:
    :return:
    """
    print("min", color)
    if terminal_test(state):
        return eval(state)
    v = sys.maxsize - 1
    moves = generate_moves(state[2], color)
    sorted_moves = sort_moves(moves)  # sorting the nodes
    # print(sorted_moves)
    for m in sorted_moves:
        m_with_color = tanslate_move_notation_to_with_color(m, state[2])
        user_num_out = state[0]
        txt_board = translate_board_format_to_text(state[2])
        print(m_with_color)
        # print(state[2])
        # print(txt_board)
        show_board(txt_board)
        result_board = generate_result_board(m_with_color, txt_board)
        show_board(result_board['board'])
        matrix_board = text_to_matrix_board(result_board['board'])
        opp_num_out = ((state[2] + 1) if result_board['isScore'] else state[2])
        new_state = [user_num_out, opp_num_out, matrix_board]
        v = min(v, max_value(new_state, alpha, beta, (2 if color == 1 else 1), start_time, time_limit))
        if v <= beta:
            return v
        beta = min(beta, v)
    return v

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
            side_step_two.append([m])
        elif m[0] == 'SS' and len(m[1]) == 3:
            side_step_three.append([m])

    sorted_moves = inline_three + inline_two + side_step_three +side_step_two + single
    return sorted_moves

def terminal_test(state):
    # check if opponent has 6 marbles out
    if state[0] == 6:
        return True # game over
    else:
        return False

def eval(state):
    if(terminal_test(state)):
        return 1000000000000 # return highest value
    else:
        return 10
    #TODO finish implemetning
    # the higher the number of enemy at edge and number of pushed off it should get more points
