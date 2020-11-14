import sys
import datetime
from move_generator import generate_moves
from GenerateBoard import generate_result_board


# initial_state = [0,0,location_matrix,7,7]

# TODO: transposition table

# TODO: implement Iterative deepening
def iterative_deepening(state, time_limit):
    while True:
        # start Time here
        current_time = datetime.datetime.now()
        if current_time>= time_limit:
            break

    pass


def minimax(state, color, start_time, time_limit):

    v = max_value(state, -sys.maxsize - 1, sys.maxsize - 1, color, start_time, time_limit)
    return get_move(locatin_matrix, v)

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
    if terminal_test(state):
        return eval(state)
    v = -sys.maxsize - 1
    moves = generate_moves(state[2], color)
    sorted_moves = sort_moves(moves) # sorting the nodes
    for m in sorted_moves:
        # TODO: update state that is being passed in min_value, currently it's only a location matrix
        # Get the board
        # Update number of outs
        v = max(v, min_value(generate_result_board([m], state[2]), alpha, beta, (2 if color == 1 else 1),start_time, time_limit))
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

    if terminal_test(state):
        return eval(state)
    v = sys.maxsize - 1
    for m in generate_moves(state[2], color):
        # TODO: update state that is being passed in max_value, currently it's only a location matrix
        v = min(v, max_value(generate_result_board([m], state[2]), alpha, beta, 2 if color == 1 else 10, start_time, time_limit))
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
        return highest_val # return highest value

    #TODO finish implemetning
    # the higher the number of enemy at edge and number of pushed off it should get more points

    pass