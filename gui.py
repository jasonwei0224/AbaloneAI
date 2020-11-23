import PySimpleGUI as sg
import constant
import GenerateBoard
import game_playing_agent
import copy
import traceback
from GenerateBoard import generate_result_board

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
                        [sg.InputText("Enter your move: type, starting nodes, ending nodes", key='move'), sg.Button("Submit")],
                        [sg.Text('Next Move: ', key="next_move", size=(50,1))],
                        [sg.Text('Number of moves taken: ', key="num_of_moves", size=(50,1))],
                        [sg.Text('Player 1 Out: 0', key="p1_out"),
                         sg.Text('Player 1 color: ' + ("White" if player1_color == 1 else "Black"))],
                        [sg.Text('Player 2 Out: 0', key = "p2_out"),
                         sg.Text('Player 2 color: ' + ("Black" if player2_color == 2 else "White"))],
                        [sg.Text('Time taken by Player 1:   ', size=(60,1), key="time_p1")],
                        [sg.Text('Time taken by Player 2:  ')],
                        [sg.VerticalSeparator(pad=((0, 0), (10, 20)))],
                        [sg.Text('Moves taken by Player 1:   ', pad=((0, 50), (0, 0)), key='p1_move_limit'),
                         sg.Text('Moves taken by Player 2: ', key='p2_move_limit')],
                        [sg.Multiline('', size=(25, 10), key="p1_move"),
                         sg.Multiline('', size=(25, 10), key="p2_move")],
                        ]

    return game_info_layout

def tanslate_move_notation_to_with_no_color(move_notation):
    for i in range(len(move_notation[1])):
        move_notation[1][i] = move_notation[1][i][:2]
        move_notation[2][i] = move_notation[2][i][:2]
    return move_notation

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
    # TODO Need to implement
    return True

def translate_move(move_str):
    move_lst = move_str.split(",")
    move = ""
    if len(move_lst[1:]) == 6:
        move = (move_lst[0], (move_lst[1:4]), (move_lst[4:]))

    elif len(move_lst[1:]) == 4:
        move = (move_lst[0], (move_lst[1:3]), (move_lst[3:]))
        print(move)
    elif len(move_lst[1:]) == 2:
        move = (move_lst[0], [move_lst[1]], [move_lst[2]])
    return move



def coordinates_to_notation(row, col):
    """
    change matrix row, col to notation used in class
    :param row: int
    :param col: int
    :return: string E.g. "A1"
    """
    return str(constant.LETTER_AND_NUM_OFFSET[row][0]) + str(col + constant.LETTER_AND_NUM_OFFSET[row][1])

def text_to_matrix_board(text_board_format):
    # location_matrix =constant.EMPTY_BOARD[:]
    location_matrix = copy.deepcopy(constant.EMPTY_BOARD)
    for value in text_board_format:
        row = constant.LOCATION_DICT[value[0]]
        col = int(value[1]) - constant.LETTER_AND_NUM_OFFSET[row][1]
        location_matrix[row][col] = 1 if value[2] == 'w' else 2
    return location_matrix

def translate_board_format_to_text(selected_board):
    text_board_format = []
    for row in range(len(selected_board)):
        for col in range(len(selected_board[row])):
            if selected_board[row][col] == 1 or selected_board[row][col] == 2:
                text_board_format.append(coordinates_to_notation(row, col) + ("b" if selected_board[row][col] == 2 else 'w'))

    return text_board_format

def get_move_detail(moves):
    """
    print list of moves based on move notation with coordinate translate to notation used in class
    :param moves: list of move notation [( move type, [starting coordinates], [end coordinates])]
    :return:
    """
    for i in range(len(moves)):
        origin = ""
        dest = ""
        for coordinate in moves[i][1]:
            origin += coordinate + " "
        for coordinate in moves[i][2]:
            dest += coordinate + " "
        return(moves[i][0] + ": " + str(origin) + " => " + str(dest))

def remove_color(moves):
    for i in range(len(moves[1])):
        moves[1][i] = move[1][i][:-1]
        moves[2][i] = move[2][i][:-1]
    return moves

def process_move_history(move_lst, turn, player1_color, player2_color):
    # print('current turn in move history ', turn, move_lst)
    if turn == 2:
        if player1_color == 2:
            color_txt = 'b'
        else:
            color_txt = 'w'
    elif turn == 1:
        if player1_color == 1:
            color_txt = 'b'
        else:
            color_txt = 'w'


    types = move_lst.pop(0)
    move_type = types.replace('\n', '')
    move_type = move_type.replace(':', '')
    move_notation = ''
    if len(move_lst) == 2:
        end = move_lst[:1]
        start = move_lst[1:]
        for i in range(len(end)):
            if '\n' in end[i]:
                end[i] = end[i].replace('\n', '')
            if '\n' in start[i]:
                start[i]= start[i].replace('\n', '')
            end[i] += color_txt
            start[i] += color_txt
        move_notation = [move_type, start, end]
    elif len(move_lst) == 4:
        end = move_lst[:2]
        start = move_lst[2:]
        for i in range(len(end)):
            if '\n' in end[i]:
                end[i] = end[i].replace('\n', '')
            if '\n' in start[i]:
                start[i]= start[i].replace('\n', '')
            end[i] += color_txt
            start[i] += color_txt
        move_notation = [move_type, start, end]

    elif len(move_lst) == 6:
        end = move_lst[:3]
        start = move_lst[3:]
        for i in range(len(end)):
            if '\n' in end[i]:
                end[i] = end[i].replace('\n', '')
            if '\n' in start[i]:
                start[i]= start[i].replace('\n', '')
            end[i] += color_txt
            start[i] += color_txt
        move_notation = [move_type, start, end]

    return move_notation
def update_move_history(move_lst):
    s = ""
    for i in move_lst:
        if '\n' not in i:
            s+=" "
        s+=i
    return s

window = sg.Window('Game Configuration', config_layout, font=('arial', 15))

event, values = window.read()

if event == "Exit":
    window.close()
elif event == 'Start':

    # Get the initial board layout
    if window["Standard"].Get():
        selected_board = copy.deepcopy(constant.DEFAULT_BOARD)
    elif window["German Daisy"].Get():
        selected_board = copy.deepcopy(constant.GERMAN_BOARD)
    elif window["Belgian Daisy"].Get():
        selected_board = copy.deepcopy(constant.BELGIAN_BOARD)
    else:
        selected_board = copy.deepcopy(constant.DEFAULT_BOARD)

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
    max_moves = int(window["max_moves"].Get())*2
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
    turn = 1 if player1_color == 2 else 2
    player1_out = 0
    player2_out = 0
    state_space = [player1_out, player2_out, selected_board]
    num_moves = 0
    total_time = 0
    agent_time = 0
    while True:
        # print(num_moves)
        # print("Current Turn", turn)
        try:
            window2["num_of_moves"].update("Number of moves taken: " + str(num_moves) + " / " + str(max_moves))
            event, values = window2.read()
            if event == "Undo":
                if len(window2['p2_move'].Get()) == 1 and len(window2['p1_move'].Get()) == 1:
                    pass
                else:

                    if turn == 1:
                        # print("Current Turn in if turn == 1", turn)
                        move_lst = window2["p2_move"].Get().split(' ')
                        move_lst2=[]
                        move_lst2.insert(0,move_lst.pop(-1))

                        while True:
                            if '\n' in move_lst[-1]:
                                break
                            else:
                                move_lst2.insert(0,move_lst.pop(-1))
                        move_lst2.insert(0,move_lst.pop(-1))
                        # print(move_lst)
                        remaining_move = update_move_history(move_lst)
                        window2["p2_move"].update(remaining_move)
                        print(remaining_move)
                        # print(move_lst2)
                        move_lst =  list(filter(lambda a: a != "=>" and a != ''and a != '\n', move_lst2))
                        print(move_lst)

                    elif turn == 2:
                        move_lst = window2["p1_move"].Get().split(' ')
                        move_lst2 = []
                        move_lst2.insert(0,move_lst.pop(-1))

                        while True:
                            if '\n' in move_lst[-1]:
                                break
                            else:
                                move_lst2.insert(0,move_lst.pop(-1))
                        move_lst2.insert(0,move_lst.pop(-1))
                        # print(move_lst)
                        remaining_move = update_move_history(move_lst)
                        window2["p1_move"].update(remaining_move)
                        print(remaining_move)
                        # print(move_lst2)
                        move_lst = list(filter(lambda a: a != "=>" and a != '' and a != '\n', move_lst2))
                        print(move_lst)
                    # print(move_lst)
                    last_move = process_move_history(move_lst, turn, player1_color, player2_color)
                    print(last_move)
                    text_board_format = translate_board_format_to_text(selected_board)
                    new_board = GenerateBoard.generate_result_board(last_move, text_board_format)  # get the updated board to be
                    selected_board = text_to_matrix_board(new_board['board'])  # translate to matrix notation
                    draw_board(canvas, selected_board)  # update board on gui
                    num_moves -= 1  # update number of moves taken
                    window2["num_of_moves"].update("Number of moves taken: " + str(num_moves) + " / " + str(max_moves))

                    turn = 1 if turn == 2 else 2  # change turns
            elif event == "Stop":
                pass
            elif event == "Pause":
                pass
            elif event == "Play":
                pass
            elif event == "Submit":
                move = window2['move'].Get()  # Get the move that user input

                if turn == 1:

                    # TODO: CALL AI GAME AGENT HERE
                    # current state space to be passed into game playing agent
                    state_space = [
                        player1_out,
                        player2_out,
                        selected_board,
                        player1_color,
                        player2_color,
                        []] # attacks on opp

                    turn_color = "w" if player1_color == 1 else "b"

                    # call the game playing agent and get the board/move notation
                    if num_moves == 0:
                        v, move, time = game_playing_agent.iterative_deepening(state_space, turn_color, 0,
                                                                         int(window['p1_time_limit'].Get()), True)

                        agent_time += time
                        print('num', v, move, time, agent_time, str(agent_time))

                        window2["time_p1"].update("Time taken by player 1: " + str(agent_time))
                    else:
                        v, move, time = game_playing_agent.iterative_deepening(state_space, turn_color, 0,
                                                                         int(window['p1_time_limit'].Get()), False)
                        print(v, move, time)
                        agent_time += time
                        window2["time_p1"].update("Time taken by player 1: " + str(agent_time))

                    text_board_format = translate_board_format_to_text(selected_board)
                    new_board = GenerateBoard.generate_result_board(move, text_board_format)  # get the updated board to be
                    selected_board = text_to_matrix_board(new_board['board'])
                    move_notation_no_color = tanslate_move_notation_to_with_no_color(move)
                    window2['next_move'].update(get_move_detail([move_notation_no_color]))
                    if new_board['isScore']:
                        player2_out = + 1
                        window2['p2_out'].update("Player 1 Out: "+str(player2_out)) # update points if pushed off

                    draw_board(canvas, selected_board)
                    window2["p1_move"].update(window2["p1_move"].Get() + get_move_detail([move])) # show moves
                    num_moves += 1  # update number of moves taken
                    window2["num_of_moves"].update("Number of moves taken: " + str(num_moves) + " / " + str(max_moves)) # update on gui
                    # window2["time_p1"].update("Time taken by player 1: " + str(agent_time))
                    turn = 2 if turn == 1 else 1 # change turns

                else:
                    if validate_input(move):
                        # OPPONENT INPUT: Type, coordinates no space
                        move = translate_move(move)
                        print("move with color", move)
                        text_board_format = translate_board_format_to_text(selected_board)
                        new_board = GenerateBoard.generate_result_board(move, text_board_format) # get the updated board to be
                        selected_board = text_to_matrix_board(new_board['board'])  # translate to matrix notation
                        move = remove_color(move)
                        print("move without color" ,move)
                        window2['next_move'].update("Next Move: " + get_move_detail([move])) # display next move on screen
                        if new_board['isScore']:
                            print('add ')
                            player1_out += 1
                            print(player1_out)
                            window2['p1_out'].update("Player 1 out: " + str(player1_out))
                        draw_board(canvas, selected_board) # update board on gui
                        window2["p2_move"].update(window2["p2_move"].Get() + get_move_detail([move])) # record move on screen
                        num_moves += 1 # update number of moves taken
                        window2["num_of_moves"].update("Number of moves taken: " + str(num_moves) + " / " + str(max_moves))
                        turn = 1 if turn == 2 else 2 # change turns


            elif event == sg.WIN_CLOSED or event == 'Exit':
                print(event)
                break
        except:
            print('error try again')
            print(traceback.format_exc())

            continue
