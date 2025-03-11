import pyautogui as pg
import time
import sys
from classes.board import Board
from classes.cells import CellsScanner
from classes.solve import Solver


class Game:
    numRows = 9
    numColumns = 6

    startX = 1085
    startY = 581
    pixelX = 78
    pixelY = 50

    pastBoard = [[] ]
    newBoard = [[]]
    newgame = False

    movesLeft = 1
    movesToExecute = 1
    setted_flags = []

    @classmethod
    def updateBoard(cls):
        cls.pastBoard = cls.newBoard
        cls.getNewBoard()

        for i in range(len(cls.newBoard)):
            for j in range(len(cls.newBoard[0])):
                if cls.newBoard[i][j] == 1 and cls.pastBoard[i][j] != 1:
                    cls.leftClick(j, i)

        for flag_pos in cls.setted_flags:
            cls.newBoard[flag_pos[0]][flag_pos[1]] = -1

        if cls.newgame:
            time.sleep(5)
            print('Она точно началась.')
            cls.pastBoard = [[9 for _ in range(cls.numColumns)] for q in range(cls.numRows)]
            cls.getNewBoard()
            cls.movesLeft = cls.numColumns * cls.numRows
            cls.movesToExecute = 1
            cls.setted_flags = []

    @classmethod
    def makeMoves(cls):
        cellsToExamine = CellsScanner.findCellsToExamine(cls.pastBoard, cls.newBoard)
        moves = Solver.solveObviousOnes(cellsToExamine, cls.newBoard)

        cls.movesToExecute = len(moves[0]) + len(moves[1])

        if moves[0]:
            pg.click(x=1451, y=466, duration=0.3)
            for coordinate in moves[0]:
                cls.setted_flags.append([coordinate[1], coordinate[0]])
                cls.rightClick(coordinate[0], coordinate[1])
                cls.movesLeft -= 1

            pg.click(x=1451, y=466, duration=0.3)

        if moves[1]:
            for coordinate in moves[1]:
                cls.leftClick(coordinate[0], coordinate[1])
                cls.movesLeft -= 1
        elif moves[0]:
            for flag_pos in cls.setted_flags:
                cls.newBoard[flag_pos[0]][flag_pos[1]] = -1

            cls.makeMoves()

        if cls.movesLeft == 0:
            sys.exit("SOLVED!!!")

    @classmethod
    def game(cls):
        while cls.movesLeft > 0:
            while cls.movesToExecute > 0:
                cls.makeMoves()
                time.sleep(2)
                if cls.movesToExecute == 0:
                    break
                cls.updateBoard()

            cellsWithProbabilities = Solver.solveProbabilityOnes(cls.newBoard)

            cellsProbList = list(cellsWithProbabilities.items())
            cellsProbList.sort(key=lambda x: x[1])
            print(cellsProbList, 'Клетки сложные с возможностями')

            clickLeftList = []
            clickRightList = []
            index = 0
            while index < len(cellsProbList):
                if cellsProbList[index][1] == 0:
                    clickLeftList.append(cellsProbList[index][0])
                    index += 1
                else:
                    break

            while index < len(cellsProbList):
                if cellsProbList[-index][1] > 1:
                    clickRightList.append(cellsProbList[-index][0])
                    index += 1
                else:
                    break

            if len(clickLeftList) == 0 and len(clickRightList) == 0:
                if len(cls.setted_flags) > 9:
                    pg.click(x=1098, y=469, duration=0.5)
                    cls.pastBoard = [[9 for _ in range(cls.numColumns)] for q in range(cls.numRows)]
                    cls.getNewBoard()
                    cls.movesLeft = cls.numColumns * cls.numRows
                    cls.setted_flags = []
                elif len(cellsProbList) == 0:
                    if len(cls.setted_flags) == 9:
                        for i in range(len(cls.newBoard)):
                            for j in range(len(cls.newBoard[0])):
                                if cls.newBoard[i][j] == 9:
                                    clickLeftList.append([i, j])
                    else:
                        time.sleep(100)
                else:
                    print("Taking a minor risk")
                    clickLeftList.append(cellsProbList[0][0])

            if clickRightList:
                pg.click(x=1451, y=466, duration=0.3)
                for coordinate in clickRightList:
                    cls.setted_flags.append([coordinate[1], coordinate[0]])
                    cls.rightClick(coordinate[0], coordinate[1])
                    cls.movesLeft -= 1
                pg.click(x=1451, y=466, duration=0.3)

            for coordinate in clickLeftList:
                cls.leftClick(coordinate[0], coordinate[1])
                cls.movesLeft -= 1

            if cls.movesLeft == 0:
                sys.exit("SOLVED!!!")

            time.sleep(0.1)

            cls.updateBoard()
            cls.movesToExecute = 1

    @classmethod
    def startGame(cls):
        cls.pastBoard = [[9 for _ in range(cls.numColumns)] for q in range(cls.numRows)]
        cls.newBoard = [[9 for _ in range(cls.numColumns)] for q in range(cls.numRows)]
        cls.newgame = False

        cls.movesLeft = cls.numColumns * cls.numRows
        cls.movesToExecute = 1
        cls.setted_flags = []

        pg.click(x=1242, y=726, duration=1)

        cls.getNewBoard()

        for i in range(len(cls.newBoard)):
            for j in range(len(cls.newBoard[0])):
                if cls.newBoard[i][j] == 1 and cls.pastBoard[i][j] != 1:
                    cls.leftClick(j, i)
        time.sleep(0.5)
        cls.game()

    @classmethod
    def getNewBoard(cls):
        cls.newBoard, cls.newgame = Board.getBoard()

    @classmethod
    def getXCoordinate(cls, column):
        return column * cls.pixelX + cls.startX

    @classmethod
    def getYCoordinate(cls, row):
        return row * cls.pixelY + cls.startY

    @classmethod
    def leftClick(cls, column, row):
        pg.click(x=cls.getXCoordinate(column), y=cls.getYCoordinate(row), duration=0.5)

    @classmethod
    def rightClick(cls, column, row):
        pg.click(x=cls.getXCoordinate(column), y=cls.getYCoordinate(row), duration=0.5)

# 1085 581 - середина верхнего левого куба # 1066 562 - верхняя левая граница первого куба # 1103 599 - нижняя правая граница первого куба
# 1163 581 - середина куба правее
# 1084 630 - середина куба ниже

# 80 - расстояние между соседними кубами в одной строчке
# 6 кубов в одной строчке

# 50 - расстояние между соседними кубами в одном столбце
# 9 кубов в одном столбце