import pyautogui
import time
import sys

print("Program started")

screenWidth, screenHeight = pyautogui.size()

print("Ready?")
ask = input("")
pyautogui.click(900,825)
time.sleep(2.3)
print("firstclick")

while True:
    pyautogui.keyDown("space")
    print("Clicked")
    pyautogui.keyUp("space")
    time.sleep(1)
