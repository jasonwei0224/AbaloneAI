import constant
import PySimpleGUI as sg


def get_input(file_name):
    # open the file
    file = open(file_name, "r")
    # get color of user
    player_color = file.readline()
    # set the color to the code
    # White: 1
    # Black: 2
    player_color = 1 if player_color[0] == 'w' else 2
    # read in the marble locations
    locations = file.readline().split(',')
    # start with an empty board
    location_matrix = constant.EMPTY_BOARD

    opp_location = []
    user_location = []

    # update the empty board with the read in data
    for value in locations:
        row = constant.LOCATION_DICT[value[0]]
        col = int(value[1]) - constant.LETTER_AND_NUM_OFFSET[row][1]
        location_matrix[row][col] = 1 if value[2] == 'w' else 2
        user_location.append(value[:2]) if value[2] == 'w' else opp_location.append(value[:2])

    return location_matrix, player_color, user_location, opp_location

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

def draw_board(canvas, matrix):
    """
    This draws the Abalone game board with coordinates listed on each location
    :param matrix: matrix representation of abalone board
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
                canvas.draw_text(
                    '{}'.format(
                        constant.LETTER_AND_NUM_OFFSET[row][0] + str(constant.LETTER_AND_NUM_OFFSET[row][1] + col)),
                    (col * width + 20 + offset, row * width + 15), color="red")
            elif matrix[row][col] == 1:
                canvas.DrawCircle((col * width + 20 + offset, row * width + 15), radius,
                                  fill_color='white')
                canvas.draw_text(
                    '{}'.format(
                        constant.LETTER_AND_NUM_OFFSET[row][0] + str(constant.LETTER_AND_NUM_OFFSET[row][1] + col)),
                    (col * width + 20 + offset, row * width + 15), color="red")
            elif matrix[row][col] == 2:
                canvas.DrawCircle((col * width + 20 + offset, row * width + 15), radius,
                                  fill_color='black')

                canvas.draw_text(
                '{}'.format(constant.LETTER_AND_NUM_OFFSET[row][0] + str(constant.LETTER_AND_NUM_OFFSET[row][1] + col)),
                (col * width + 20 + offset, row * width + 15), color="red")
            else:
                pass
def print_move_detail(moves):
    """
    print list of moves based on move notation with coordinate translate to notation used in class
    :param moves: list of move notation [( move type, [starting coordinates], [end coordinates])]
    :return:
    """
    for i in range(len(moves)):
        origin = ""
        dest = ""
        for coordinate in moves[i][1]:
            origin += coordinates_to_notation(coordinate[0], coordinate[1]) + " "
        for coordinate in moves[i][2]:
            dest += coordinates_to_notation(coordinate[0], coordinate[1]) + " "
        print(moves[i][0] + ": " + str(origin) + " => " + str(dest))

def get_value(s, location_matrix):
    """
    Return the value at the given location
    :param s: The coordinate of the location in stirng E.g. "H4"
    :param location_matrix: matrix representation of abalone board
    :return: the value 1: white, 2: black, 0: empty
    """
    row = int(constant.LOCATION_DICT[s[0]])
    col = int(s[1]) - constant.LETTER_AND_NUM_OFFSET[constant.LOCATION_DICT[s[0]]][1]
    return location_matrix[row][col]

def get_value_row_col(row, col, location_matrix):
    """
    Return the value at the given location
    :param row: int row value of the location
    :param col: int col value of the locaiton
    :param location_matrix: matrix representation of abalone board
    :return: the value 1: white, 2: black, 0: empty
    """
    return location_matrix[row][col]

def get_marble_with_direction(adj_lst, marble, direction):
    """
    get marble from the specified location
    :param adj_lst: the list of marble adjacents
    :param marble: the marble to go from
    :param direction: 1,3,5,7,9 or 11
    :return: the coordinate of marble e.g. I5 with direction = 5 will return H5
    """
    for m in adj_lst[marble]:
        if m[1] == direction:
            adj_marble = m
            return adj_marble[0]

def generate_move_notation(raw_move_notation, adj_lst):
    """
    From a list of raw move notations generate the move notations
    E.g.
    raw_move_notation = [move_type, marble, number of marble to move, direction, push or not]
    :param raw_move_notation: [move_type, marble, number of marble to move, direction, push or not]
    :param adj_lst: the dictionary of adjacent values
    :return: [move_type, [list of origin location], [list of dest location]]
    """
    moves = []

    for move in range(len(raw_move_notation)):
        m = []
        m.append(raw_move_notation[move][0])

        direction = raw_move_notation[move][3]
        if int(raw_move_notation[move][2]) == 1:
            row = notation_to_coordinates(raw_move_notation[move][1])[0]
            col = notation_to_coordinates(raw_move_notation[move][1])[1]
            m.append([(row, col)])
            dest = get_marble_with_direction(adj_lst, raw_move_notation[move][1], direction)
            dest_row = notation_to_coordinates(dest)[0]
            dest_col = notation_to_coordinates(dest)[1]
            m.append([(dest_row, dest_col)])

        elif int(raw_move_notation[move][2]) == 2:
            row = notation_to_coordinates(raw_move_notation[move][1])[0]
            col = notation_to_coordinates(raw_move_notation[move][1])[1]
            second_marble = get_marble_with_direction(adj_lst, raw_move_notation[move][1], direction)
            second_row, second_col = notation_to_coordinates(second_marble)
            m.append([(row, col), (second_row, second_col)])
            dest_marble = get_marble_with_direction(adj_lst,second_marble, direction)
            dest_marble2 = get_marble_with_direction(adj_lst, dest_marble, direction)
            dest_marble_row, dest_marble_col = notation_to_coordinates(dest_marble)
            dest_marble2_row, dest_marble2_col = notation_to_coordinates(dest_marble2)
            m.append([(dest_marble_row, dest_marble_col), (dest_marble2_row, dest_marble2_col)])
        elif int(raw_move_notation[move][2]) == 3:
            row = notation_to_coordinates(raw_move_notation[move][1])[0]
            col = notation_to_coordinates(raw_move_notation[move][1])[1]
            second_marble = get_marble_with_direction(adj_lst, raw_move_notation[move][1], direction)
            second_row, second_col = notation_to_coordinates(second_marble)
            third_marble = get_marble_with_direction(adj_lst,second_marble, direction)
            third_row, third_col = notation_to_coordinates(third_marble)
            m.append([(row, col), (second_row, second_col), (third_row, third_col)])
            dest_marble = get_marble_with_direction(adj_lst, second_marble, direction)
            dest_marble2 = get_marble_with_direction(adj_lst, dest_marble, direction)
            dest_marble3 = get_marble_with_direction(adj_lst, dest_marble2, direction)
            dest_marble_row, dest_marble_col = notation_to_coordinates(dest_marble)
            dest_marble2_row, dest_marble2_col = notation_to_coordinates(dest_marble2)
            dest_marble3_row, dest_marble3_col = notation_to_coordinates(dest_marble3)

            m.append([(dest_marble_row, dest_marble_col), (dest_marble2_row, dest_marble2_col), (dest_marble3_row, dest_marble3_col)])

        moves.append(m)
    return moves


def get_all_locations(row, col, m, n):
    """
    return list of neighbor coordinates
    E.g. I5 will return [I6,H5,H4]
    :param row: int of the row that marble you wanna get its neighbor for
    :param col: int of the col that marble you wanna get its neighbor for
    :param m: N/A
    :param n: lenght of each row
    :return: a  list all location and it's neighbor
    """
    adjacent_lst = []
    if row == 4 and col == 0:
        adjacent_lst.append((coordinates_to_notation(row - 1, col), 1))
        adjacent_lst.append((coordinates_to_notation(row, col + 1), 3))
        adjacent_lst.append((coordinates_to_notation(row + 1, col), 5))

    # when on edge (E.g. E9)
    if row == 4 and col == 8:
        adjacent_lst.append((coordinates_to_notation(row - 1, col - 1), 11))
        adjacent_lst.append((coordinates_to_notation(row + 1, col - 1), 7))
        adjacent_lst.append((coordinates_to_notation(row, col - 1), 9))

    # when on corner (E.g. I5)
    if row == 0 and col == 0:
        adjacent_lst.append((coordinates_to_notation(row + 1, col + 1), 5))
        adjacent_lst.append((coordinates_to_notation(row, col + 1), 3))
        adjacent_lst.append((coordinates_to_notation(row + 1, col), 7))

    # when on corner (E.g. I9)
    if row == 0 and col == 4:
        adjacent_lst.append((coordinates_to_notation(row + 1, col + 1), 5))
        adjacent_lst.append((coordinates_to_notation(row, col - 1), 9))
        adjacent_lst.append((coordinates_to_notation(row + 1, col), 7))

    # when on corner (E.g. A1)
    if row == 8 and col == 0:
        adjacent_lst.append((coordinates_to_notation(row - 1, col + 1), 1))
        adjacent_lst.append((coordinates_to_notation(row - 1, col), 11))
        adjacent_lst.append((coordinates_to_notation(row, col + 1), 3))
    # when on corner (E.g. A5)
    if row == 8 and col == 4:
        adjacent_lst.append((coordinates_to_notation(row - 1, col), 11))
        adjacent_lst.append((coordinates_to_notation(row - 1, col + 1), 1))
        adjacent_lst.append((coordinates_to_notation(row, col - 1), 9))

    # when on edge (E.g. D2, C1, B1)
    if 4 < row < 8 and col == 0:
        adjacent_lst.append((coordinates_to_notation(row - 1, col), 11))
        adjacent_lst.append((coordinates_to_notation(row - 1, col + 1), 1))
        adjacent_lst.append((coordinates_to_notation(row, col + 1), 3))
        adjacent_lst.append((coordinates_to_notation(row + 1, col), 5))

    # when on edge (E.g. B6, C7, D8)
    if 4 < row < 8 and col == n - 1:
        adjacent_lst.append((coordinates_to_notation(row - 1, col), 11))
        adjacent_lst.append((coordinates_to_notation(row + 1, col - 1), 7))
        adjacent_lst.append((coordinates_to_notation(row, col - 1), 9))
        adjacent_lst.append((coordinates_to_notation(row - 1, col + 1), 1))

    # when on edge (E.g. H4, G3, F2)
    if 4 > row > 0 and col == 0:
        adjacent_lst.append((coordinates_to_notation(row + 1, col), 7))
        adjacent_lst.append((coordinates_to_notation(row + 1, col + 1), 5))
        adjacent_lst.append((coordinates_to_notation(row, col + 1), 3))
        adjacent_lst.append((coordinates_to_notation(row - 1, col), 1))

    # when on edge (E.g. G9, F9, H9)
    if 4 > row > 0 and col == n - 1:
        adjacent_lst.append((coordinates_to_notation(row - 1, col - 1), 11))
        adjacent_lst.append((coordinates_to_notation(row, col - 1), 9))
        adjacent_lst.append((coordinates_to_notation(row + 1, col + 1), 5))
        adjacent_lst.append((coordinates_to_notation(row + 1, col), 7))

    # when on edge (E.g. I6, I7, I8)
    if row == 0 and n - 1 > col > 0:
        adjacent_lst.append((coordinates_to_notation(row, col - 1), 9))
        adjacent_lst.append((coordinates_to_notation(row, col + 1), 3))
        adjacent_lst.append((coordinates_to_notation(row + 1, col + 1), 5))
        adjacent_lst.append((coordinates_to_notation(row + 1, col), 7))

    # when on edge (E.g. A2, A3, A4)
    if row == 8 and n - 1 > col > 0:
        adjacent_lst.append((coordinates_to_notation(row, col - 1), 9))
        adjacent_lst.append((coordinates_to_notation(row, col + 1), 3))
        adjacent_lst.append((coordinates_to_notation(row - 1, col + 1), 1))
        adjacent_lst.append((coordinates_to_notation(row - 1, col), 11))

    # when it is in the middle of the abalone board above row 4
    if 0 < row < 4 and 0 < col < n - 1:
        adjacent_lst.append((coordinates_to_notation(row - 1, col), 1))
        adjacent_lst.append((coordinates_to_notation(row - 1, col - 1), 11))
        adjacent_lst.append((coordinates_to_notation(row + 1, col), 7))
        adjacent_lst.append((coordinates_to_notation(row, col - 1), 9))
        adjacent_lst.append((coordinates_to_notation(row + 1, col + 1), 5))
        adjacent_lst.append((coordinates_to_notation(row, col + 1), 3))
    if 4 < row < 8 and 0 < col < n - 1:
        adjacent_lst.append((coordinates_to_notation(row - 1, col), 11))
        adjacent_lst.append((coordinates_to_notation(row - 1, col + 1), 1))
        adjacent_lst.append((coordinates_to_notation(row + 1, col), 5))
        adjacent_lst.append((coordinates_to_notation(row, col - 1), 9))
        adjacent_lst.append((coordinates_to_notation(row + 1, col - 1), 7))
        adjacent_lst.append((coordinates_to_notation(row, col + 1), 3))
    if row == 4 and 0 < col < n - 1:
        adjacent_lst.append((coordinates_to_notation(row - 1, col), 1))
        adjacent_lst.append((coordinates_to_notation(row - 1, col - 1), 11))
        adjacent_lst.append((coordinates_to_notation(row + 1, col), 5))
        adjacent_lst.append((coordinates_to_notation(row, col - 1), 9))
        adjacent_lst.append((coordinates_to_notation(row + 1, col - 1), 7))
        adjacent_lst.append((coordinates_to_notation(row, col + 1), 3))

    return adjacent_lst

def push():
    pass

def generate_inline(location_matrix, adjacent_marble, adj_lst, direction, color, user_lst, opp_lst, count_user,
                    count_opp):

    if count_user > 3 or adjacent_marble is None:
        return
    row = notation_to_coordinates(adjacent_marble)[0]
    col = notation_to_coordinates(adjacent_marble)[1]

    if location_matrix[row][col] == 0:
        if count_user > count_opp and count_user == 1:
            return count_user, direction, 'I'
        elif count_user > count_opp and count_user > 1 and count_opp > 0:
            return  count_user, direction, 'P'
        elif count_user > count_opp:
            return count_user, direction, 'I'

    elif adjacent_marble in opp_lst:
        adj_marble = get_marble_with_direction(adj_lst, adjacent_marble, direction)
        return generate_inline(location_matrix, adj_marble, adj_lst, direction, color, user_lst, opp_lst, count_user,
                               count_opp + 1)

    elif adjacent_marble in user_lst:

        adj_marble = get_marble_with_direction(adj_lst, adjacent_marble, direction)
        return generate_inline(location_matrix, adj_marble, adj_lst, direction, color,
                               user_lst, opp_lst,
                               count_user + 1, count_opp)

def generate_move(location_matrix, color, user_lst, opp_lst):
    loc = {}
    for row in range(len(location_matrix)):
        for col in range(len(location_matrix[row])):
            loc[coordinates_to_notation(row, col)] = get_all_locations(row, col, len(location_matrix),
                                                                       len(location_matrix[row]))
    raw_move_notation = []
    # for key in loc.keys():
    #     for value in loc[key]:
    #         row = notation_to_coordinates(value[0])[0]
    #         col = notation_to_coordinates(value[0])[1]
    #         key_row = notation_to_coordinates(key)[0]
    #         key_col = notation_to_coordinates(key)[1]
    #         if location_matrix[key_row][key_col] == color or location_matrix[row][col] == 0 and location_matrix[row][
    #             col] == color:
    #             direction = generate_inline(location_matrix, value[0], loc, value[1], color, user_lst, opp_lst, 1, 0)
    #             if direction is not None:
    #                 # move type, move marble, number of marble to move, direction to move
    #                 raw_move_notation.append(["I", key, direction[0], direction[1], direction[2]])
    #                 # print("I " + key + " "+ str(direction[1]) + "num of marbles " + str(direction[0]))
    # generate_move_notation(raw_move_notation, loc)
    print(loc['A1'])
    parsed = []
    for key in loc.keys():

        for value in loc[key]:
            row = notation_to_coordinates(value[0])[0]
            col = notation_to_coordinates(value[0])[1]
            key_row = notation_to_coordinates(key)[0]
            key_col = notation_to_coordinates(key)[1]
            if location_matrix[key_row][key_col] == color and location_matrix[row][col] == color\
                    and value[0] not in parsed:
                parsed.append(key)

                move = generate_side_step(key, location_matrix, loc, color, parsed)
                # if move is not None:
                #     print("SS", key, move)

def generate_side_step(marble, location_matrix, adj_lst, color, parsed):
    dir_available = []
    marbles_to_move = []
    moves = []
    type = 'SS'
    for m in adj_lst[marble]:
        dir_available.append(m[1])

    # print(parsed)
    # print(marble, adj_lst[marble])
    for marbles in adj_lst[marble]:

         if get_value(marbles[0], location_matrix) == color and get_value(marbles[0], location_matrix) != None:

            if marbles[1] == 3 and 3 in dir_available:
                dir_available.remove(3)
                if 9 in dir_available:
                    dir_available.remove(9)
            if marbles[1] == 9 and 9 in dir_available:
                dir_available.remove(9)
                if 3 in dir_available:
                    dir_available.remove(3)
            if marbles[1] == 5 and 5 in dir_available:
                dir_available.remove(5)
                if 11 in dir_available:
                    dir_available.remove(11)
            if marbles[1] == 11 and 11 in dir_available:
                dir_available.remove(11)
                if 5 in dir_available:
                    dir_available.remove(5)
            if marbles[1] == 1 and 1 in dir_available:
                dir_available.remove(1)
                if 7 in dir_available:
                    dir_available.remove(7)
            if marbles[1] == 7 and 7 in dir_available:
                dir_available.remove(7)
                if 1 in dir_available:
                    dir_available.remove(1)

            if (marbles[0] not in parsed):
                print(marbles[0], parsed)
                # print(marbles[0] not in parsed)
                # print(marbles, adj_lst[marble], "parsed list ", parsed, "cur ", marble, "adj ", marbles[0], marbles[0] not in parsed)
                # print("cur ", marble, "adj ", marbles[0], marbles[0] in parsed)
                # print(parsed)
                marbles_to_move.append([marble, marbles[0]])
                # print(marbles_to_move)
                # dir_available.remove(marbles[1])

    for dir in dir_available:
        for m in marbles_to_move:
            row, col = notation_to_coordinates(m[0])
            row2, col2 = notation_to_coordinates(m[1])

            if row < 4 and row2 < 4:
                if dir == 1:
                    if col == len(location_matrix[row])-1 or col2 == len(location_matrix[row2])-1:
                        pass
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row-1, col), (row2-1, col2)]])
                if dir == 3:
                    moves.append(['SS', [(row, col), (row2, col2)], [(row, col+1), (row2, col2+1)]])
                if dir == 5:
                    moves.append(['SS', [(row, col), (row2, col2)], [(row+1, col+1), (row2+1, col2+1)]])
                if dir == 7:
                    if col == 0 and col2 == 0:
                        pass
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row+1, col), (row2+1, col2)]])
                if dir == 9:
                    moves.append(['SS', [(row, col), (row2, col2)], [(row, col-1), (row2, col2-1)]])
                if dir == 11:
                    moves.append(['SS', [(row, col), (row2, col2)], [(row - 1, col-1), (row2 - 1, col2-1)]])
            if row > 4 and row2 > 4 and row2 < 8:
                if dir == 1:
                    moves.append(['SS', [(row, col), (row2, col2)], [(row-1, col+1), (row2-1, col2+1)]])
                if dir == 3:
                    if col == len(location_matrix[row]) - 1 or col2 == len(location_matrix[row2]) - 1:
                        pass
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row, col+1), (row2, col2+1)]])
                if dir == 5:
                    if col == len(location_matrix[row])-1 or col2 == len(location_matrix[row2])-1:
                        pass
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row+1, col), (row2+1, col2)]])
                if dir == 7:
                     moves.append(['SS', [(row, col), (row2, col2)], [(row+1, col-1), (row2+1, col2-1)]])
                if dir == 9:
                    if col == 0 or col2 ==0:
                        pass
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row, col-1), (row2, col2-1)]])
                if dir == 11:
                    moves.append(['SS', [(row, col), (row2, col2)], [(row - 1, col), (row2 - 1, col2)]])
            if row == 4 or row2 == 4:
                if dir == 1:
                    if col ==0 and col2 ==0:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row-1, col), (row2-1, col2+1)]])
                    elif row ==5 or row2 == 5:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row - 1, col), (row2 - 1, col2+1)]])
                    elif col == len(location_matrix[row]) - 1 or col2 == len(location_matrix[row2]) - 1:
                        pass
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row - 1, col), (row2 - 1, col2)]])
                if dir == 3:
                    if col == len(location_matrix[row]) - 1 or col2 == len(location_matrix[row2]) - 1:
                        pass
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row, col+1), (row2, col2+1)]])
                if dir == 5:
                    if row == 4and row2 ==4 and col != len(location_matrix[row]) - 1 and col2 != len(location_matrix[row2]) - 1:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row + 1, col), (row2 + 1, col2)]])
                    elif row == 5 or row2 == 5:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row +1, col), (row2 + 1, col2)]])
                    elif col == len(location_matrix[row]) - 1 or col2 == len(location_matrix[row2]) - 1:
                        pass
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row+1, col+1), (row2+1, col2)]])
                if dir == 7:
                    if row == 4 and row2 == 4 and col == len(location_matrix[row]) - 1 or col2 == len(location_matrix[row2]) - 1:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row + 1, col - 1), (row2 + 1, col2 - 1)]])
                    elif row == 5 or row2 == 5:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row+1, col-1), (row2+1, col2-1)]])
                    elif col == len(location_matrix[row]) - 1 or col2 == len(location_matrix[row2]) - 1:
                        pass
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row+1, col), (row2+1, col2-1)]])
                if dir == 9:
                    if row == 5 or row2 == 5 and col ==0 or col2 ==0:
                        pass
                    else:
                       moves.append(['SS', [(row, col), (row2, col2)], [(row, col-1), (row2, col2-1)]])
                if dir == 11:
                    if row == 5 or row2 == 5:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row - 1, col-1), (row2 - 1, col2)]])
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row - 1, col-1), (row2 - 1, col2-1)]])

            if row2 == 8 or row == 8:
                if dir == 1:
                    moves.append(['SS', [(row, col), (row2, col2)], [(row - 1, col + 1), (row2 - 1, col2 + 1)]])
                if dir == 3:
                    if col == len(location_matrix[row]) - 1 or col2 == len(location_matrix[row2]) - 1:
                        pass
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row, col + 1), (row2, col2 + 1)]])
                if dir == 5:
                    # print(col, col2)
                    if row2 == 8 or row == 8:
                        # print('s')
                        pass
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row + 1, col), (row2 + 1, col2)]])
                if dir == 7:
                    pass
                    # moves.append(['SS', [(row, col), (row2, col2)], [(row + 1, col - 1), (row2 + 1, col2 - 1)]])
                if dir == 9:
                    if col == 0 or col2 == 0:
                        pass
                    else:
                        moves.append(['SS', [(row, col), (row2, col2)], [(row, col - 1), (row2, col2 - 1)]])
                if dir == 11:
                    moves.append(['SS', [(row, col), (row2, col2)], [(row - 1, col), (row2 - 1, col2)]])


    # print(dir_available)
    # print(marbles_to_move)
    # print(moves)
    print_move_detail(moves)





def generate_new_board(location_matrix, moves):

    for m in moves:
        type = m[0]
        origin = m[1]
        destination = m[2]

        # if side step we just directly update the board
        if type == "SS":
            for coord in destination:
                location_matrix[coord[0]][coord[1]] = location_matrix[origin[0][0]][origin[0][1]]
            for coord in origin:
                location_matrix[coord[0]][coord[1]] = 0
        if type == "I":
            # if not empty then need to push might need the direction to push to?

            # if empty move directly

            pass


    pass


def show_grid(location_matrix):
    graph_element = sg.Graph((600, 600), (0, 300), (300, 0), key='graph')
    window = sg.Window('Abalone', [[graph_element]], font=('arial', 15)).Finalize()
    canvas = window['graph']
    draw_board(canvas, location_matrix)
    generate_move(location_matrix, color, user_lst, opp_lst)
    event, values = window.read()


matrix, color, user_lst, opp_lst = get_input("Test3.input")
show_grid(matrix)