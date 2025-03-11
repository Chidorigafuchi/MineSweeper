import webbrowser
import pyautogui as pg
from classes.game import Game


def open_coinsweeper():
    webbrowser.get(using='windows-default').open_new_tab('https://web.telegram.org/k/#@BybitCoinsweeper_Bot')
    pg.click(x=1196, y=1351, duration=5)
    pg.click(x=1279, y=908, duration=2)
    pg.click(x=1278, y=800, duration=1)
    pg.click(x=1062, y=469, duration=0.1)


if __name__ == "__main__":
    open_coinsweeper()

    Game.startGame()
