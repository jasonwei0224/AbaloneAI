import constant
import PySimpleGUI as sg
import numpy as np

# import gui

location_dict = {"I": 0, "H": 1, "G": 2, "F": 3, "E": 4, "D": 5, "C": 6, "B": 7, "A": 8}

# from the row number get the letter and the offset of the number for each location
letter_and_numOffset = {0: ('I', 5), 1: ('H', 4), 2: ('G', 3), 3: ('F', 2), 4: ('E', 1), 5: ('D', 1), 6: ('C', 1),
                        7: ('B', 1), 8: ('A', 1)}

coord_dict = {(0, 0): ["I", 5], (0, 1): ["I", 6], (0, 2): ["I", 7], (0, 3): ["I", 8], (0, 4): ["I", 9],
              (1, 0): ["H", 4], (1, 1): ["H", 5], (1, 2): ["H", 6], (1, 3): ["H", 7], (1, 4): ["H", 8],
              (1, 5): ["H", 9],
              (2, 0): ["G", 3], (2, 1): ["G", 4], (2, 2): ["G", 5], (2, 3): ["G", 6], (2, 4): ["G", 7],
              (2, 5): ["G", 8], (2, 6): ["G", 9],
              (3, 0): ["F", 2], (3, 1): ["F", 3], (3, 2): ["F", 4], (3, 3): ["F", 5], (3, 4): ["F", 6],
              (3, 5): ["F", 7], (3, 6): ["F", 8], (3, 7): ["F", 9],
              (4, 0): ["E", 1], (4, 1): ["E", 2], (4, 2): ["E", 3], (4, 3): ["E", 4], (4, 4): ["E", 5],
              (4, 5): ["E", 6], (4, 6): ["E", 7], (4, 7): ["E", 8], (4, 8): ["E", 9],
              (5, 0): ["D", 1], (5, 1): ["D", 2], (5, 2): ["D", 3], (5, 3): ["D", 4], (5, 4): ["D", 5],
              (5, 5): ["D", 6], (5, 6): ["D", 7], (5, 8): ["D", 8],
              (6, 0): ["C", 1], (6, 1): ["C", 2], (6, 2): ["C", 3], (6, 3): ["C", 4], (6, 4): ["C", 5],
              (6, 5): ["C", 6], (6, 6): ["C", 7],
              (7, 0): ["B", 1], (7, 1): ["B", 2], (7, 2): ["B", 3], (7, 3): ["B", 4], (7, 4): ["B", 5],
              (7, 5): ["B", 6],
              (8, 0): ["A", 1], (8, 1): ["A", 2], (8, 2): ["A", 3], (8, 3): ["A", 4], (8, 4): ["A", 5]}


def get_input(file_name):
    file = open(file_name, "r")
    player_color = file.readline()
    print(player_color)
    locations = file.readline().split(',')

    location_matrix = constant.EMPTY_BOARD

    for value in locations:
        row = constant.LOCATION_DICT[value[0]]
        col = int(value[1]) - constant.LETTER_AND_NUM_OFFSET[row][1]
        color = 1 if value[2] == 'w' else 2
        location_matrix[row][col] = color

    return location_matrix, color


def draw_board(canvas, matrix):
    """
    This draws the Abalone game board with coordinates listed on each location
    :param canvas: the canavas on the GUI to be draw on
    :return: null
    """
    offset_lst = [48, 38, 28, 17, 5, 17, 28, 38, 48]  # this changes the distance from the left to the first circle
    width = 28  # this changes the distance between the marbles
    radius = 13  # this changes the size of the marble
    for row in range(len(matrix)):
        offset = offset_lst[row]
        for col in range(len(matrix[row])):
            if matrix[row][col] == 0:
                canvas.DrawCircle((col * width + 20 + offset, row * width + 15), radius,
                                  fill_color="dark grey")

            elif matrix[row][col] == 1:
                canvas.DrawCircle((col * width + 20 + offset, row * width + 15), radius,
                                  fill_color='white')

            elif matrix[row][col] == 2:
                canvas.DrawCircle((col * width + 20 + offset, row * width + 15), radius,
                                  fill_color='black')

            canvas.draw_text(
                '{}'.format(constant.LETTER_AND_NUM_OFFSET[row][0] + str(constant.LETTER_AND_NUM_OFFSET[row][1] + col)),
                (col * width + 20 + offset, row * width + 15), color="red")


def show_grid(location_matrix, ):
    graph_element = sg.Graph((600, 600), (0, 300), (300, 0), key='graph')
    window = sg.Window('Abalone', [[graph_element]], font=('arial', 15)).Finalize()
    draw_board(graph_element, location_matrix)
    event, values = window.read()


def generate_moves(matrix, player_color):
    inline_ply_moves, inline_opp_moves = generate_inline(player_color, matrix)
    sidestep_ply_moves = generate_sidestep(player_color, matrix)
    print("Inline", inline_ply_moves)
    print("SS", sidestep_ply_moves)
    print("Opposite moves", inline_opp_moves)


def generate_inline(color, location_matrix):
    """
    Generates inline moves (for 1, 2, or 3 marbles).
    :return:
    """
    player = color

    locations = [(ix, iy) for ix, row in enumerate(location_matrix) for iy, i in enumerate(row) if i == player]
    opp_loc = [(ix, iy) for ix, row in enumerate(location_matrix) for iy, i in enumerate(row) if i != player and i != 0]

    move_notation = []
    opp_move_notation = []

    directions = [move_1, move_3, move_5, move_7, move_9, move_11]

    # for 1 marble moving inline
    for move in directions:
        for x, y in locations:
            old_position = [coord_dict[(x, y)][0] + str(coord_dict[(x, y)][1])]
            new_points = move(x, y)
            if new_points not in locations and new_points != (-1, -1) and check_if_legal(new_points[0], new_points[1])\
                    and new_points not in opp_loc:
                new_position = [coord_dict[new_points][0] + str(coord_dict[new_points][1])]
                move_notation.append(("I", old_position, new_position))

    # For 2 marbles, if opp only has 1 in line, can move that marble
    # check if there are two marbles in player's hand
    for move in directions:

        for x, y in locations:
            chain = get_chain(move, (x, y), 2, locations)
            opp_chain = get_opp_chain(move, (x, y), opp_loc)

            if len(chain) > len(opp_chain) and len(chain) > 1:
                new_points = move(chain[0][0], chain[0][1])

                new_position = []
                new_opp_position = []
                old_position = []
                old_opp_pos = []

                if new_points not in locations and new_points != (-1, -1) and check_if_legal(new_points[0], new_points[1]):
                    pp = move(chain[0][0], chain[0][1])

                    if pp in opp_chain:

                        # check if pushing against opposite color
                        for i in opp_chain:
                            new_opp_coord = move(i[0], i[1])

                            old_opp_pos.append(coord_dict[i][0] + str(coord_dict[i][1]))
                            if new_opp_coord == (-1, -1):
                                pass
                            else:
                                new_opp_position.append(coord_dict[new_opp_coord][0] + str(coord_dict[new_opp_coord][1]))
                        opp_move_notation.append(("I", old_opp_pos, new_opp_position))

                    for i in chain:
                        new_points = move(i[0], i[1])

                        old_position.append(coord_dict[i][0] + str(coord_dict[i][1]))

                        new_position.append(coord_dict[new_points][0] + str(coord_dict[new_points][1]))
                    move_notation.append(("I", old_position, new_position))

    # For 3 marbles, if opp has 2 or less in line, can move that line
    # check if there are 3 marbles in player's hand
    for move in directions:

        for x, y in locations:

            chain = get_chain(move, (x, y), 3, locations)
            opp_chain = get_opp_chain(move, (x, y), opp_loc)

            if len(chain) > len(opp_chain) and len(chain) > 2:
                new_points = move(chain[0][0], chain[0][1])

                new_position = []
                new_opp_position = []
                old_position = []
                old_opp_pos = []

                if new_points not in locations and new_points != (-1, -1) and check_if_legal(new_points[0],
                                                                                             new_points[1]):
                    pp = move(chain[0][0], chain[0][1])

                    if pp in opp_chain:

                        # check if pushing against opposite color
                        for i in opp_chain:
                            new_opp_coord = move(i[0], i[1])

                            old_opp_pos.append(coord_dict[i][0] + str(coord_dict[i][1]))
                            if new_opp_coord == (-1, -1):
                                pass
                            else:
                                new_opp_position.append(
                                    coord_dict[new_opp_coord][0] + str(coord_dict[new_opp_coord][1]))
                        opp_move_notation.append(("I", old_opp_pos, new_opp_position))

                    for i in chain:
                        new_points = move(i[0], i[1])

                        old_position.append(coord_dict[i][0] + str(coord_dict[i][1]))

                        new_position.append(coord_dict[new_points][0] + str(coord_dict[new_points][1]))
                    move_notation.append(("I", old_position, new_position))

    return move_notation, opp_move_notation


def generate_sidestep(color, location_matrix):
    """
    Generate sidestep notations.
    :param color:
    :param location_matrix:
    :return:
    """
    player = color

    locations = [(ix, iy) for ix, row in enumerate(location_matrix) for iy, i in enumerate(row) if i == player]
    opp_loc = [(ix, iy) for ix, row in enumerate(location_matrix) for iy, i in enumerate(row) if i != player and i != 0]

    move_notation = []

    directions = [move_1, move_3, move_5, move_7, move_9, move_11]

    # for chains of 2
    for move in directions:
        for x, y in locations:
            if move == move_1 or move == move_7:
                chains = [get_left_diag, get_line]
            elif move == move_3 or move == move_9:
                chains = [get_left_diag, get_right_diag]
            elif move == move_5 or move == move_11:
                chains = [get_right_diag, get_line]

            for get_chain in chains:
                chain = get_chain((x, y), 2, locations)

                new_chains = []
                old_moves = []
                if len(chain) > 1:
                    first_move = move(chain[0][0], chain[0][1])
                    second_move = move(chain[1][0], chain[1][1])
                    if (-1, -1) not in [first_move, second_move] and first_move not in locations \
                            and second_move not in locations and first_move not in opp_loc \
                            and second_move not in opp_loc:
                        old_moves.append(coord_dict[chain[0]][0] + str(coord_dict[chain[0]][1]))
                        old_moves.append(coord_dict[chain[1]][0] + str(coord_dict[chain[1]][1]))
                        new_chains.append(coord_dict[first_move][0] + str(coord_dict[first_move][1]))
                        new_chains.append(coord_dict[second_move][0] + str(coord_dict[second_move][1]))
                        move_notation.append(("SS", old_moves, new_chains))
    # for chains of 3
    for move in directions:
        for x, y in locations:
            if move == move_1 or move == move_7:
                chains = [get_left_diag, get_line]
            elif move == move_3 or move == move_9:
                chains = [get_left_diag, get_right_diag]
            elif move == move_5 or move == move_11:
                chains = [get_right_diag, get_line]

            for get_chain in chains:
                chain = get_chain((x, y), 3, locations)

                new_chains = []
                old_moves = []
                if len(chain) > 2:
                    first_move = move(chain[0][0], chain[0][1])
                    second_move = move(chain[1][0], chain[1][1])
                    if (-1, -1) not in [first_move, second_move] and first_move not in locations \
                            and second_move not in locations and first_move not in opp_loc \
                            and second_move not in opp_loc:
                        old_moves.append(coord_dict[chain[0]][0] + str(coord_dict[chain[0]][1]))
                        old_moves.append(coord_dict[chain[1]][0] + str(coord_dict[chain[1]][1]))
                        new_chains.append(coord_dict[first_move][0] + str(coord_dict[first_move][1]))
                        new_chains.append(coord_dict[second_move][0] + str(coord_dict[second_move][1]))
                        move_notation.append(("SS", old_moves, new_chains))
    return move_notation


def get_left_diag(current_coord, num_marbles, location_matrix):
    """
    Finds chains of 2 or 3 according to which side-step they're moving.
    :param current_coord:
    :param num_marbles:
    :param location_matrix:
    :return:
    """
    chain = [current_coord]

    for i in range(num_marbles - 1):
        current_coord = move_5(current_coord[0], current_coord[1])
        if current_coord in location_matrix:
            chain.append(current_coord)
    return chain

def get_right_diag(current_coord, num_marbles, location_matrix):
    """
    Finds chains of 2 or 3 according to which side-step they're moving.
    :param current_coord:
    :param num_marbles:
    :param location_matrix:
    :return:
    """
    chain = [current_coord]

    for i in range(num_marbles - 1):
        current_coord = move_7(current_coord[0], current_coord[1])
        if current_coord in location_matrix:
            chain.append(current_coord)
    return chain


def get_line(current_coord, num_marbles, location_matrix):
    chain = [current_coord]
    for i in range(num_marbles - 1):
        current_coord = move_3(current_coord[0], current_coord[1])
        if current_coord in location_matrix:
            chain.append(current_coord)
    return chain


def get_chain(move, current_coord, num_marbles, location_matrix):
    """
    Finds chains of 2 or 3 according to which direction they are being pushed for current player.
    :param move_type:
    :param current_coord:
    :return:
    """
    chain = [current_coord]

    if move == move_1:
        for i in range(num_marbles - 1):
            current_coord = move_7(current_coord[0], current_coord[1])
            if current_coord in location_matrix:
                chain.append(current_coord)
    elif move == move_3:
        for i in range(num_marbles - 1):
            current_coord = move_9(current_coord[0], current_coord[1])
            if current_coord in location_matrix:
                chain.append(current_coord)
    elif move == move_5:
        for i in range(num_marbles - 1):
            current_coord = move_11(current_coord[0], current_coord[1])
            if current_coord in location_matrix:
                chain.append(current_coord)
    elif move == move_7:
        for i in range(num_marbles - 1):
            current_coord = move_1(current_coord[0], current_coord[1])
            if current_coord in location_matrix:
                chain.append(current_coord)
    elif move == move_9:
        for i in range(num_marbles - 1):
            current_coord = move_3(current_coord[0], current_coord[1])
            if current_coord in location_matrix:
                chain.append(current_coord)
    elif move == move_11:
        for i in range(num_marbles - 1):
            current_coord = move_5(current_coord[0], current_coord[1])
            if current_coord in location_matrix:
                chain.append(current_coord)
    return chain


def get_opp_chain(move, current_coord, location_matrix):
    """
    Return the coordinates of the opposite player's chain of marbles.
    :param move_type:
    :param current_coord:
    :param location_matrix:
    :return:
    """
    opp_chain = []

    next_coord = move(current_coord[0], current_coord[1])

    for i in range(3):
        if next_coord != (-1, -1) and next_coord in location_matrix:
            opp_chain.append(next_coord)
            next_coord = move(next_coord[0], next_coord[1])

    return opp_chain


def check_if_legal(x, y):
    legal = True
    if (x > 8 or x < 0) or (y < 0 or y > 8):
        legal = False
    if (x == 0 or x == 8) and y > 4:
        legal = False
    if (x == 1 or x == 7) and y > 5:
        legal = False
    if (x == 2 or x == 6) and y > 6:
        legal = False
    if (x == 3 or x == 5) and y > 7:
        legal = False
    return legal


# Defining simple moves in each direction
def move_1(x, y):
    new_coord = -1, -1
    point = -1, -1

    if x != 0 and (x, y) != (-1, -1):

        current_coord = coord_dict[(x, y)]
        new_coord = [letter_and_numOffset[x - 1][0], current_coord[1] + 1]
        for key in coord_dict:
            if coord_dict[key] == new_coord:
                point = key
    return point


def move_3(x, y):
    new_coord = -1, -1
    point = -1, -1
    if (x, y + 1) in coord_dict:
        current_coord = coord_dict[(x, y)]
        new_coord = coord_dict[(x, y + 1)]
        for key in coord_dict:
            if coord_dict[key] == new_coord:
                point = key
    return point


def move_5(x, y):
    new_coord = -1, -1
    point = -1, -1
    if x != 8 and (x, y) != (-1, -1):

        current_coord = coord_dict[(x, y)]
        new_coord = [letter_and_numOffset[x + 1][0], current_coord[1]]
        for key in coord_dict:
            if coord_dict[key] == new_coord:
                point = key
    return point


def move_7(x, y):
    new_coord = -1, -1
    point = -1, -1

    if x != 8 and (x, y) != (-1, -1):
        current_coord = coord_dict[(x, y)]
        new_coord = [letter_and_numOffset[x + 1][0], current_coord[1] - 1]
        for key in coord_dict:
            if coord_dict[key] == new_coord:
                point = key
    return point


def move_9(x, y):
    new_coord = -1, -1
    point = -1, -1
    if (x, y - 1) in coord_dict:
        current_coord = coord_dict[(x, y)]
        new_coord = coord_dict[(x, y - 1)]
        for key in coord_dict:
            if coord_dict[key] == new_coord:
                point = key
    return point


def move_11(x, y):
    new_coord = -1, -1
    point = -1, -1
    if x != 0 and (x, y) != (-1, -1):

        current_coord = coord_dict[(x, y)]
        new_coord = [letter_and_numOffset[x - 1][0], current_coord[1]]
        for key in coord_dict:
            if coord_dict[key] == new_coord:
                point = key
    return point


matrix, player_color = get_input("Test1.input")
generate_moves(matrix, player_color)
# show_grid(matrix)

