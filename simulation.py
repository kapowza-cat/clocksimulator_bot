import pyautogui
import time
from pynput import keyboard
import sys
from threading import Event

print("Program started")

screenWidth, screenHeight = pyautogui.size()
allowedToClick = True

# Event used to signal the main loop to stop
stop_event = Event()

def on_press(key):
    try:
        if getattr(key, 'char', None) == 'k':
            allowedToClick = False
            print("K pressed, exiting...")
            stop_event.set()
            return False  # stop the listener thread
    except AttributeError:
        pass

# Start keyboard listener in background
listener = keyboard.Listener(on_press=on_press)
listener.start()

print("Ready?")
ask = input("")
pyautogui.click(900,825)
time.sleep(2.5)

print ("hi")

try:
    while not stop_event.is_set():
        if not stop_event.is_set():
            pyautogui.click()
            print("Clicked")
        time.sleep(1)
finally:
    # Ensure listener is stopped and joined before exiting
    listener.stop()
    listener.join()
    print("Exited.")
    sys.exit(0)