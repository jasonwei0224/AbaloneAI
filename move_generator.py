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

    # update the empty board with the read in data
    for value in locations:
        row = constant.LOCATION_DICT[value[0]]
        col = int(value[1]) - constant.LETTER_AND_NUM_OFFSET[row][1]
        location_matrix[row][col] = 1 if value[2] == 'w' else 2

    return location_matrix, player_color


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

            elif matrix[row][col] == 1:
                canvas.DrawCircle((col * width + 20 + offset, row * width + 15), radius,
                                  fill_color='white')

            elif matrix[row][col] == 2:
                canvas.DrawCircle((col * width + 20 + offset, row * width + 15), radius,
                                  fill_color='black')

            canvas.draw_text(
                '{}'.format(constant.LETTER_AND_NUM_OFFSET[row][0] + str(constant.LETTER_AND_NUM_OFFSET[row][1] + col)),
                (col * width + 20 + offset, row * width + 15), color="red")


def show_grid(location_matrix):
    graph_element = sg.Graph((600, 600), (0, 300), (300, 0), key='graph')
    window = sg.Window('Abalone', [[graph_element]], font=('arial', 15)).Finalize()
    canvas = window['graph']
    draw_board(canvas, location_matrix)
    generate_moves(location_matrix, color)
    event, values = window.read()


def coordinates_to_notation(row, col):
    return str(constant.LETTER_AND_NUM_OFFSET[row][0]) + str(col + constant.LETTER_AND_NUM_OFFSET[row][1])


def notation_to_coordinates(s):
    return (
        int(constant.LOCATION_DICT[s[0]]), int(s[1]) - constant.LETTER_AND_NUM_OFFSET[constant.LOCATION_DICT[s[0]]][1])


def generate_single_marble_move(location_matrix, location):
    move = 'S'
    moves = []

    # when on edge (E.g. E1)
    if location[0] == 4 and location[1] == 0:
        if location_matrix[location[0] - 1][location[1]] == 0:
            # print([location[0] - 1], [location[1]])
            moves.append((move, location, (location[0] - 1, location[1])))
        if location_matrix[location[0] + 1][location[1]] == 0:
            # print([location[0] + 1], [location[1]])
            moves.append((move, location, (location[0] + 1, location[1])))
        if location_matrix[location[0]][location[1] + 1] == 0:
            # print([location[0]], [location[1] + 1])
            moves.append((move, location, (location[0], location[1] + 1)))

    # when on edge (E.g. E9)
    if location[0] == 4 and location[1] == 8:
        if location_matrix[location[0] - 1][location[1] - 1] == 0:
            # print([location[0] - 1], [location[1] - 1])
            moves.append((move, location, (location[0] - 1, location[1] - 1)))
        if location_matrix[location[0] + 1][location[1] - 1] == 0:
            # print([location[0] + 1], [location[1] - 1])
            moves.append((move, location, (location[0] + 1, location[1] - 1)))
        if location_matrix[location[0]][location[1] - 1] == 0:
            # print([location[0]], [location[1] - 1])
            moves.append((move, location, (location[0], location[1] - 1)))

    # when on corner (E.g. I5)
    if location[0] == 0 and location[1] == 0:
        if location_matrix[location[0] + 1][location[1] + 1] == 0:
            # print([location[0] + 1], [location[1] + 1])
            moves.append((move, location, (location[0] + 1, location[1] + 1)))
        if location_matrix[location[0]][location[1] + 1] == 0:
            # print([location[0]], [location[1] + 1])
            moves.append((move, location, (location[0], location[1] + 1)))
        if location_matrix[location[0] + 1][location[1]] == 0:
            # print([location[0] + 1], [location[1]])
            moves.append((move, location, (location[0] + 1, location[1])))

    # when on corner (E.g. I9)
    if location[0] == 0 and location[1] == 4:
        if location_matrix[location[0] + 1][location[1] + 1] == 0:
            print([location[0] + 1], [location[1] + 1])
            moves.append((move, location, (location[0] + 1, location[1] + 1)))
        if location_matrix[location[0]][location[1] - 1] == 0:
            print([location[0]], [location[1] - 1])
            moves.append((move, location, (location[0], location[1] - 1)))
        if location_matrix[location[0] + 1][location[1]] == 0:
            print([location[0] + 1], [location[1]])
            moves.append((move, location, (location[0] + 1, location[1])))

    # when on corner (E.g. A1)
    if location[0] == 8 and location[1] == 0:
        if location_matrix[location[0] - 1][location[1] + 1] == 0:
            # print([location[0] - 1], [location[1] + 1])
            moves.append((move, location, (location[0] - 1, location[1] + 11)))
        if location_matrix[location[0] - 1][location[1]] == 0:
            # print([location[0] - 1], [location[1]])
            moves.append((move, location, (location[0] - 1, location[1])))
        if location_matrix[location[0]][location[1] + 1] == 0:
            # print([location[0]], [location[1] + 1])
            moves.append((move, location, (location[0], location[1] + 1)))

    # when on corner (E.g. A5)
    if location[0] == 8 and location[1] == 4:
        if location_matrix[location[0] - 1][location[1]] == 0:
            # print([location[0] - 1], [location[1]])
            moves.append((move, location, (location[0] - 1, location[1])))
        if location_matrix[location[0] - 1][location[1] + 1] == 0:
            # print([location[0] - 1], [location[1] + 1])
            moves.append((move, location, (location[0] - 1, location[1] + 1)))
        if location_matrix[location[0]][location[1] - 1] == 0:
            # print([location[0]], [location[1] - 1])
            moves.append((move, location, (location[0], location[1] - 1)))

    # when on edge (E.g. D2, C1, B1)
    if 4 < location[0] < 8 and location[1] == 0:
        if location_matrix[location[0] - 1][location[1]] == 0:
            # print([location[0] - 1], [location[1]])
            moves.append((move, location, (location[0] - 1, location[1])))
        if location_matrix[location[0] - 1][location[1] + 1] == 0:
            # print([location[0] - 1], [location[1] + 1])
            moves.append((move, location, (location[0] - 1, location[1] + 1)))
        if location_matrix[location[0]][location[1] + 1] == 0:
            # print([location[0]], [location[1] + 1])
            moves.append((move, location, (location[0], location[1] + 1)))
        if location_matrix[location[0] + 1][location[1]] == 0:
            # print([location[0] + 1], [location[1]])
            moves.append((move, location, (location[0] + 1, location[1])))

    # when on edge (E.g. B6, C7, D8)
    if 4 < location[0] < 8 and location[1] == len(location_matrix[location[0]]) - 1:
        if location_matrix[location[0] - 1][location[1]] == 0:
            # print([location[0] - 1], [location[1]])
            moves.append((move, location, (location[0] - 1, location[1])))
        if location_matrix[location[0] - 1][location[1] - 1] == 0:
            # print([location[0] - 1], [location[1] - 1])
            moves.append((move, location, (location[0] - 1, location[1] - 1)))
        if location_matrix[location[0]][location[1] - 1] == 0:
            # print([location[0]], [location[1] - 1])
            moves.append((move, location, (location[0], location[1] - 1)))
        if location_matrix[location[0] - 1][location[1] + 1] == 0:
            # print([location[0] - 1], [location[1] + 1])
            moves.append((move, location, (location[0] - 1, location[1] + 1)))

    # when on edge (E.g. H4, G3, F2)
    if 4 > location[0] > 0 and location[1] == 0:
        if location_matrix[location[0] + 1][location[1]] == 0:
            # print([location[0] + 1], [location[1]])
            moves.append((move, location, (location[0] + 1, location[1])))
        if location_matrix[location[0] + 1][location[1] + 1] == 0:
            # print([location[0] + 1], [location[1] + 1])
            moves.append((move, location, (location[0] + 1, location[1] + 1)))
        if location_matrix[location[0]][location[1] + 1] == 0:
            # print([location[0]], [location[1] + 1])
            moves.append((move, location, (location[0], location[1] + 1)))
        if location_matrix[location[0] - 1][location[1]] == 0:
            # print([location[0] - 1], [location[1]])
            moves.append((move, location, (location[0] - 1, location[1])))

    # when on edge (E.g. G9, F9, H9)
    if 4 > location[0] > 0 and location[1] == len(location_matrix[location[0]]) - 1:
        if location_matrix[location[0] - 1][location[1] - 1] == 0:
            # print([location[0] - 1], [location[1] - 1])
            moves.append((move, location, (location[0] - 1, location[1] - 1)))
        if location_matrix[location[0]][location[1] - 1] == 0:
            # print([location[0]], [location[1] - 1])
            moves.append((move, location, (location[0], location[1] - 1)))
        if location_matrix[location[0] + 1][location[1] + 1] == 0:
            # print([location[0] + 1], [location[1] + 1])
            moves.append((move, location, (location[0] + 1, location[1] + 1)))
        if location_matrix[location[0] + 1][location[1]] == 0:
            # print([location[0] + 1], [location[1]])
            moves.append((move, location, (location[0] + 1, location[1])))

    # when on edge (E.g. I6, I7, I8)
    if location[0] == 0 and len(location_matrix[location[0]]) - 1 > location[1] > 0:
        if location_matrix[location[0]][location[1] - 1] == 0:
            # print([location[0]], [location[1] - 1])
            moves.append((move, location, (location[0], location[1] - 1)))
        if location_matrix[location[0]][location[1] + 1] == 0:
            # print([location[0]], [location[1] + 1])
            moves.append((move, location, (location[0], location[1] + 1)))
        if location_matrix[location[0] + 1][location[1] + 1] == 0:
            # print([location[0] + 1], [location[1] + 1])
            moves.append((move, location, (location[0] + 1, location[1] + 1)))
        if location_matrix[location[0] + 1][location[1]] == 0:
            # print([location[0] + 1], [location[1]])
            moves.append((move, location, (location[0] + 1, location[1])))

    # when on edge (E.g. A2, A3, A4)
    if location[0] == 8 and len(location_matrix[location[0]]) - 1 > location[1] > 0:
        if location_matrix[location[0]][location[1] - 1] == 0:
            # print([location[0]], [location[1] - 1])
            moves.append((move, location, (location[0], location[1] - 1)))
        if location_matrix[location[0]][location[1] + 1] == 0:
            # print([location[0]], [location[1] + 1])
            moves.append((move, location, (location[0], location[1] + 1)))
        if location_matrix[location[0] - 1][location[1] + 1] == 0:
            # print([location[0] - 1], [location[1] + 1])
            moves.append((move, location, (location[0] - 1, location[1] + 1)))
        if location_matrix[location[0] - 1][location[1]] == 0:
            # print([location[0] - 1], [location[1]])
            moves.append((move, location, (location[0] - 1, location[1])))

    # when it is in the middle
    if 0 < location[0] < 8 and 0 < location[1] < len(location_matrix[location[0]]) - 1:
        if location_matrix[location[0] - 1][location[1]] == 0:
            # print([location[0] - 1], [location[1]])
            moves.append((move, location, (location[0] - 1, location[1])))
        if location_matrix[location[0] - 1][location[1] - 1] == 0:
            # print([location[0] - 1], [location[1] - 1])
            moves.append((move, location, (location[0] - 1, location[1] - 1)))
        if location_matrix[location[0] + 1][location[1]] == 0:
            # print([location[0] + 1], [location[1] + 1])
            moves.append((move, location, (location[0] + 1, location[1])))
        if location_matrix[location[0]][location[1] - 1] == 0:
            # print([location[0]], [location[1] - 1])
            moves.append((move, location, (location[0], location[1] - 1)))
        if location_matrix[location[0] + 1][location[1] + 1] == 0:
            # print([location[0] + 1], [location[1] + 1])
            moves.append((move, location, (location[0] + 1, location[1] - 1)))
        if location_matrix[location[0]][location[1] + 1] == 0:
            # print([location[0]], [location[1] + 1])
            moves.append((move, location, (location[0], location[1] + 1)))

    return moves

def generate_side_step_three_marbles(location_matrix, color):
    pass

def generate_side_step_two_marbles(location_matrix, color):
    move_lst = []  # (move type, [start locations], [end locations])
    move = "SS"

    # This only check diagonal two marbles NW/SW

    # This only check diagonal two marbles NE/SW


    # This check the horizontal of two marbles
    row = 0
    while row < len(location_matrix):
        col = 0
        while col < len(location_matrix[row]):
            location = (row, col)

            if location_matrix[row][col] == color and location_matrix[row][col + 1] == color:
                # this mean it's second to last only two can be make
                if row == 0:
                    if location_matrix[row + 1][col + 2] == 0 and location_matrix[row + 1][col + 1] == 0:  # SE

                        move_lst.append((move, [location, (row, col + 1)], [(row + 1, col + 1), (row + 1, col + 2)]))
                    if location_matrix[row + 1][col] == 0 and location_matrix[row + 1][col] == 0:  # SW
                        move_lst.append((move, [location, (row, col + 1)], [(row + 1, col), (row + 1, col + 1)]))
                    col += 2

                if row == 8:
                    if location_matrix[row - 1][col + 1] == 0 and location_matrix[row - 1][col + 2] == 0:  # NE
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row - 1, col + 1), (row - 1, col + 2)]))
                    if location_matrix[row - 1][col] == 0 and location_matrix[row - 1][col + 1] == 0:  # NW
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row - 1, col), (row - 1, col + 1)]))
                    col += 2

                if 0 < row < 4:
                    if col == 0 and location_matrix[row + 1][col] == 0 and location_matrix[row + 1][col + 1] == 0:
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row + 1, col), (row + 1, col + 1)]))
                        print(coordinates_to_notation(row + 1, col), coordinates_to_notation(row + 1, col + 1))
                    if location_matrix[row + 1][col + 1] == 0 and location_matrix[row + 1][col + 2] == 0:  # SE
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row + 1, col + 1), (row + 1, col + 2)]))
                        print(coordinates_to_notation(row + 1, col + 1), coordinates_to_notation(row + 1, col + 2))
                    if not col == 0 and location_matrix[row + 1][col] == 0 and location_matrix[row + 1][
                        col + 1] == 0:  # SW
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row + 1, col), (row + 1, col + 1)]))
                        print(coordinates_to_notation(row + 1, col), coordinates_to_notation(row + 1, col + 1))
                    if not col == 0 and location_matrix[row - 1][col - 1] == 0 and location_matrix[row - 1][
                        col] == 0:  # NE
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row - 1, col - 1), (row - 1, col)]))
                        print(coordinates_to_notation(row - 1, col - 1), coordinates_to_notation(row - 1, col))
                    if not col == len(location_matrix[row]) - 2 and location_matrix[row - 1][col - 1] == 0 and \
                            location_matrix[row - 1][col] == 0:  # NW only available in the middle of board
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row - 1, col), (row - 1, col + 1)]))
                        print(coordinates_to_notation(row - 1, col), coordinates_to_notation(row - 1, col + 1))
                    col += 2
                if 4 < row < 8:
                    if location_matrix[row - 1][col + 1] == 0 and location_matrix[row - 1][col + 2] == 0:  # NE
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row - 1, col + 1), (row - 1, col + 2)]))
                        print(coordinates_to_notation(row - 1, col + 1), coordinates_to_notation(row - 1, col + 2))
                    if not col == 0 and location_matrix[row - 1][col] == 0 and location_matrix[row - 1][
                        col + 1] == 0:  # NW
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row - 1, col), (row - 1, col + 1)]))
                        print(coordinates_to_notation(row - 1, col), coordinates_to_notation(row - 1, col + 1))
                    if not col == 0 and location_matrix[row + 1][col - 1] == 0 and location_matrix[row + 1][
                        col] == 0:  # SW
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row + 1, col - 1), (row + 1, col)]))
                        print(coordinates_to_notation(row + 1, col - 1), coordinates_to_notation(row + 1, col))
                    if not col == len(location_matrix[row]) - 2 and location_matrix[row + 1][col] == 0 and \
                            location_matrix[row + 1][col + 1] == 0:  # NW only available in the middle of board
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row + 1, col), (row + 1, col + 1)]))
                        print(coordinates_to_notation(row + 1, col), coordinates_to_notation(row + 1, col + 1))
                    col += 2
                if row == 4:
                    print(col)
                    if not col == len(location_matrix[row]) - 2 and location_matrix[row - 1][col] == 0 and \
                            location_matrix[row - 1][col + 1] == 0:  # NE
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row - 1, col), (row - 1, col + 1)]))
                        print(coordinates_to_notation(row - 1, col), coordinates_to_notation(row - 1, col + 1))
                    if not col == 0 and location_matrix[row - 1][col - 1] == 0 and location_matrix[row - 1][
                        col] == 0:  # NW
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row - 1, col - 1), (row - 1, col)]))
                        print(coordinates_to_notation(row - 1, col - 1), coordinates_to_notation(row - 1, col))
                    if not col == 0 and location_matrix[row + 1][col - 1] == 0 and location_matrix[row + 1][
                        col] == 0:  # SW
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row + 1, col - 1), (row + 1, col)]))
                        print(coordinates_to_notation(row + 1, col - 1), coordinates_to_notation(row + 1, col))
                    if not col == len(location_matrix[row]) - 2 and location_matrix[row + 1][col] == 0 and \
                            location_matrix[row + 1][col + 1] == 0:  # SE
                        move_lst.append(
                            (move, [location, (row, col + 1)], [(row + 1, col), (row + 1, col + 2)]))
                        print(coordinates_to_notation(row + 1, col), coordinates_to_notation(row + 1, col + 1))
                    col += 2
            else:
                col += 1
        row += 1
    return move_lst


def check_in_line(location_matrix, location, num_of_marble, direction):
    pass


def generate_new_board(location_matrix, moves):
    # generate new board based on provided moves
    pass


def generate_moves(location_matrix, color):
    color_location = []
    for row in range(len(location_matrix)):
        for col in range(len(location_matrix[row])):
            if location_matrix[row][col] == color:
                color_location.append((row, col))
    moves = []

    # for coordinate in color_location:
    #     m = check_single_marble_move(location_matrix, coordinate)
    #     for n in m:
    #         moves.append(n)
    print(color_location)

    # generate ss two marbles
    # Need to find two clusters
    m = generate_side_step_two_marbles(location_matrix, color)
    for n in m:
        moves.append(n)
    # print(moves)
    # print(len(moves))

    # generate ss three marbles

    # generate inline two marbles

    # generate inline three marbles

    pass


matrix, color = get_input("Test3.input")
show_grid(matrix)
