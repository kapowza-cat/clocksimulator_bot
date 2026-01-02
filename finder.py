import pyautogui
import time


while True:
    mousex, mousey = pyautogui.position()
    print(mousex, " ", mousey)
    time.sleep(0.1)

