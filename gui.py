import PySimpleGUI as sg

# List of options for user to choose from
board_choice = ['Standard','German Daisy','Belgian Daisy']
player_color = ['Black', 'White']
game_mode = ["human vs human", "human vs computer"]

# Configuration window layout
config_layout = [  [sg.Text('Select Initial Board Layout')],
            [sg.Radio(board, 1) for board in board_choice],
            [sg.Text('Select Player Color')],
            [sg.Radio(color, 1) for color in player_color],
            [sg.Text('Select Game Mode')],
            [sg.Radio(mode, 1) for mode in game_mode],
            [sg.Text('Set player 1 (human) move limit per game'), sg.Spin([i for i in range(1,11)], initial_value=1)],
            [sg.Text('Set player 2 (computer/human) move limit per game'), sg.Spin([i for i in range(1,11)], initial_value=1)],
            [sg.Text('Set player 1 (human) time limit for a move limit'), sg.Spin([i for i in range(1,11)], initial_value=1)],
            [sg.Text('Set player 2 (computer/human) time limit for a move limit'), sg.Spin([i for i in range(1,11)], initial_value=1)],
            [sg.OK("Start"), sg.Cancel("Exit")]]

# drop down menu layout
menu = [['Actions', ['Play', 'Stop', 'Pause', 'Reset' ]],
            ['History', ['Player Move History', 'Player Time History']]]

# Game window layout
game_layout = [[sg.Menu(menu, )],[sg.Column([[sg.Text('Game Score: 0 ')]]), sg.Column([[sg.Button('Undo')]])],
               [sg.Column([[sg.Text('Moves Taken by Player 1:   ')]]), sg.Column([[sg.Text('Moves Taken by Player 2: ')]])],
               [sg.Column([[sg.Text('Time Taken by Player 1:   ')]]), sg.Column([[sg.Text('Time Taken by Player 2:  ')]])],
                [sg.Column([[sg.Text('Next Move: ....')]])],
            [sg.Canvas(size=(500, 500), background_color='red', key= 'canvas')],
         ]


window = sg.Window('Game Configuration', config_layout)
event, values = window.read()

if event == "Exit":
    window.close()
elif event == 'Start':
    window.close()  # Close the configuration window
    window2 = sg.Window('Abalone', game_layout)  # Create the game window
    event, values = window2.read()