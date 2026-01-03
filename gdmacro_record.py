from pynput import mouse
import keyboard
import sys
import time

mouse_down = False

def wait_until(predicate):
    while not predicate():
        time.sleep(0.1)

def on_click(x, y, _button, pressed):
    global mouse_down
    mouse_down = pressed

# Start listener in the background
listener = mouse.Listener(on_click=on_click)
listener.start()
print(mouse_down)
# Ask for confirmation
ask = input("Ready to start? [y/n] ")
if (ask == 'y'):
    pass
else:
    print('Cancelled')
    sys.exit()
print('Ready. Next click will start recording.')

# Record
wait_until(lambda: mouse_down)
recording = []
time_since_start = time.time()
print("Started")
while True:
    wait_until(lambda: mouse_down)
    recording.append(time.time() - time_since_start)
    print("CLICK")
    wait_until(lambda: not mouse_down)
    recording.append(time.time() - time_since_start)
    print("RELEASE")

with open("recording.txt", "w") as f:
    for item in recording:
        f.write(str(item) + "\n")
