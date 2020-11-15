import math
import constant

def score(move_notation):
    dest_coords = move_notation[2]
    rows = []
    cols = []
    for value in dest_coords:
        row = constant.LOCATION_DICT[value[0]]
        col = int(value[1]) - constant.LETTER_AND_NUM_OFFSET[row][1]
        rows.append(row)
        cols.append(col)
    # center
    center_alpha = 4
    center_number = 4
    alpha_coord = sum(cols) / len(cols)
    print(alpha_coord)
    number_coord = sum(rows) / len(rows)
    print(number_coord)
    distance = (alpha_coord - center_alpha) ** 2 + (number_coord - center_number) ** 2
    distance = math.sqrt(distance)
    return distance


def main():
    test = [[1, 0, 0], [0, 1, 0]]
    test_move_notation = ('I', ['H6'], ['I7'])
    print(score(test_move_notation))
    test_move_notation = ('I', ['C6', 'B5'], ['D7', 'C6'])
    print(score(test_move_notation))


if __name__ == '__main__':
    main()