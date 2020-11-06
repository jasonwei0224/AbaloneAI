import PySimpleGUI as sg
import constant

# List of options for user to choose from
board_choice = ['Standard', 'German Daisy', 'Belgian Daisy']
player_color = ['Black', 'White']
game_mode = ["human vs human", "human vs computer"]

# based on the board representation given in class change the letter to the row it represents (starting at
# row 0)
location_dict = {"I": 0, "H": 1, "G": 2, "F": 3, "E": 4, "D": 5, "C": 6, "B": 7, "A": 8}

# from the row number get the letter and the offset of the number for each location
letter_and_numOffset = {0: ('I', 5), 1: ('H', 4), 2: ('G', 3), 3: ('F', 2), 4: ('E', 1), 5: ('D', 1), 6: ('C', 1),
                        7: ('B', 1), 8: ('A', 1)}

# Configuration window layout
config_layout = [[sg.Text('Select Initial Board Layout', text_color="yellow")],
                 [sg.Radio(board, 1, default=True, key=str(board)) if board == 'Standard' else sg.Radio(board, 1,
                                                                                                        key=str(board))
                  for board in
                  board_choice],
                 [sg.VerticalSeparator(pad=((0, 0), (10, 20)))],
                 [sg.Text('Select Player Color', text_color="yellow")],
                 [sg.Radio(color, 2, default=True, key="Black") if color == 'Black' else sg.Radio(color, 2, key='White')
                  for color in
                  player_color],
                 [sg.VerticalSeparator(pad=((0, 0), (10, 20)))],
                 [sg.Text('Select Game Mode', text_color="yellow")],
                 [sg.Radio(mode, 3, default=True, key=str(mode)) for mode in game_mode],
                 [sg.VerticalSeparator(pad=((0, 0), (10, 20)))],
                 [sg.Text('Set number of moves per player per game:'),
                  sg.Spin([i for i in range(1, 11)], initial_value=15, key="max_moves")],
                 [sg.VerticalSeparator(pad=((0, 0), (10, 20)))],
                 [sg.Text('Set player 1 (human) time limit for a move limit (s)'),
                  sg.Spin([i for i in range(1, 11)], initial_value=1, key="p1_time_limit")],
                 [sg.VerticalSeparator(pad=((0, 0), (10, 20)))],
                 [sg.Text('Set player 2 (computer/human) time limit for a move  (s)'),
                  sg.Spin([i for i in range(1, 11)], initial_value=1, key="p2_time_limit")],
                 [sg.OK("Start", pad=((10, 0), (50, 10))), sg.Cancel("Exit", pad=((20, 0), (50, 10)))]]


# The layout for the game information including the canvas showing Abalone game board

def generate_game_info_layout(player1_color, player2_color):
    game_info_layout = [[sg.Button('Play'), sg.Button('Pause'), sg.Button('Stop'), sg.Button('Undo')],
                        [sg.VerticalSeparator(pad=((0, 0), (10, 20)))],
                        [sg.InputText("Please Enter your move", key='move'), sg.Button("Submit")],
                        [sg.Text('Next Move: ....'), ],
                        [sg.VerticalSeparator(pad=((0, 0), (10, 20)))],
                        [sg.Text('Player 1: 0'),
                         sg.Text('Player 1 color: ' + ("White" if player1_color == 1 else "Black"))],
                        [sg.Text('Player 2: 0'),
                         sg.Text('Player 2 color: ' + ("Black" if player2_color == 2 else "White"))],
                        [sg.Text('Time Taken by Player 1:   ')],
                        [sg.Text('Time Taken by Player 2:  ')],
                        [sg.VerticalSeparator(pad=((0, 0), (10, 20)))],
                        [sg.Text('Moves Taken by Player 1:   ', pad=((0, 50), (0, 0))),
                         sg.Text('Moves Taken by Player 2: ')],
                        [sg.Multiline('Moves Taken by Player 1:   ', size=(25, 10)),
                         sg.Multiline('Moves Taken by Player 2: ', size=(25, 10))],
                        ]

    return game_info_layout


def draw_board(canvas, matrix):
    """
    This draws the Abalone game board with coordinates listed on each location
    :param matrix: matrix representation of the abalone board
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
                '{}'.format(letter_and_numOffset[row][0] + str(letter_and_numOffset[row][1] + col)),
                (col * width + 20 + offset, row * width + 15), color="red")


def validate_input(move_str):
    # Need to implement
    pass


def update_board(move_str):
    # Get the starting row, column and ending row, column of a marble
    # Currently only work with moving single marble
    start_row = location_dict[move[0]]
    start_col = int(move[1]) - start_row
    end_row = location_dict[move[3]]
    end_col = int(move[4]) - end_row

    # update the Abalone representation of the board
    selected_board[end_row][end_col + start_row] = selected_board[start_row][start_col]
    selected_board[start_row][start_col] = 0


window = sg.Window('Game Configuration', config_layout, font=('arial', 15))

event, values = window.read()

if event == "Exit":
    window.close()
elif event == 'Start':

    # Get the initial board layout
    if window["Standard"].Get():
        selected_board = constant.DEFAULT_BOARD
    elif window["German Daisy"].Get():
        selected_board = constant.GERMAN_BOARD
    elif window["Belgian Daisy"].Get():
        selected_board = constant.BELGIAN_BOARD
    else:
        selected_board = constant.DEFAULT_BOARD

    # Get the player color
    # White = 1
    # Black = 2
    if window["Black"].Get():
        player1_color = 2
        player2_color = 1
    elif window["White"].Get():
        player1_color = 1
        player2_color = 2
    else:
        player1_color = 2
        player2_color = 1

    if window["human vs human"].Get():
        game_mode = "human"
    else:
        game_mode = "comp"

    # Get the max moves and time limit for each player
    max_moves = window["max_moves"].Get()
    p1_time_limit = window["p1_time_limit"].Get()
    p2_time_limit = window["p2_time_limit"].Get()

    window.close()  # Close the configuration window

    # the graph element that the board will be drawn on
    graph_element = sg.Graph((600, 600), (0, 300), (300, 0), key='graph')

    game_layout = [[graph_element, sg.Column(generate_game_info_layout(player1_color, player2_color))]]
    # Create the game window
    window2 = sg.Window('Abalone', game_layout, font=('arial', 15)).Finalize()
    # get the canvas to be drawn on
    canvas = window2['graph']
    # Draw the board
    draw_board(canvas, selected_board)

    while True:
        event, values = window2.read()

        if event == "Submit":
            move = window2['move'].Get()  # Get the move that user input
            if validate_input(move):
                # update board
                # update_board(move)
                pass
            else:
                # show error
                pass

            # Redraw the board
            draw_board(canvas, selected_board)
        elif event == sg.WIN_CLOSED or event == 'Exit':
            print(event)
            break
