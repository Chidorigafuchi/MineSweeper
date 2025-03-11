import pyautogui as pg
import time
import numpy as np
from mss import mss
import cv2
import sys


class Board:
    path = r'./sources/minesweeper.txt'

    def __init__(self):
        raise TypeError("Cannot instantiate this class")

    @classmethod
    def reccursion(cls, recc, field, pixels):
        field, pixels, newgame = cls.check_and_click_play_button(field, pixels)  # Анализируем поле снова

        if not (cls.checker(cls.path, field)):  # Если поле не совпало
            field, pixels, newgame = cls.check_and_click_play_button(field, pixels)  # то снова его просматриваем
            if not (
            cls.checker(cls.path, field)):  # если не совпало дважды, то перезаписываем файл и начинаем по новой
                cls.writer(cls.path, field)
                recc += 1
                if recc > 10:
                    sys.exit('Больше 10 рекурсий')
                    return False, field, pixels
                else:
                    return cls.reccursion(recc, field, pixels)
            else:
                return True, field, pixels
        else:  # а если уже совпало то заканчиваем
            return True, field, pixels

    @staticmethod
    def checker(path, field):
        with open(path) as f:
            if (str(field) != f.read()):
                return False
            else:
                return True

    @staticmethod
    def writer(path, field):
        with open(path, 'w') as f:
            f.write(str(field))

    @classmethod
    def check_and_click_play_button(cls, field, pixels):
        def comparison(sct, img, monitor):
            template = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

            img_new = np.array(sct.grab(monitor))
            img_gray = cv2.cvtColor(img_new, cv2.COLOR_BGRA2GRAY)

            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)  # TM_CCOEFF_NORMED,
            loc = np.where(res >= 0.80)  # 0.9 - идеально

            matched_points = list(zip(*loc[::-1]))

            if matched_points:
                pt_x, pt_y = matched_points[0]
                cX = pt_x + monitor["left"]
                cY = pt_y + monitor["top"]
                return cX, cY, True
            else:
                return 0, 0, False

        sct = mss()

        newgame = False

        for top in [819, 936, 977]:
            newX, newY, match = comparison(sct, r'sources\Play_again.jpg',
                                           monitor={'left': 1178, 'top': top, 'width': 202, 'height': 56})
            if match:
                newgame = True
                pg.click(newX, newY, duration=0.5)
                print('Началась новая игра')
                pg.click(x=1242, y=726, duration=1)
                break

        if not match:
            count_x = -1
            for x in range(1085, 1553, 78):

                count_x += 1
                count_y = -1
                for y in range(580, 1021, 50):
                    count_y += 1
                    monitor = {'left': x - 15, 'top': y - 15, 'width': 30, 'height': 30}
                    images = [r'sources\mon1.jpg', r'sources\mon2.jpg', r'sources\mon3.jpg', r'sources\mon4.jpg']

                    pixels[count_x][count_y] = pg.pixel(x - 7, y)

                    if pg.pixel(x, y)[0] < 30:
                        field[count_x][count_y] = 0
                    else:
                        for img in images:
                            newX, newY, match = comparison(sct, img, monitor)

                            if match:
                                field[count_x][count_y] = img[-5]
                                break
            field, pixels = cls.pixel_transform(field, pixels)

        return field, pixels, newgame

    @staticmethod
    def pixel_transform(field, pixels):
        for i in range(9):
            for j in range(6):
                if field[j][i] == -1: field[j][i] = 9
                if field[j][i] == '1' and pixels[j][i][0] < 250 and pixels[j][i][1] < 200: field[j][i] = 3
                if field[j][i] == '1' and pixels[j][i][1] < 200: field[j][i] = 9
                if field[j][i] == '2' and pixels[j][i][0] > 100: field[j][i] = 3
                if field[j][i] == '1' and pixels[j][i][0] < 200: field[j][i] = 2
                if field[j][i] == '[]' and pixels[j][i][0] < 100: field[j][i] = 0
                if field[j][i] != '4' and pixels[j][i][2] > 200: field[j][i] = 4
                if field[j][i] == '2' and pixels[j][i][2] > 150: field[j][i] = 4
        return field, pixels

    @classmethod
    def getBoard(cls):
        field = [[-1 for _ in range(9)] for _ in range(6)]
        pixels = [[-1 for _ in range(9)] for _ in range(6)]

        time.sleep(1)

        field, pixels, newgame = cls.check_and_click_play_button(field, pixels)  # Запускаем анализ поля
        cls.writer(cls.path, field)  # Записываем его в файл

        bol, field, pixels = cls.reccursion(0, field, pixels)

        field = list(zip(*field))
        return field, newgame
