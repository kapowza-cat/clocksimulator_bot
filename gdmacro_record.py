from pynput import mouse
from pynput.keyboard import Controller, Key
import keyboard
import sys
import time
import os
import threading

kb = Controller()
mouse_pressed = threading.Event()

def wait_until(predicate):
    while not predicate():
        if keyboard.is_pressed('e'):
            return False
        time.sleep(0.005)
    return True

def on_click(x, y, _button, pressed):
    if pressed:
        mouse_pressed.set()
    else:
        mouse_pressed.clear()

listener = mouse.Listener(on_click=on_click)
listener.start()

ask = input("Do you wish to record or play back? [r/p] ")

if ask.lower() == 'r':
    while True:
        print('Ready. Recording will start on mouse release.')
        print('Press E at any time to stop.')
        print('Press R at any time to reset and restart.')

        if not wait_until(mouse_pressed.is_set):
            break
        if not wait_until(lambda: not mouse_pressed.is_set()):
            break

        recording = []
        start = time.perf_counter()
        print("Started")

        while True:
            if keyboard.is_pressed('e'):
                break

            if keyboard.is_pressed('r'):
                break

            if not wait_until(mouse_pressed.is_set):
                break
            recording.append(time.perf_counter() - start)
            print("CLICK")

            if not wait_until(lambda: not mouse_pressed.is_set()):
                break
            recording.append(time.perf_counter() - start)
            print("RELEASE")

        if keyboard.is_pressed('r'):
            time.sleep(0.3)
            continue

        name = input("Enter the name of the text file: ") + ".txt"
        filepath = os.path.join("macros", name)

        os.makedirs("macros", exist_ok=True)
        if os.path.exists(filepath):
            os.remove(filepath)

        with open(filepath, "w") as f:
            for t in recording:
                f.write(f"{t}\n")

        print(f"Saved to {filepath}")
        break

else:
    name = input("Enter name of recording ") + ".txt"
    filepath = os.path.join("macros", name)

    with open(filepath, "r") as f:
        recording = [float(line.strip()) for line in f if line.strip()]

    print("Loaded macro. Will begin playback after next click")
    print("Press E at any time to stop.")

    wait_until(mouse_pressed.is_set)
    wait_until(lambda: not mouse_pressed.is_set())

    print("Starting playback...")
    start = time.perf_counter()
    start = start - 0.1 #manual offset

    for i, t in enumerate(recording):
        if keyboard.is_pressed('e'):
            kb.release(Key.space)
            sys.exit()

        target = start + t
        while True:
            now = time.perf_counter()
            if now >= target:
                break
            time.sleep(min(0.005, target - now))

        if i % 2 == 0:
            print("SPACE DOWN", time.perf_counter() - start)
            kb.press(Key.space)
        else:
            print("SPACE UP")
            kb.release(Key.space)
