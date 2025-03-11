class CellsScanner:
    numRows = 9
    numColumns = 6

    def __init__(self):
        raise TypeError("Cannot instantiate this class")

    @classmethod
    def surroundingCellsNum(cls, column, row):
        onVerticalEdge = column == 0 or column == cls.numColumns - 1
        onHorizontalEdge = row == 0 or row == cls.numRows - 1

        if onHorizontalEdge and onVerticalEdge:
            return 4
        elif onVerticalEdge or onHorizontalEdge:
            return 6
        else:
            return 9

    @classmethod
    def nearbyIncompleteCells(cls, column, row, newBoard):
        res = set()
        for x in range(column - 1, column + 2):
            for y in range(row - 1, row + 2):
                if 0 <= y < cls.numRows and 0 <= x < cls.numColumns:
                    if 0 < newBoard[y][x] < 9:
                        res.add((x, y))
        return res

    @classmethod
    def surroundingMines(cls, column, row, newBoard):
        mines = 0
        for x in range(column - 1, column + 2):
            for y in range(row - 1, row + 2):
                if y >= 0 and y < cls.numRows and x >= 0 and x < cls.numColumns:
                    if newBoard[y][x] == -1:
                        mines += 1
        return mines

    @classmethod
    def findNewCells(cls, pastBoard, newBoard):
        result = []

        for column in range(cls.numColumns):
            for row in range(cls.numRows):
                if pastBoard[row][column] != newBoard[row][column] and newBoard[row][column] != 0:
                    result.append((column, row))
        return result

    @classmethod
    def shouldExamine(cls, column, row, newBoard):
        notOutOfBounds = 0 <= row < cls.numRows and 0 <= column < cls.numColumns
        return notOutOfBounds and newBoard[row][column] != 0 and newBoard[row][column] != 9 and newBoard[row][
            column] != -1

    @classmethod
    def findCellsToExamine(cls, pastBoard, newBoard):
        result = set()
        consideredCells = cls.findNewCells(pastBoard, newBoard)

        # находим все клетки рядом
        for coordinate in consideredCells:
            result.add(coordinate)
            for x in range(coordinate[0] - 1, coordinate[0] + 2):
                for y in range(coordinate[1] - 1, coordinate[1] + 2):
                    if cls.shouldExamine(x, y, newBoard):
                        result.add((x, y))
        print(f'{result} - клетки для простых')
        return result

    @staticmethod
    def inSetList(elm, setList):
        for i in range(len(setList)):
            if elm in setList[i]:
                return True, i
        return False, -1

    @classmethod
    def findSectionsToProbTest(cls, newBoard):
        unexploredCells = []
        testableSurroundingCells = []
        sortedTestableCells = []

        for row in range(cls.numRows):
            for column in range(cls.numColumns):
                if 0 < newBoard[row][column] < 9:
                    res = []
                    for x in range(column - 1, column + 2):
                        for y in range(row - 1, row + 2):

                            if 0 <= y < cls.numRows and 0 <= x < cls.numColumns and newBoard[y][x] == 9:
                                res.append((x, y))

                    if len(res) > 0:
                        unexploredCells.append((column, row))
                        testableSurroundingCells.append(res)

        # сортируем

        for i in range(len(unexploredCells)):
            similarSets = set()
            for coordinate in testableSurroundingCells[i]:
                inSetData = cls.inSetList(coordinate, sortedTestableCells)
                if inSetData[0]:
                    similarSets.add(inSetData[1])

            similarSets = list(similarSets)
            if len(similarSets) == 0:
                sortedTestableCells.append(set(testableSurroundingCells[i]))
            elif len(similarSets) == 1:
                sortedTestableCells[similarSets[0]].update(
                    set(testableSurroundingCells[i]))
            else:
                while len(similarSets) > 1:
                    deletedSet = sortedTestableCells.pop(similarSets[-1])
                    similarSets.pop()
                    sortedTestableCells[similarSets[0]].update(deletedSet)
                sortedTestableCells[similarSets[0]].update(
                    set(testableSurroundingCells[i]))

        return sortedTestableCells