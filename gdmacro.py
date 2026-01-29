import mouse
import keyboard
import sys
import time
import os
import pyautogui

space_pressed = False
space_event = None

def on_space_press(event):
    global space_pressed, space_event
    if event.name == 'space' and not event.is_keypad:
        if event.event_type == 'down':
            space_pressed = True
            space_event = time.perf_counter()
        elif event.event_type == 'up':
            space_pressed = False

keyboard.hook(on_space_press)

ask = input("Do you wish to record or play back? [r/p] ")

if ask.lower() == 'r':
    while True:
        print('Ready. Recording will start on spacebar press.')
        print('Press E at any time to stop.')
        print('Press R at any time to reset and restart.')

        while not space_pressed:
            if keyboard.is_pressed('e'):
                sys.exit()
            time.sleep(0.001)
        
        while space_pressed:
            if keyboard.is_pressed('e'):
                sys.exit()
            time.sleep(0.001)

        recording = []
        start = time.perf_counter()
        print("Started")

        while True:
            if keyboard.is_pressed('e'):
                break

            if keyboard.is_pressed('r'):
                break

            while not space_pressed:
                if keyboard.is_pressed('e') or keyboard.is_pressed('r'):
                    break
                time.sleep(0.001)
            
            if keyboard.is_pressed('e') or keyboard.is_pressed('r'):
                break
            
            recording.append(time.perf_counter() - start)
            print("PRESS")

            while space_pressed:
                if keyboard.is_pressed('e') or keyboard.is_pressed('r'):
                    break
                time.sleep(0.001)
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

    print("Loaded macro. Will begin playback after spacebar press")
    print("Press E at any time to stop.")

    while not space_pressed:
        time.sleep(0.001)
    
    while space_pressed:
        time.sleep(0.001)

    print("Starting playback...")
    start = time.perf_counter()
    start = start - 0 #manual offset

    for i, t in enumerate(recording):
        if keyboard.is_pressed('e'):
            pyautogui.keyUp('space')
            sys.exit()

        target = start + t
        while True:
            now = time.perf_counter()
            if now >= target:
                break
            time.sleep(min(0.005, target - now))

        if i % 2 == 0:
            pyautogui.keyDown('space')
            print(i, " SPACE DOWN", time.perf_counter() - start)
        else:
            pyautogui.keyUp('space')
            print(i, " SPACE UP")
