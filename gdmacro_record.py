from pynput import mouse
import keyboard
import sys
import time
import os

mouse_down = False

def wait_until(predicate):
    while not predicate():
        # Allow exit during waits
        if keyboard.is_pressed('e'):
            return False
        time.sleep(0.001)
    return True

def on_click(x, y, _button, pressed):
    global mouse_down
    mouse_down = pressed

# Start listener in the background
listener = mouse.Listener(on_click=on_click)
listener.start()


ask = input("Do you wish to record or play back? [r/p] ")
if ask.lower() == 'r':
    while True:  # Allows restarting after R
        print('Ready. Recording will start on mouse release.')
        print('Press E at any time to stop.')
        print('Press R at any time to reset and restart.')

        # Wait for first click → release
        if not wait_until(lambda: mouse_down):
            print("Stopped before start.")
            break
        if not wait_until(lambda: not mouse_down):
            print("Stopped before start.")
            break

        recording = []
        time_since_start = time.time()
        print("Started")

        while True:
            # Stop if E pressed
            if keyboard.is_pressed('e'):
                print("Stopping...")
                break

            # Reset if R pressed
            if keyboard.is_pressed('r'):
                print("Resetting recording...")
                # Break out of inner loop and restart outer loop
                break

            # Wait for press
            if not wait_until(lambda: mouse_down):
                print("Stopping...")
                break
            recording.append(time.time() - time_since_start)
            print("CLICK")

            # Wait for release
            if not wait_until(lambda: not mouse_down):
                print("Stopping...")
                break
            recording.append(time.time() - time_since_start)
            print("RELEASE")

        # If R was pressed, restart without saving
        if keyboard.is_pressed('r'):
            # Small delay to avoid instantly re-triggering R
            time.sleep(0.3)
            continue

        # If E was pressed, save and exit
        ask = input("Enter the name of the text file: ")
        ask = (f"{ask}.txt")
        filepath = os.path.join("macros", ask)
        if os.path.exists(filepath):
            os.remove(filepath)
        with open(filepath, "w") as f:
            for item in recording:
                f.write(str(item) + "\n")

        print(f"Saved to {filepath}")
        break  # Exit outer loop after saving

else:
    recording = []
    ask = input("Enter name of recording ")
    ask = (f"{ask}.txt")
    filepath = os.path.join("macros", ask)

    recording = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                recording.append(float(line))


    print(recording)
    print("Loaded macro. Will begin playback after next click")
    # begin playback, clicking spacebar when the time has elapsed to equal the number and releasing when it equals the next, and so on
    print("Press E at any time to stop.")
    wait_until(lambda: mouse_down)
    wait_until(lambda: not mouse_down)
    print("Starting playback...")
    time_since_start = time.time()
    time_since_start += -0.02 #Manual offset
    for t in recording:
        # Stop if E pressed
        if keyboard.is_pressed('e'):
            print("Stopping...")
            keyboard.release('space')
            break

        # Wait until the right time
        while time.time() - time_since_start < t:
            if keyboard.is_pressed('e'):
                print("Stopping...")
                keyboard.release('space')
                sys.exit()
            time.sleep(0.001)

        # Determine if this is a press or release
        index = recording.index(t)
        if index % 2 == 0:
            print("SPACE DOWN ", time.time()-time_since_start)
            keyboard.press('space')
        else:
            print("SPACE UP")
            keyboard.release('space')