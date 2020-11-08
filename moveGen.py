import copy


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


def targetAdj(marble_positions: []):
    if len(marble_positions) < 1 or len(marble_positions) > 3:
        print('only [1,2,3] marbles can be move')
        return
    nearbyCoordinates = []
    for marble_position in marble_positions:
        nearbyCoordinates.append(marble_position)
        alphabet_coordinate_unicode = ord(marble_position[0])
        num_cord = int(marble_position[1])
        marble_color = marble_position[2]
        temp = ''
        # SW
        temp = chr(alphabet_coordinate_unicode - 1)
        temp += str(num_cord - 1)
        temp += marble_color
        if temp not in nearbyCoordinates:
            nearbyCoordinates.append(temp)
        # W
        temp = chr(alphabet_coordinate_unicode)
        temp += str(num_cord - 1)
        temp += marble_color
        if temp not in nearbyCoordinates:
            nearbyCoordinates.append(temp)
        # NW
        temp = chr(alphabet_coordinate_unicode + 1)
        temp += str(num_cord)
        temp += marble_color
        if temp not in nearbyCoordinates:
            nearbyCoordinates.append(temp)
        # NE
        temp = chr(alphabet_coordinate_unicode + 1)
        temp += str(num_cord + 1)
        temp += marble_color
        if temp not in nearbyCoordinates:
            nearbyCoordinates.append(temp)
        # E
        temp = chr(alphabet_coordinate_unicode)
        temp += str(num_cord + 1)
        temp += marble_color
        if temp not in nearbyCoordinates:
            nearbyCoordinates.append(temp)
        # SE
        temp = chr(alphabet_coordinate_unicode - 1)
        temp += str(num_cord)
        temp += marble_color
        if temp not in nearbyCoordinates:
            nearbyCoordinates.append(temp)

    # remove added current positions
    # (for example, moving [A1w, A2w] would have A2w added to nearby list. <- we want to remove it)
    for marble_position in marble_positions:
        nearbyCoordinates = list(filter(lambda a: a != marble_position, nearbyCoordinates))

    # remove invalid coordinate (eg. E10, E0, Z3...)
    temp_array = copy.deepcopy(nearbyCoordinates)
    for marble_position in nearbyCoordinates:
        # remove nearby element if alpha coor is not from A to I
        if ord(marble_position[0]) < 65 or ord(marble_position[0]) > 73:
            temp_array.remove(marble_position)
            continue

        # remove nearby element if num coor is not legal
        # first handle lower board that alpha coor is from A to E
        if ord(marble_position[0]) < 70:
            # legal number:
            #               A: 1 - 5    note: ord('A') = 65
            #               B: 1 - 6
            #               C: 1 - 7
            #               D: 1 - 8
            #               E: 1 - 9
            if int(marble_position[1]) < 1 or int(marble_position[1]) > (ord(marble_position[0]) - 60):
                temp_array.remove(marble_position)
                continue
        # then handle upper board that alpha coor is from F to I
        else:
            # legal number:
            #               F: 2 - 9    note: ord('F') = 70
            #               G: 3 - 9
            #               H: 4 - 9
            #               I: 5 - 9
            if int(marble_position[1]) < (ord(marble_position[0]) - 68) or int(marble_position[1]) > 9:
                temp_array.remove(marble_position)
                continue
    nearbyCoordinates = temp_array

    print("nearby coordinates for ", marble_positions, " are: ", nearbyCoordinates)
    return nearbyCoordinates

"""
move notation example: ['inline', ['G4w', 'H5w', 'I6w'], ['F3w','G4w','H5w']]
"""
# def generate_available_move(move_notation: [], board_taken_coordinates: []):
#     nearby = targetAdj(move_notation[1])
#     for available_coordinate in nearby:
#
#     return


def main():
    board = readInputFile('Test1.input')['board']
    targetAdj(['G4w', 'H5w', 'I6w'])
    targetAdj(['G4w'])


if __name__ == '__main__':
    main()
