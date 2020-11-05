import constant
import PySimpleGUI as sg
# import gui

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

    return location_matrix

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

def show_grid(location_matrix,):
    graph_element = sg.Graph((600, 600), (0, 300), (300, 0), key='graph')
    window = sg.Window('Abalone', [[graph_element]], font=('arial', 15)).Finalize()
    draw_board(graph_element, location_matrix)
    event, values = window.read()

def generate_moves():
    pass


matrix = get_input("Test1.input")
show_grid(matrix)