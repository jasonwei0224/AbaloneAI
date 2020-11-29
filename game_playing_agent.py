import math
import sys
import random

import constant
import time
from move_generator import generate_moves
from GenerateBoard import generate_result_board
from visualize_board import show_board
import copy

MAX_DEPTH = 100


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
                text_board_format.append(
                    coordinates_to_notation(row, col) + ("b" if selected_board[row][col] == 2 else 'w'))

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
        if location_matrix[notation_to_coordinates(move_notation[1][i])[0]][
            notation_to_coordinates(move_notation[1][i])[1]] == 1:
            move_notation[1][i] = move_notation[1][i] + 'w'
            move_notation[2][i] = move_notation[2][i] + 'w'
        if location_matrix[notation_to_coordinates(move_notation[1][i])[0]][
            notation_to_coordinates(move_notation[1][i])[1]] == 2:
            move_notation[1][i] = move_notation[1][i] + 'b'
            move_notation[2][i] = move_notation[2][i] + 'b'

    return move_notation


# TODO: CONSCIENCE SEARCH

# TODO: transposition table

# TODO: implement Iterative deepening
def iterative_deepening(state, color, start_time, time_limit, first_move):
    start_time = time.perf_counter()
    if first_move:
        moves = generate_moves(state[2], color)
        moves = sort_moves(moves, state, color)
        move_num = random.randint(0, len(moves) - 1)
        color_txt = ('w' if color == 1 else 'b')
        for i in range(len(moves[move_num][1])):
            moves[move_num][1][i] = moves[move_num][1][i] + color
            moves[move_num][2][i] = moves[move_num][2][i] + color

        return 0, moves[move_num], time.perf_counter() - start_time

    depth = 0
    val = -sys.maxsize - 1
    b = ""
    # while True:
    #     if depth >= MAX_DEPTH:
    #         break
    #     # start Time here
    #     current_time = datetime.datetime.now()
    #     if current_time>= time_limit:
    #         break

    v, best_move, time_taken = minimax(state, color, start_time, time_limit, depth)
    if v >= val:
        val = v
        b = best_move
    depth += 1
    return val, b, time_taken


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
    i = 0
    print('\nmax', "Color is: ", color)
    time_taken = time.perf_counter() - start_time
    if terminal_test(state):
        return eval(state), best_move, time_taken
    if depth >= MAX_DEPTH:
        return eval(state), best_move, time_taken
    if time_taken >= time_limit:
        return eval(state), best_move, time_taken
    v = -sys.maxsize - 1
    best_move = ""
    moves = generate_moves(state[2], color)
    sorted_moves = sort_moves(moves, state, color)  # sorting the nodes

    for m in sorted_moves:
        i += 1
        print(i)
        m_with_color = tanslate_move_notation_to_with_color(m, state[2])
        user_num_out = state[0]
        txt_board = translate_board_format_to_text(state[2])
        print("text board: ", txt_board)
        result_board = generate_result_board(m_with_color, txt_board)
        matrix_board = text_to_matrix_board(result_board['board'])
        opp_num_out = ((state[1] + 1) if result_board['isScore'] else state[1])
        new_state = [user_num_out, opp_num_out, matrix_board, state[3], state[4], moves['inline_opp_moves']]
        print("The move: ", m_with_color, "\nprevious state: ", state[:2], "\ncurrent state after move: ",
              new_state[:2], "\nmarble pushed: ", result_board['isScore'], "board: ", matrix_board)
        # new_val, best_move = min_value(new_state, alpha, beta, (2 if color == 1 else 1) ,start_time, time_limit, depth+1, m_with_color)
        new_val, time_taken = min_value(new_state, alpha, beta, (2 if color == 1 else 1), start_time, time_limit,
                                        depth + 1, m_with_color)
        print("current value: ", v, "new value: ", new_val, "alpha", alpha, "beta", beta)
        if type(new_val) is tuple:
            new_val = new_val[0]
        v = max(v, new_val)
        if v > beta:
            return v, best_move, time_taken
        alpha = max(alpha, v)

        best_move = m
    return v, best_move, time_taken


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
    print("\nmin", "Color is: ", color)
    time_taken = time.perf_counter() - start_time

    if terminal_test(state):
        return eval(state), time_taken  # best_move
    if depth >= MAX_DEPTH:
        return eval(state), time_taken  # best_move
    if time_taken >= time_limit:
        return eval(state), time_taken
    v = sys.maxsize - 1
    best_move = ""
    moves = generate_moves(state[2], color)
    sorted_moves = sort_moves(moves, state, color)  # sorting the nodes
    for m in sorted_moves:
        m_with_color = tanslate_move_notation_to_with_color(m, state[2])
        user_num_out = state[1]
        txt_board = translate_board_format_to_text(state[2])
        print("text board: ", txt_board)
        result_board = generate_result_board(m_with_color, txt_board)
        matrix_board = text_to_matrix_board(result_board['board'])
        opp_num_out = ((state[0] + 1) if result_board['isScore'] else state[0])
        new_state = [user_num_out, opp_num_out, matrix_board, state[3], state[4], moves['inline_opp_moves']]
        print("The move: ", m_with_color, "\nprevious state: ", state[:2], "\ncurrent state after move: ",
              new_state[:2], "\nmarble pushed: ", result_board['isScore'], "board: ", matrix_board)
        # new_val, best_move = max_value(new_state, alpha, beta, (2 if color == 1 else 1), start_time, time_limit, depth +1, m_with_color)
        v = max_value(new_state, alpha, beta, (2 if color == 1 else 1), start_time, time_limit,
                      depth + 1, m_with_color)[0]
        # print("current value: ", v, "new value: " ,new_val, "alpha", alpha, "beta", beta)
        # v = min(v, new_val)
        if v <= alpha:
            return v, time_taken  # best_move

        beta = min(beta, v)
    return v, time_taken  # best_move


def sort_moves(moves, state, color):
    # Ordering of moves:
    # 1. Inline
    # 2. Side step
    # 3. single marble
    single_in_middle_already = []
    single_possible_defence = []
    single = []
    inline_edge_two = []
    inline_towards_middle_two = []
    inline_in_middle_two = []
    inline_defence_two = []
    inline_edge_three = []
    inline_towards_middle_three = []
    inline_in_middle_three = []
    inline_defence_three= []
    inline_push_two = []
    inline_push_three = []
    side_step_towards_middle = []
    side_step_defence = []
    side_step_two = []
    side_step_three = []
    enemy_location = []
    pushable_enemy_location = []
    get_point_enemy_location = []

    for row in range(len(state[2])):
        for col in range(len(state[2][row])):
            if state[2][row][col] != color and  state[2][row][col] != 0:
                enemy_location.append(coordinates_to_notation(row, col))

    for m in moves['inline_opp_moves']:
         if '' in m[2]:
             # if the  '' is in the destination then opponent is being pushed off the grid
             for n in m[1]:
                 pushable_enemy_location.append(n)
         else:
             # if the '' is not in the destination then it is just a normal enemy location
             for n in m[1]:
                 pushable_enemy_location.append(n)


    for m in moves['inline_ply_moves']:

        if m[0] == 'I' and len(m[1]) == 1:
            if m[1][0] in constant.EDGE and m[2][0] in constant.EDGE:
                # if start and dest both on edge then its possible escape move
                single_possible_defence.append(m)
            elif m[1][0] in constant.MIDDLE and m[2][0] in constant.EDGE:
                # if in start is in middle and dest is at edge probably "suiciding" giving opponent a chance to push us off
                single.append(m)
            elif m[1][0] in constant.EDGE and m[2][0] in constant.MIDDLE:
                # if start is in edge and go towards middle then it is another possible esacpe move
                single_possible_defence.append(m)
            elif m[1][0] in constant.CENTER and m[2][0] in constant.MIDDLE or m[1][0] in constant.MIDDLE and m[2][0] in constant.CENTER :
                # if start is in center then we rarely would move this cuz we wanna move in three
                single_in_middle_already.append(m)

        elif m[0] == 'I' and len(m[1]) == 2:
            if m[2][0] in pushable_enemy_location or m[2][1] in pushable_enemy_location:
                # if it is pushable
                inline_push_two.append(m)  # TODO Sort by closeness to edge
            else:  # if it is not pushable
                if m[1][0] in constant.CENTER and m[1][1] in constant.CENTER:
                    # A if origin are in the center
                    inline_in_middle_two.append(m)
                elif m[1][0] in constant.CENTER or m[1][1] in constant.CENTER:
                    # B if only one origin is in the center probably should try to move to center
                    if m[2][0] in constant.CENTER and m[2][1] in constant.CENTER:
                        # if destination is in center probably want to make this move
                        inline_towards_middle_two.append(m)
                    else: # if destination is not in center probably dont wanna do this move
                        inline_edge_two.append(m)
                elif m[1][0] not in constant.CENTER or m[1][2] not in constant.CENTER:
                    # C if both origin not in center
                    if m[2][0] in constant.MIDDLE and m[2][1] in constant.MIDDLE and m[1][0] in constant.MIDDLE and m[1][1] in constant.MIDDLE:
                        # if destination is in middle probably want to move to center
                        inline_defence_two.append(m)
                    elif m[2][0] in constant.MIDDLE and m[2][1] in constant.MIDDLE:
                        inline_towards_middle_two.append(m)
                    else: # if destination is not in middle
                        if m[2][0] in constant.EDGE and m[2][1] in constant.EDGE:
                            # if destination at edge possible defensive move
                            inline_defence_two.append(m)
                        else:
                            inline_edge_two.append(m)
        elif m[0] == 'I' and len(m[1]) == 3:
            if m[2][0] in pushable_enemy_location or m[2][1] in pushable_enemy_location or m[2][2] in pushable_enemy_location:
                inline_push_three.append(m)  # TODO Sort by closeness to edge
            else:  # if it is not pushable
                if m[1][0] in constant.CENTER and m[1][1] in constant.CENTER and m[2][2] in constant.CENTER:
                    # A if origin are in the center
                    inline_in_middle_three.append(m)
                elif m[1][0] in constant.CENTER or m[1][1] in constant.CENTER or m[2][2] in constant.CENTER:
                    # B if only one origin is in the center probably should try to move to center
                    if m[2][0] in constant.CENTER and m[2][1] in constant.CENTER or m[2][2] in constant.CENTER and m[2][1] in constant.CENTER:
                        # if two destination is in center probably want to make this move
                        inline_towards_middle_three.append(m)
                    else:  # if destination is not in center probably dont wanna do this move
                        inline_edge_three.append(m)
                elif m[1][0] not in constant.CENTER or m[1][2] not in constant.CENTER or m[2][2] not in constant.CENTER:
                    # C if origin not in center
                    if m[2][0] in constant.CENTER or m[2][1] in constant.CENTER or m[2][2] in constant.CENTER:
                        # if destination is in center probably want to move to center
                        inline_towards_middle_three.append(m)
                    else:  # if destination is not in center
                        if m[2][0] in constant.EDGE and m[2][1] in constant.EDGE and m[2][2] in constant.EDGE:
                            # if all destination at edge possible defensive move
                            inline_defence_three.append(m)
                        else: # horizontally in middle
                            inline_edge_three.append(m)

    for m in moves['sidestep_ply_moves']: # All side step are classified as defend moves for now
        if m[0] == 'SS' and len(m[1]) == 2:
            side_step_defence.append(m)
        elif m[0] == 'SS' and len(m[1]) == 3:
            side_step_defence.append(m)
    # For DEFAULT BOARD
    # sorted_moves = single + single_in_middle_already + inline_in_middle_two + inline_in_middle_three + inline_edge_two + \
    # inline_edge_three + inline_defence_two + inline_defence_three + side_step_defence \
    #               + inline_towards_middle_two + inline_towards_middle_three + inline_push_two + inline_push_three

    # For GERMAN DIASY BOARD
    # sorted_moves = single + single_in_middle_already + inline_edge_two + \
    #                inline_edge_three + inline_defence_two + inline_defence_three + side_step_defence + inline_in_middle_two + inline_in_middle_three\
    #                + inline_towards_middle_two + inline_towards_middle_three + inline_push_two + inline_push_three

    # For BELGIAN DIASY BOARD
    print("inline pushes" , inline_push_two, inline_push_three)

    sorted_moves = single + single_in_middle_already + inline_edge_two + \
                   inline_edge_three + inline_defence_two + inline_defence_three + side_step_defence + inline_in_middle_two + inline_in_middle_three\
                   + inline_towards_middle_two + inline_towards_middle_three + inline_push_two + inline_push_three
    return sorted_moves


def terminal_test(state):
    # check if opponent has 6 marbles out
    if state[0] == 6 or state[1] == 6:
        return True  # game over
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
        user_edge, opponent_edge = get_edge(state[2], state[3])
        # number of player marbles out
        # number of opponent marbles out
        # number of player marbles on edge
        # number of opponent marbles on edge
        # number of pushes available
        # number of pushes that result opponent gets pushed off
        value = state[0] * (-5) + \
                state[1] * 2 + \
                user_edge * (-2) + \
                opponent_edge * 5 + \
                -(distance_from_centre(state[2], state[3])) * 30 + \
                len(state[5]) * 20 + \
                calculate_push_off(state[5])[0] * 10 + \
                calculate_push_off(state[5])[1] * 100


        return value


def calculate_push_off(opp_move):
    count = 0
    push = 0
    for m in opp_move:
        if m[2] == [] or m[2][-1] == '':
            count += 1
        else:
            push +=1
    return count, push


def calculate_center(row, col):
    center_x = 3
    center_y = 4
    dist = (row - center_y) ** 2 + (col - center_x) ** 2
    dist = math.sqrt(dist)
    return int(dist)


def distance_from_centre(matrix, color):
    player = 0
    opponent = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] != 0:
                if matrix[row][col] == color:
                    player += calculate_center(row, col)
                else:
                    opponent += calculate_center(row, col)

    return player


def get_edge(matrix, color):
    user_edge = 0
    opponent_edge = 0

    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if row == 0 or row == 8 or col == 0 or col == len(matrix[row]) - 1:
                if matrix[row][col] == color:
                    user_edge += 1
                elif matrix[row][col] != 0:
                    opponent_edge += 1
    return user_edge, opponent_edge


