import random

import PySimpleGUI as sg

# List of options for user to choose from
board_choice = ['Standard', 'German Daisy', 'Belgian Daisy']
player_color = ['Black', 'White']
game_mode = ["human vs human", "human vs computer"]

# Configuration window layout
config_layout = [[sg.Text('Select Initial Board Layout')],
                 [sg.Radio(board, 1) for board in board_choice],
                 [sg.Text('Select Player Color')],
                 [sg.Radio(color, 1) for color in player_color],
                 [sg.Text('Select Game Mode')],
                 [sg.Radio(mode, 1) for mode in game_mode],
                 [sg.Text('Set player 1 (human) move limit per game'),
                  sg.Spin([i for i in range(1, 11)], initial_value=1)],
                 [sg.Text('Set player 2 (computer/human) move limit per game'),
                  sg.Spin([i for i in range(1, 11)], initial_value=1)],
                 [sg.Text('Set player 1 (human) time limit for a move limit'),
                  sg.Spin([i for i in range(1, 11)], initial_value=1)],
                 [sg.Text('Set player 2 (computer/human) time limit for a move limit'),
                  sg.Spin([i for i in range(1, 11)], initial_value=1)],
                 [sg.OK("Start"), sg.Cancel("Exit")]]

# drop down menu layout
menu = [['Actions', ['Play', 'Stop', 'Pause', 'Reset']],
        ['History', ['Player Move History', 'Player Time History']]]

window = sg.Window('Game Configuration', config_layout)

event, values = window.read()

if event == "Exit":
    window.close()
elif event == 'Start':
    window.close()  # Close the configuration window
    game_layout = [
        [sg.Menu(menu, )], [sg.Column([[sg.Text('Game Score: 0 ')]]), sg.Column([[sg.Button('Undo')]])],
        [sg.Column([[sg.Text('Moves Taken by Player 1:   ')]]),
         sg.Column([[sg.Text('Moves Taken by Player 2: ')]])],
        [sg.Column([[sg.Text('Time Taken by Player 1:   ')]]),
         sg.Column([[sg.Text('Time Taken by Player 2:  ')]])],
        [sg.Column([[sg.Text('Next Move: ....')]])],
        [sg.Graph((300, 300), (0, 300), (300, 0), key='graph')],
        [sg.Column([[sg.InputText("Please Enter your move", key='move')], [sg.Button("Submit")]], )]
    ]
    window2 = sg.Window('Abalone', game_layout).Finalize()  # Create the game window

    canvas = window2['graph']

    # default starting position of marbles
    default_board = [
        ["-", "-", 1, 1, 1, 1, 1, "-", "-"],
        ["-", 1, 1, 1, 1, 1, 1, "-", "-"],
        ["-", 0, 0, 1, 1, 1, 0, 0, "-"],
        ["-", 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["-", 0, 0, 0, 0, 0, 0, 0, 0],
        ["-", 0, 0, 2, 2, 2, 0, 0, "-"],
        ["-", 2, 2, 2, 2, 2, 2, "-", "-"],
        ["-", "-", 2, 2, 2, 2, 2, "-", "-"],
    ]

    offset_lst = [8, 15, 6, -5, 5, -5, 6, 15, 8]
    BOX_SIZE = 22
    RADIUS = 10
    for row in range(len(default_board)):
        offset = offset_lst[row]
        for col in range(len(default_board[row])):
            if default_board[row][col] == '-':

                canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), RADIUS, fill_color="",
                                  line_color='')

            elif default_board[row][col] == 0:
                canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), RADIUS, fill_color="dark grey")

            elif default_board[row][col] == 1:
                canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), RADIUS, fill_color='white')

            elif default_board[row][col] == 2:
                canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), RADIUS, fill_color='black')

    while True:
        event, values = window2.read()

        # based on the board representation given in class change the letter to the row it represents (starting at
        # row 0)
        location_dict = {"I": 0, "H": 1, "G": 2, "F": 3, "E": 4, "D": 5, "C": 6, "B": 7, "A": 8}

        if event == "Submit":
            move = window2['move'].Get()  # Get the move that user input

            # Get the starting row, column and ending row, column of a marble
            # Currently only work with moving single marble
            start_row = location_dict[move[0]]
            start_col = int(move[1]) - start_row
            end_row = location_dict[move[3]]
            end_col = int(move[4]) - end_row

            # update the Abalone representation of the board
            default_board[end_row][end_col + start_row] = default_board[start_row][start_col]
            default_board[start_row][start_col] = 0

            # Redraw the board
            for row in range(len(default_board)):
                offset = offset_lst[row]
                for col in range(len(default_board[row])):
                    if default_board[row][col] == '-':
                        canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), 10, fill_color="",
                                          line_color='')
                    elif default_board[row][col] == 0:
                        canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), 10,
                                          fill_color="dark grey")
                    elif default_board[row][col] == 1:
                        canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), 10, fill_color='white')
                    elif default_board[row][col] == 2:
                        canvas.DrawCircle((col * BOX_SIZE + 20 + offset, row * BOX_SIZE + 15), 10, fill_color='black')
