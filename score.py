import math
import constant


def score(alpha_coord, number_coord):
    # rows = []
    # cols = []
    # for value in dest_coords:
    #     row = constant.LOCATION_DICT[value[0]]
    #     col = int(value[1]) - constant.LETTER_AND_NUM_OFFSET[row][1]
    #     rows.append(row)
    #     cols.append(col)
    # center
    center_alpha = 4
    center_number = 4

    # alpha_coord = sum(cols) / len(cols)
    # number_coord = sum(rows) / len(rows)
    distance = (alpha_coord - center_alpha) ** 2 + (number_coord - center_number) ** 2
    distance = math.sqrt(distance)
    return distance


def eval_distance(board, player_color, weight):
    player_distance_eval_values = []
    opponent_distance_eval_values = []
    for row in range(len(board)):
        for col in range(len(board[row])):

            if board[row][col] == 0:
                continue

            distance = score(row, col)
            if distance == 0:
                distance = 0.1
            distance_eval_h_value = 1 / distance

            if board[row][col] == player_color:
                player_distance_eval_values.append(distance_eval_h_value)
            else:
                opponent_distance_eval_values.append(distance_eval_h_value)

    player_distance_eval = sum(player_distance_eval_values)
    opponent_distance_eval = sum(opponent_distance_eval_values)
    return player_distance_eval * weight * -1 + opponent_distance_eval * weight


def eval_h(state, player_color):
    player_current_score = state[0]
    opponent_current_score = state[1]

    if player_current_score == 6:
        return 1
    elif opponent_current_score == 6:
        return -1
    else:

        return player_current_score * -0.1 + opponent_current_score * 0.1 + eval_distance(state[2], player_color,
                                                                                          0.08)


def main():
    test = [[1, 0, 0], [0, 1, 0]]
    test_move_notation = ('I', ['H6'], ['I7'])
    print(score(test_move_notation))
    test_move_notation = ('I', ['C6', 'B5'], ['D7', 'C6'])
    print(score(test_move_notation))


if __name__ == '__main__':
    main()
