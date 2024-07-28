import subprocess
import re
import tkinter as tk
from tkinter import ttk
import threading
import time

def get_wifi_signal_strength():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
        match = re.search(r'Signal\s*:\s*(\d+)%', result.stdout)
        if match:
            return int(match.group(1))
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def update_signal_strength(label, progress):
    while True:
        strength = get_wifi_signal_strength()
        if strength is not None:
            label.config(text=f"Wi-Fi Signal Strength: {strength}%")
            progress['value'] = strength
        else:
            label.config(text="Could not determine Wi-Fi signal strength.")
            progress['value'] = 0
        time.sleep(5)

def start_monitoring():
    root = tk.Tk()
    root.title("Wi-Fi Signal Strength Monitor")
    root.geometry("300x150")

    label = ttk.Label(root, text="Initializing...", font=("Arial", 14))
    label.pack(pady=10)

    progress = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
    progress.pack(pady=10)

    threading.Thread(target=update_signal_strength, args=(label, progress), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    start_monitoring()
