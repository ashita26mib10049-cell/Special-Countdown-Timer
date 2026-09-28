import tkinter as tk
from .timer import CountdownTimer


class TimerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Countdown Timer")
        self.root.geometry("350x250")

        self.label = tk.Label(
            root,
            text="00:00",
            font=("Arial", 40)
        )
        self.label.pack(pady=20)

        self.entry = tk.Entry(root, font=("Arial", 16))
        self.entry.pack()

        self.start_button = tk.Button(
            root,
            text="Start",
            command=self.start_timer
        )
        self.start_button.pack(pady=10)

        self.timer = None

    def start_timer(self):
        try:
            seconds = int(self.entry.get())

            if seconds <= 0:
                self.label.config(text="Enter > 0")
                return

            self.timer = CountdownTimer(seconds)
            self.update_display()

        except ValueError:
            self.label.config(text="Enter seconds")

    def update_display(self):
        if self.timer and not self.timer.is_finished():

            minutes, seconds = divmod(self.timer.seconds, 60)

            self.label.config(
                text=f"{minutes:02d}:{seconds:02d}"
            )

            self.timer.tick()

            self.root.after(1000, self.update_display)

        else:
            self.label.config(text="Time's up!")


def run():
    root = tk.Tk()
    TimerGUI(root)
    root.mainloop()