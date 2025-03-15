import pyautogui
import keyboard
import threading
import screeninfo
import pystray
from PIL import Image, ImageDraw

def center_window_on_monitors():
    """Centers the active window on the middle of monitors it spans, or the single monitor it is on."""
    try:
        active_window = pyautogui.getActiveWindow()
        if active_window:
            window_rect = active_window.box
            if window_rect:
                monitors = find_monitors_window_spans(window_rect.left, window_rect.top, window_rect.width, window_rect.height)

                if monitors:
                    total_width = sum(m.width for m in monitors)
                    total_height = max(m.height for m in monitors)

                    min_x = min(m.x for m in monitors)
                    min_y = min(m.y for m in monitors)

                    window_width = active_window.width
                    window_height = active_window.height

                    x = min_x + (total_width - window_width) // 2
                    y = min_y + (total_height - window_height) // 2

                    active_window.moveTo(x, y)
                else:
                    print("Could not determine monitor(s).")
            else:
                print("Could not get window dimensions.")
        else:
            print("No active window found.")

    except Exception as e:
        print(f"Error centering window: {e}")

def find_monitors_window_spans(x, y, width, height):
    """Finds the monitors that the window spans."""
    monitors = screeninfo.get_monitors()
    spanning_monitors = []
    for monitor in monitors:
        if (monitor.x <= x + width and x <= monitor.x + monitor.width) and \
           (monitor.y <= y + height and y <= monitor.y + monitor.height):
            spanning_monitors.append(monitor)

    return spanning_monitors

def on_hotkey():
    """Handles the Ctrl+Alt hotkey press."""
    center_window_on_monitors()

def hotkey_listener():
    """Listens for the Ctrl+Alt hotkey in a separate thread."""
    keyboard.add_hotkey("ctrl+alt", on_hotkey)
    keyboard.wait()

def create_image():
    """Creates a simple image for the system tray icon."""
    width, height = 64, 64
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=(0, 0, 0)) #simple outline
    draw.rectangle((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill=(0, 0, 255)) # center blue rectangle
    return image

def setup_system_tray():
    """Sets up the system tray icon."""
    image = create_image()
    menu = (pystray.MenuItem("Exit", on_exit),)
    icon = pystray.Icon("Window Centering", image, "Window Centering", menu)
    return icon

def on_exit(icon, item):
    """Exits the application."""
    icon.stop()
    keyboard.unhook_all_hotkeys()
    exit()

def main():
    """Main function to start the hotkey listener."""
    print("Window centering script started. Press Ctrl+Alt to center the active window.")
    hotkey_thread = threading.Thread(target=hotkey_listener)
    hotkey_thread.daemon = True
    hotkey_thread.start()

    system_tray_icon = setup_system_tray()
    system_tray_icon.run()

if __name__ == "__main__":
    main()
