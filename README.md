PopOff - Color-Based Trigger System
PopOff is a highly efficient automation tool that allows you to trigger custom actions by detecting specific colors on your screen. Whether you’re gaming, working with color-coded elements, or automating repetitive tasks, PopOff detects highlight colors (such as red or purple) and activates actions like simulating mouse clicks or blocking/unblocking keys. It’s an easy-to-use solution for enhancing your workflow or gaming experience.

Core Features
Color Detection: Monitors your screen for a specific color (e.g., red or purple highlights) in a defined area (typically the center of the screen).
Automated Actions: Triggers customizable actions when the color is detected, such as simulating mouse clicks or blocking certain keys.
Custom Hotkeys: Assign a custom hotkey to control the system, making it easy to toggle or activate color detection on demand.
Hold or Toggle Modes: Choose between "Hold Mode" (activation while holding the hotkey) or "Toggle Mode" (activation/deactivation with a single key press).
How It Works
Color Detection: PopOff continuously scans a portion of your screen for a predefined highlight color (e.g., red or purple).
Triggered Actions: Once the target color is found, PopOff can:
Simulate a mouse click at the location.
Optionally block/unblock keys to prevent unintended actions while active.
Modes:
Hold Mode: The tool remains active as long as the hotkey is held down.
Toggle Mode: The tool activates and deactivates with a single press of the hotkey.
Features at a Glance
Custom Hotkey Activation: Easily assign a hotkey to trigger or toggle color detection.
Action on Color Detection: Detects specific colors and activates corresponding actions (mouse clicks, key blocking).
Flexible Modes: Choose between continuous "Hold Mode" or convenient "Toggle Mode".
Simple Setup: Configuration is stored in an easy-to-edit config.txt file. Adjust the hotkey or highlight color at any time.
Key Blocking: Prevent unwanted key presses while PopOff is active.
Installation
Getting started with PopOff is easy. Follow these simple steps to install:

Ensure that you have Python 3.x installed on your machine.

Install the required libraries by running the following command:

bash
Copy code
pip install keyboard mss pillow
PopOff will automatically try to install any missing dependencies.

Configuration
PopOff allows for quick configuration through a simple config.txt file:

Hotkey: Set your preferred hotkey to trigger or toggle the color detection system.
Highlight Color: Choose which color PopOff should detect (default: red or purple).
Your settings will be saved in the config.txt file, and you can edit it any time to update the hotkey or color.
System Requirements
Operating System: Windows (PopOff uses Windows APIs for system interaction).
Python Version: Python 3.x.
Required Libraries: keyboard, mss, Pillow.
