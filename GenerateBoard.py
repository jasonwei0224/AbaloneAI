# move notation example: ['inline', ['G4w', 'H5w', 'I6w'], ['F3w','G4w','H5w']]
# board info example: ['A3b', 'B2b', 'B3b', 'C3b', 'C4b', 'G7b', 'G8b', 'H7b', 'H8b', 'H9b', 'I8b', 'I9b', 'A4w', 'A5w',
# 'B4w', 'B5w', 'B6w', 'C5w', 'C6w', 'G4w', 'G5w', 'H4w', 'H5w', 'H6w', 'I5w', 'I6w']


def generate_result_board(move_notation: [], board_info: []):
    move_type = move_notation[0]
    start_coords = move_notation[1]
    dest_coords = move_notation[2]
    result_board = [board_value for board_value in board_info if board_value not in start_coords]

    if validate_move_destination(dest_coords, result_board):
        print("invalid move_notation. Destination coordinate is not empty nor contains opponent marble")
        return None
    if move_type == "SS":
        # regular update
        [result_board.append(dest_coord) for dest_coord in dest_coords]
    if move_type == "I":
        for dest_coord in dest_coords:
            if dest_coord[0:2] in [result_coord[0:2] for result_coord in result_board]:
                if dest_coord[2] == 'w':
                    opponent_color = 'b'
                else:
                    opponent_color = 'w'
                opponent_marble_against = dest_coord[0:2] + opponent_color
                opp_move_array = push_okay(len(start_coords),
                                           result_board,
                                           start_coords[0],
                                           dest_coords[0],
                                           opponent_marble_against)
                if opp_move_array:
                    alphabet_change = opp_move_array[0]
                    number_change = opp_move_array[1]
                    opp_to_be_move_array = opp_move_array[2]
                    for opp_to_be_move in opp_to_be_move_array:
                        result_board.remove(opp_to_be_move)
                        opp_update = chr(ord(opp_to_be_move[0]) + alphabet_change) + \
                                     str(int(opp_to_be_move[1]) + number_change) + opp_to_be_move[2]
                        result_board.append(opp_update)
                    result_board.append(dest_coord)
                else:
                    print('invalid push opponent.')
                    return None
            else:
                # regular update
                result_board.append(dest_coord)
    return result_board


# invalid if destination coordinate already contains ally that won't be change
def validate_move_destination(dest_coordinates: [], board_coord_unchanged: []):
    return any(elem in dest_coordinates for elem in board_coord_unchanged)


def push_okay(num_ally_marbles_move: int, board_coord_unchanged: [],
              start_coordinate: str,
              dest_coordinate: str,
              coordinate_to_be_push: str):
    # 1 marble can't push any opponent marble
    if num_ally_marbles_move == 1:
        return None
    opponent_start = []

    # determine movement direction
    alphabet_change = ord(dest_coordinate[0]) - ord(start_coordinate[0])
    number_change = int(dest_coordinate[1]) - int(start_coordinate[1])

    # counter for number of opponent are inline with ally
    opp_marble_inline_count = 1
    opponent_array_push = [coordinate_to_be_push]
    # determine the coordinate behind opponent marble(this position is right next to the ally)
    alphabet_behind_opponent_marble_1 = chr(ord(coordinate_to_be_push[0]) + alphabet_change)
    number_behind_opponent_marble_1 = int(coordinate_to_be_push[1]) + number_change
    coordinate_behind_opponent_marble_1 = alphabet_behind_opponent_marble_1 + str(number_behind_opponent_marble_1) \
                                          + coordinate_to_be_push[2]
    # counter++ if opponent coordinate on board
    if coordinate_behind_opponent_marble_1 in board_coord_unchanged:
        opp_marble_inline_count = opp_marble_inline_count + 1
        opponent_array_push.append(coordinate_behind_opponent_marble_1)

    # determine if there's 3 opponent marbles inline against ally
    alphabet_behind_opponent_marble_2 = chr(ord(coordinate_behind_opponent_marble_1[0]) + alphabet_change)
    number_behind_opponent_marble_2 = int(coordinate_behind_opponent_marble_1[1]) + number_change
    coordinate_behind_opponent_marble_2 = alphabet_behind_opponent_marble_2 + str(number_behind_opponent_marble_2) \
                                          + coordinate_behind_opponent_marble_1[2]

    if coordinate_behind_opponent_marble_2 in board_coord_unchanged:
        opp_marble_inline_count = opp_marble_inline_count + 1
        opponent_array_push.append(coordinate_behind_opponent_marble_2)
        return None

    if num_ally_marbles_move <= opp_marble_inline_count:
        return None
    else:
        opponent_start = opponent_array_push
        print(opponent_start)
        return [alphabet_change, number_change, opponent_array_push]


def readInputFile(filename: str):
    inputDic = {}
    with open(filename, 'r', encoding='utf-8') as inputFile:
        lines = inputFile.readlines()
        if len(lines) != 2:
            print('invalid input... only allow 2 lines in input file')
            return
        inputDic['color'] = lines[0][0]
        inputDic['board'] = lines[1].replace('\n', '')
        inputDic['board'] = inputDic['board'].split(",")

        print(inputDic)
        return inputDic


def main():
    print('INPUT\n')
    board = readInputFile('Test1.input')['board']
    print('\n')
    # test regular SS
    print('SS')
    move_notation = ['SS', ['G4w', 'G5w'], ['F3w', 'F4w']]
    print("Move notation:", move_notation, "\n new board:", generate_result_board(move_notation, board))

    # test regular inline
    print('\nI(no push)')
    move_notation = ['I', ['G4w', 'G5w'], ['G3w', 'G4w']]
    print("Move notation:", move_notation, "\n new board:", generate_result_board(move_notation, board))

    # test push
    print('\nI(push)')
    move_notation = ['I', ['B4w', 'B5w', 'B6w'], ['B3w', 'B4w', 'B5w']]
    print("Move notation:", move_notation, "\n new board:", generate_result_board(move_notation, board))

    # test push
    print('\nI(push)')
    move_notation = ['I', ['B4w', 'C5w'], ['A3w', 'B4w']]
    print("Move notation:", move_notation, "\n new board:", generate_result_board(move_notation, board))


if __name__ == '__main__':
    main()
