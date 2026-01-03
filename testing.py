from pynput import mouse, keyboard
import time

last_event_time = time.time()

def report_event(event_name):
    global last_event_time
    now = time.time()
    elapsed = now - last_event_time
    print(f"{event_name} — time since last event: {elapsed:.3f} seconds")
    last_event_time = now

# Mouse listener
def on_click(x, y, button, pressed):
    if pressed:
        report_event(f"Mouse {button} pressed at ({x}, {y})")

# Keyboard listener
def on_press(key):
    try:
        if key == keyboard.Key.space:
            report_event("Space key pressed")
    except AttributeError:
        pass  # Special keys don't have .char

print("Tracking time since last spacebar or mouse press...")
print("Press Ctrl+C to stop.")

with mouse.Listener(on_click=on_click) as ml, \
     keyboard.Listener(on_press=on_press) as kl:
    ml.join()
    kl.join()