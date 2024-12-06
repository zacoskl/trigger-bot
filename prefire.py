import os
import time
from ctypes import WinDLL
from PIL import Image
from mss import mss
from keyboard import is_pressed, add_hotkey, block_key, unblock_key

def setup_terminal():
    os.system("mode 80,18 & title Prefire & powershell $H=get-host;$W=$H.ui.rawui;$B=$W.buffersize;$B.width=80;$B.height=9999;$W.buffersize=$B;")

def exit_program():
    os.system("echo Press any key to exit . . . & pause >nul")
    exit(0)

ERROR = "\x1b[38;5;255m[\x1b[31m-\x1b[38;5;255m]"
SUCCESS = "\x1b[38;5;255m[\x1b[32m+\x1b[38;5;255m]"
INFO = "\x1b[38;5;255m[\x1b[35m*\x1b[38;5;255m]"

def ensure_requirements():
    try:
        import PIL
        import mss
        import keyboard
    except ModuleNotFoundError:
        print(f"{INFO} Installing required modules...")
        os.system("pip3 install keyboard mss pillow --quiet --no-warn-script-location --disable-pip-version-check")

def load_configuration():
    try:
        with open("config.txt") as f:
            TRIGGER, HIGHLIGHT = [line.strip() for line in f.readlines()]
        print(f"{SUCCESS} Hotkey: {TRIGGER}\n{SUCCESS} Enemy highlight color: {HIGHLIGHT}\n")
    except (FileNotFoundError, ValueError):
        print(f"{ERROR} Missing or invalid config.txt\n")
        HIGHLIGHT = input(f"{INFO} Enemy highlight color\n\n[\x1b[35m1\x1b[38;5;255m] Red (default)\n[\x1b[35m2\x1b[38;5;255m] Purple\n\n> ")
        if HIGHLIGHT not in ["1", "2"]:
            print(f"{ERROR} Invalid choice. Please select 1 or 2.\n")
            exit_program()
        HIGHLIGHT = "red" if HIGHLIGHT == "1" else "purple"
        with open("config.txt", "w") as f:
            f.write(f"Replace this first line with your hotkey (e.g., c or ` or even ctrl + alt + z)\n{HIGHLIGHT}")
        exit_program()

    return TRIGGER, HIGHLIGHT

def set_highlight_color(HIGHLIGHT):
    colors = {
        "red": (152, 20, 37),
        "purple": (250, 100, 250)
    }
    return colors.get(HIGHLIGHT, (152, 20, 37))

def get_mode_selection():
    MODE = input(f"{INFO} Mode\n\n[\x1b[35m1\x1b[38;5;255m] Hold\n[\x1b[35m2\x1b[38;5;255m] Toggle\n\n> ")
    if MODE not in ["1", "2"]:
        print(f"{ERROR} Invalid mode. Please select 1 or 2.\n")
        exit_program()
    return MODE

def initialize_windows_api():
    user32 = WinDLL("user32", use_last_error=True)
    kernel32 = WinDLL("kernel32", use_last_error=True)
    shcore = WinDLL("shcore", use_last_error=True)
    
    shcore.SetProcessDpiAwareness(2)
    
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    
    return user32, kernel32, shcore, screen_width, screen_height

class PopOff:
    def __init__(self, trigger, highlight_rgb, screen_width, screen_height, mode):
        self.trigger = trigger
        self.highlight_rgb = highlight_rgb
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.mode = mode
        self.active = False
        self.TOLERANCE = 20
        self.ZONE = 5
        self.GRAB_ZONE = (int(screen_width / 2 - self.ZONE), int(screen_height / 2 - self.ZONE),
                          int(screen_width / 2 + self.ZONE), int(screen_height / 2 + self.ZONE))

    def switch(self):
        self.active = not self.active
        sound_freq = 700 if self.active else 200
        kernel32.Beep(440, 75)
        kernel32.Beep(sound_freq, 100)

    def search(self):
        start_time = time.perf_counter()
        with mss() as sct:
            img = sct.grab(self.GRAB_ZONE)
        
        pmap = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        
        for x in range(0, self.ZONE * 2):
            for y in range(0, self.ZONE * 2):
                r, g, b = pmap.getpixel((x, y))
                if self.highlight_detected(r, g, b):
                    print(f"\x1b[2A{SUCCESS} Reaction time: {int((time.perf_counter() - start_time) * 1000)}ms")
                    self.handle_key_presses()
                    return

    def highlight_detected(self, r, g, b):
        R, G, B = self.highlight_rgb
        return (R - self.TOLERANCE < r < R + self.TOLERANCE and
                G - self.TOLERANCE < g < G + self.TOLERANCE and
                B - self.TOLERANCE < b < B + self.TOLERANCE)

    def handle_key_presses(self):
        blocked, held = [], []
        if any(user32.GetKeyState(k) > 1 for k in [87, 65, 83, 68]):
            if is_pressed("a"):
                block_key(30)
                blocked.append(30)
                user32.keybd_event(68, 0, 0, 0)
                held.append(68)
            if is_pressed("d"):
                block_key(32)
                blocked.append(32)
                user32.keybd_event(65, 0, 0, 0)
                held.append(65)
            if is_pressed("w"):
                block_key(17)
                blocked.append(17)
                user32.keybd_event(83, 0, 0, 0)
                held.append(83)
            if is_pressed("s"):
                block_key(31)
                blocked.append(31)
                user32.keybd_event(87, 0, 0, 0)
                held.append(87)
            time.sleep(0.1)

        user32.mouse_event(2, 0, 0, 0, 0)
        time.sleep(0.005)
        user32.mouse_event(4, 0, 0, 0, 0)

        for b in blocked:
            unblock_key(b)
        for h in held:
            user32.keybd_event(h, 0, 2, 0)

    def hold(self):
        while True:
            if is_pressed(self.trigger):
                while is_pressed(self.trigger):
                    self.search()
            else:
                time.sleep(0.1)

    def toggle(self):
        add_hotkey(self.trigger, self.switch)
        while True:
            if self.active:
                self.search()
            else:
                time.sleep(0.5)

def main():
    setup_terminal()
    ensure_requirements()
    trigger, highlight = load_configuration()
    highlight_rgb = set_highlight_color(highlight)
    mode = get_mode_selection()
    user32, kernel32, shcore, screen_width, screen_height = initialize_windows_api()

    popoff = PopOff(trigger, highlight_rgb, screen_width, screen_height, mode)

    if mode == "1":
        popoff.hold()
    else:
        popoff.toggle()

if __name__ == "__main__":
    main()
