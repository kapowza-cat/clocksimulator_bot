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
        time.sleep(0.01)
    return True

def on_click(x, y, _button, pressed):
    global mouse_down
    mouse_down = pressed

# Start listener in the background
listener = mouse.Listener(on_click=on_click)
listener.start()


ask = input("Do you wish to record or play back? [r/p] ")
if ask.lower() == 'r':
    print('Ready. Recording will start on mouse release.')
    print('Press E at any time to stop.')

    # Use existing funtions to wait until first click, but only start when mouse is RELEASED
    wait_until(lambda: mouse_down)
    wait_until(lambda: not mouse_down)
    

    recording = []
    time_since_start = time.time()
    print("Started")

    while True:
        # Stop if E pressed
        if keyboard.is_pressed('e'):
            print("Stopping...")
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

    # Save results
    if os.path.exists("recording.txt"):
        os.remove("recording.txt")
    with open("recording.txt", "w") as f:
        for item in recording:
            f.write(str(item) + "\n")

    print("Saved to recording.txt")
else:
    recording = []

    with open("recording.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:  # skip empty lines
                recording.append(float(line))

    print(recording)
    print("Loaded macro. Will begin playback after next click")
    # begin playback, clicking spacebar when the time has elapsed to equal the number and releasing when it equals the next, and so on
    print("Press E at any time to stop.")
    wait_until(lambda: mouse_down)
    wait_until(lambda: not mouse_down)
    print("Starting playback...")
    time_since_start = time.time()
    for t in recording:
        # Stop if E pressed
        if keyboard.is_pressed('e'):
            print("Stopping...")
            break

        # Wait until the right time
        while time.time() - time_since_start < t:
            if keyboard.is_pressed('e'):
                print("Stopping...")
                sys.exit()
            time.sleep(0.01)

        # Determine if this is a press or release
        index = recording.index(t)
        if index % 2 == 0:
            print("SPACE DOWN")
            keyboard.press('space')
        else:
            print("SPACE UP")
            keyboard.release('space')