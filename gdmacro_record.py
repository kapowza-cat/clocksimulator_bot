from pynput import mouse
import keyboard
import sys
import time

mouse_down = False

def wait_until(predicate):
    while not predicate():
        # Allow exit during waits
        if keyboard.is_pressed('e'):
            return False
        time.sleep(0.1)
    return True

def on_click(x, y, _button, pressed):
    global mouse_down
    mouse_down = pressed

# Start listener in the background
listener = mouse.Listener(on_click=on_click)
listener.start()

print(mouse_down)

ask = input("Ready to start? [y/n] ")
if ask.lower() != 'y':
    print('Cancelled')
    sys.exit()

print('Ready. Next click will start recording.')
print('Press E at any time to stop.')

# Wait for first click
if not wait_until(lambda: mouse_down):
    print("Stopped before start.")
    sys.exit()

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
with open("recording.txt", "w") as f:
    for item in recording:
        f.write(str(item) + "\n")

print("Saved to recording.txt")