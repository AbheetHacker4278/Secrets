import time
import winsound
import pyttsx3
import threading
import keyboard
import tkinter as tk

# Global variable to indicate if the timer should terminate
terminate_timer = False

def timer(hours, minutes, seconds, label):
    global terminate_timer
    total_seconds = hours * 3600 + minutes * 60 + seconds
    while total_seconds > 0:
        if terminate_timer:
            break
        hrs, remaining_seconds = divmod(total_seconds, 3600)
        mins, secs = divmod(remaining_seconds, 60)
        timer_text = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        label.config(text=timer_text)
        time.sleep(1)
        total_seconds -= 1
    if not terminate_timer:
        label.config(text="Time's up!")
        beep()

def beep():
    frequency = 2500  # Set frequency to 2500 Hz
    duration = 1000  # Set duration to 1000 ms (1 second)
    while True:
        winsound.Beep(frequency, duration)

def get_user_input():
    try:
        engine = pyttsx3.init()
        engine.say("Please enter the number of hours, minutes, and seconds.")
        engine.runAndWait()
        hours = int(input("Enter the number of hours: "))
        minutes = int(input("Enter the number of minutes: "))
        seconds = int(input("Enter the number of seconds: "))
        return hours, minutes, seconds
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return None

def on_key_release(event):
    global terminate_timer
    if event.name == 'q':
        print("\nTimer terminated.")
        terminate_timer = True

def start_timer_gui():
    global terminate_timer
    user_input = get_user_input()
    if user_input is not None:
        hours, minutes, seconds = user_input
        # Create a Tkinter window
        window = tk.Tk()
        window.title("Timer")
        window.geometry("200x100")
        # Create a label to display the timer
        timer_label = tk.Label(window, text="", font=('Helvetica', 24))
        timer_label.pack(pady=10)
        # Start the timer in a separate thread
        timer_thread = threading.Thread(target=timer, args=(hours, minutes, seconds, timer_label))
        timer_thread.start()
        # Listen for the 'q' key to terminate the timer
        keyboard.on_release(on_key_release)
        window.mainloop()

def main():
    start_timer_gui()

if __name__ == "__main__":
    main()
