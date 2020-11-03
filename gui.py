import PySimpleGUI as sg


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
                 [sg.Radio(board, 1, default=True) if board == 'Standard' else sg.Radio(board, 1) for board in board_choice],
                 [sg.VerticalSeparator(pad=((0,0),(10,20)))],
                 [sg.Text('Select Player Color', text_color="yellow")],
                 [sg.Radio(color, 2, default=True) if color == 'Black' else sg.Radio(color, 2)  for color in player_color],
                 [sg.VerticalSeparator(pad=((0,0),(10,20)))],
                 [sg.Text('Select Game Mode', text_color="yellow")],
                 [sg.Radio(mode, 3,  default=True) for mode in game_mode],
                 [sg.VerticalSeparator(pad=((0,0),(10,20)))],
                 [sg.Text('Set player move limit per game:'),
                  sg.Spin([i for i in range(1, 11)], initial_value=15)],
                [sg.VerticalSeparator(pad=((0,0),(10,20)))],
                 [sg.Text('Set player 1 (human) time limit for a move limit (s)'),
                  sg.Spin([i for i in range(1, 11)], initial_value=1)],
                 [sg.VerticalSeparator(pad=((0,0),(10,20)))],
                 [sg.Text('Set player 2 (computer/human) time limit for a move  (s)'),
                  sg.Spin([i for i in range(1, 11)], initial_value=1)],
                 [sg.OK("Start", pad=((10,0),(50,10))), sg.Cancel("Exit",  pad=((20,0),(50,10)))]]

# drop down menu layout
menu = [['Actions', ['Play', 'Stop', 'Pause', 'Reset']],
        ['History', ['Player Move History', 'Player Time History']]]

window = sg.Window('Game Configuration', config_layout, font=('arial', 15))

event, values = window.read()

selected_board = [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 2, 0, 0],
    [2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2],
]

if event == "Exit":
    window.close()
elif event == 'Start':
    window.close()  # Close the configuration window
    time_col = sg.Col([])
    col = [[sg.Button('Play'), sg.Button('Pause'), sg.Button('Stop'), sg.Button('Undo')],
        [sg.VerticalSeparator(pad=((0, 0), (10, 20)))],
        [sg.InputText("Please Enter your move", key='move'), sg.Button("Submit")],
           [sg.Text('Next Move: ....'), ],
        [sg.VerticalSeparator(pad=((0, 0), (10, 20)))],
        [sg.Text('Player 1: 0')],
        [sg.Text('Player 2: 0')],
        [sg.Text('Time Taken by Player 1:   ')],
        [sg.Text('Time Taken by Player 2:  ')],
        [sg.VerticalSeparator(pad=((0, 0), (10, 20)))],

        [sg.Text('Moves Taken by Player 1:   ' ,pad= ((0,50),(0,0))),sg.Text('Moves Taken by Player 2: ')],
        [sg.Multiline('Moves Taken by Player 1:   ',size=(25,10)), sg.Multiline('Moves Taken by Player 2: ',size=(25,10))],
        ]
    game_layout = [
        [sg.Graph((600, 600), (0, 300), (300, 0), key='graph'), sg.Column(col)],
    ]

    window2 = sg.Window('Abalone', game_layout,  font=('arial', 15)).Finalize()  # Create the game window

    canvas = window2['graph']


    offset_lst = [48, 38, 28, 17, 5, 17, 28, 38, 48]
    BOX_SIZE = 28
    RADIUS = 13

    for row in range(len(selected_board)):
        offset = offset_lst[row]
        for col in range(len(selected_board[row])):
            if selected_board[row][col] == 0:
                canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), RADIUS, fill_color="dark grey")

            elif selected_board[row][col] == 1:
                canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), RADIUS, fill_color='white')

            elif selected_board[row][col] == 2:
                canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), RADIUS, fill_color='black')

            canvas.draw_text('{}'.format(letter_and_numOffset[row][0] + str(letter_and_numOffset[row][1]+col)),
                             (col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), color="red")


    while True:
        event, values = window2.read()

        if event == "Submit":
            move = window2['move'].Get()  # Get the move that user input

            # Get the starting row, column and ending row, column of a marble
            # Currently only work with moving single marble
            start_row = location_dict[move[0]]
            start_col = int(move[1]) - start_row
            end_row = location_dict[move[3]]
            end_col = int(move[4]) - end_row

            # update the Abalone representation of the board
            selected_board[end_row][end_col + start_row] = selected_board[start_row][start_col]
            selected_board[start_row][start_col] = 0

            # Redraw the board
            for row in range(len(selected_board)):
                offset = offset_lst[row]
                for col in range(len(selected_board[row])):
                    if selected_board[row][col] == 0:
                        canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), RADIUS,
                                          fill_color="dark grey")

                    elif selected_board[row][col] == 1:
                        canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), RADIUS,
                                          fill_color='white')

                    elif selected_board[row][col] == 2:
                        canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), RADIUS,
                                          fill_color='black')

                    canvas.draw_text(
                        '{}'.format(letter_and_numOffset[row][0] + str(letter_and_numOffset[row][1] + col)),
                        (col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), color="red")