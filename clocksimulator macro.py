import pyautogui
import time
import sys

print("Program started")
time.sleep(2)
screenWidth, screenHeight = pyautogui.size()
pyautogui.click(900,825)
time.sleep(2.3)
print("click 1")
pyautogui.keyDown('space')
pyautogui.keyUp('space')

time.sleep(0.8)
print("click 2")
pyautogui.keyDown('space')
pyautogui.keyUp('space')

# Schedule clicks based on elapsed time since start to avoid drift.
start_time = time.time()
interval = 0.1 # seconds between clicks
next_click_time = start_time + interval

try:
    while True:
        now = time.time()
        if now >= next_click_time:
            pyautogui.keyDown('space')
            elapsed = now - start_time
            print(f"Clicked at {elapsed:.3f}s")
            next_click_time += interval
            pyautogui.keyUp('space')
        else:
            # sleep a short amount to avoid busy loop but wake before next click
            time.sleep(min(next_click_time - now, 0.05))
except KeyboardInterrupt:
    print("Interrupted by user.")
    sys.exit(0)
 