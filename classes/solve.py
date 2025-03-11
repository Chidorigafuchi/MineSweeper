from classes.cells import CellsScanner


class Solver:
    numRows = 9
    numColumns = 6

    def __init__(self):
        raise TypeError("Cannot instantiate this class")

    @classmethod
    def solveObviousOnes(cls, cellsToCheck, newBoard):
        flag = set()
        mineFree = set()
        for coordinate in cellsToCheck:
            mines = 0
            unknown = 0
            noMines = 0
            for x in range(coordinate[0] - 1, coordinate[0] + 2):
                for y in range(coordinate[1] - 1, coordinate[1] + 2):
                    if 0 <= y < cls.numRows and 0 <= x < cls.numColumns:
                        if newBoard[y][x] == -1:
                            mines += 1
                        elif newBoard[y][x] == 9:
                            unknown += 1
                        else:
                            noMines += 1

            # проверка для флагов
            if CellsScanner.surroundingCellsNum(coordinate[0], coordinate[1]) - noMines == newBoard[coordinate[1]][coordinate[0]]:
                for x in range(coordinate[0] - 1, coordinate[0] + 2):
                    for y in range(coordinate[1] - 1, coordinate[1] + 2):
                        if 0 <= y < cls.numRows and 0 <= x < cls.numColumns:
                            if newBoard[y][x] == 9:
                                flag.add((x, y))

            # проверка для НЕ мин
            if newBoard[coordinate[1]][coordinate[0]] == mines:
                for x in range(coordinate[0] - 1, coordinate[0] + 2):
                    for y in range(coordinate[1] - 1, coordinate[1] + 2):
                        if 0 <= y < cls.numRows and 0 <= x < cls.numColumns:
                            if newBoard[y][x] == 9:
                                mineFree.add((x, y))
        return (flag, mineFree)

    @classmethod
    def solveProbabilityOnes(cls, newBoard):
        cellProbabilities = {}
        explorableCells = CellsScanner.findSectionsToProbTest(newBoard)
        explorableCells.sort(key=len)
        for cellGroup in explorableCells:
            incompleteCellsDict = {}
            cellsAndSurroundingDict = {}
            for coordinate in cellGroup:
                cellsAndSurroundingDict[coordinate] = CellsScanner.nearbyIncompleteCells(
                    coordinate[0], coordinate[1], newBoard)
                for incompleteCoordinate in cellsAndSurroundingDict[coordinate]:
                    incompleteCellsDict[incompleteCoordinate] = 0

            for incompleteCoordinate in incompleteCellsDict.keys():
                x = incompleteCoordinate[0]
                y = incompleteCoordinate[1]
                mines = CellsScanner.surroundingMines(x, y, newBoard)
                incompleteCellsDict[incompleteCoordinate] = newBoard[y][x] - mines

            goodResults = []
            cellGroupList = list(cellGroup)
            possibilities = [False] * len(cellGroupList)
            dontGoFurther = False
            totalRemainingMines = sum(incompleteCellsDict.values())

            def tryPossibiility(attempt, index, changeMine, incompletedCellDict, minesSum):
                nonlocal dontGoFurther
                dontGoFurther = False
                attempt[index] = changeMine

                if changeMine:
                    cellChanged = cellGroupList[index]
                    for coordinate in cellsAndSurroundingDict[cellChanged]:
                        minesSum -= 1
                        incompletedCellDict[coordinate] -= 1
                        if incompletedCellDict[coordinate] < 0:
                            dontGoFurther = True

                if dontGoFurther:
                    return
                if minesSum == 0:
                    nonlocal goodResults
                    goodResults.append(attempt.copy())
                    return
                if index == len(possibilities) - 1:
                    return

                tryPossibiility(attempt.copy(), index + 1, False,
                                incompletedCellDict.copy(), minesSum)
                tryPossibiility(attempt.copy(), index + 1, True,
                                incompletedCellDict.copy(), minesSum)

            tryPossibiility(possibilities.copy(), 0, False,
                            incompleteCellsDict.copy(), totalRemainingMines)
            tryPossibiility(possibilities.copy(), 0, True,
                            incompleteCellsDict.copy(), totalRemainingMines)

            for index, coord in enumerate(cellGroupList):
                tot = 0
                for attempt in goodResults:
                    if attempt[index]:
                        tot += 1
                    else:
                        tot += 0
                cellProbabilities[coord] = tot / len(cellGroupList)

        return cellProbabilities