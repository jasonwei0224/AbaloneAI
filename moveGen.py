def readInputFile(filename):
    inputDic = {}
    with open(filename, 'r', encoding='utf-8') as inputFile:
        lines = inputFile.readlines()
        if len(lines) != 2:
            print('invalid input... only allow 2 lines in input file')
            return
        inputDic['color'] = lines[0][0]
        inputDic['board'] = lines[1]
        return inputDic


def targetAdj(marble_positions):
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
    for marble_position in marble_positions:
        print(marble_position == nearbyCoordinates[5])
        print(len(marble_position))
        print(len(nearbyCoordinates[6]))
        nearbyCoordinates = list(filter(lambda a: a != marble_position, nearbyCoordinates))

    # remove invalid coordinate (eg. E10, E0, Z3...)


    return nearbyCoordinates


print(targetAdj(['A1w', 'A2w', 'A3w']))
