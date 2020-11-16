import move_generator, GenerateBoard, constant

import PySimpleGUI as sg


def main():
    test_number = input("please enter test number: ")
    matrix, player_color = move_generator.get_input("Test" + str(test_number) + ".input")
    move_dict = move_generator.generate_moves(matrix, player_color)
    # output into test#.move
    for move_notation in move_dict['inline_ply_moves']:
        with open("Test" + str(test_number) + ".move", 'a', encoding='utf-8') as file:
            file.write("'{}', {} => {}\n".format(move_notation[0], move_notation[1], move_notation[2]))

    for move_notation in move_dict['sidestep_ply_moves']:
        with open("Test" + str(test_number) + ".move", 'a', encoding='utf-8') as file:
            file.write("'{}', {} => {}\n".format(move_notation[0], move_notation[1], move_notation[2]))

    # generate board
    board = GenerateBoard.readInputFile("Test" + str(test_number) + ".input")['board']
    for move_notation in move_dict['inline_ply_moves']:
        move_notation_for_board = [move_notation[0]]
        start_coords = []
        dest_coords = []

        for start_coord in move_notation[1]:
            start_coords.append(start_coord + player_color[0])
        move_notation_for_board.append(start_coords)

        for dest_coord in move_notation[2]:
            dest_coords.append(dest_coord + player_color[0])
        move_notation_for_board.append(dest_coords)
        result_board = GenerateBoard.generate_result_board(move_notation_for_board, board)['board']
        # output to test#.board
        with open("Test" + str(test_number) + ".board", 'a', encoding='utf-8') as file:
            file.write("")
            for index in range(0, len(result_board) - 1):
                file.write(result_board[index])
                file.write(",")
            file.write(result_board[-1])
            file.write("\n")

    for move_notation in move_dict['sidestep_ply_moves']:
        move_notation_for_board = [move_notation[0]]
        start_coords = []
        dest_coords = []

        for start_coord in move_notation[1]:
            start_coords.append(start_coord + player_color[0])
        move_notation_for_board.append(start_coords)

        for dest_coord in move_notation[2]:
            dest_coords.append(dest_coord + player_color[0])
        move_notation_for_board.append(dest_coords)
        result_board = GenerateBoard.generate_result_board(move_notation_for_board, board)['board']
        # output to test#.board
        with open("Test" + str(test_number) + ".board", 'a', encoding='utf-8') as file:
            for index in range(0, len(result_board) - 1):
                file.write(result_board[index])
                file.write(",")
            file.write(result_board[-1])
            file.write("\n")

    # move_generator.show_grid(matrix)


if __name__ == '__main__':
    main()
