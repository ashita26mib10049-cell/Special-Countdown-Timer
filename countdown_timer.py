import tkinter as tk
from tkinter import messagebox
import time


class CountdownTimer:

    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.total_seconds = 0
        self.original_seconds = 0
        self.running = False
        self.paused = False
        self.timer_id = None

        title = tk.Label(
            root,
            text="COUNTDOWN TIMER",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=20)

        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(
            input_frame,
            text="Minutes:",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=5)

        self.minute_entry = tk.Entry(
            input_frame,
            width=8,
            font=("Arial", 14),
            justify="center"
        )
        self.minute_entry.grid(row=0, column=1, padx=5)
        self.minute_entry.insert(0, "0")

        tk.Label(
            input_frame,
            text="Seconds:",
            font=("Arial", 12)
        ).grid(row=0, column=2, padx=5)

        self.second_entry = tk.Entry(
            input_frame,
            width=8,
            font=("Arial", 14),
            justify="center"
        )
        self.second_entry.grid(row=0, column=3, padx=5)
        self.second_entry.insert(0, "30")

        self.timer_label = tk.Label(
            root,
            text="00:30",
            font=("Arial", 55, "bold"),
            fg="blue"
        )
        self.timer_label.pack(pady=30)

        self.status_label = tk.Label(
            root,
            text="Ready",
            font=("Arial", 12),
            fg="gray"
        )
        self.status_label.pack()

        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)

        start_button = tk.Button(
            button_frame,
            text="START",
            width=10,
            bg="green",
            fg="white",
            command=self.start_timer
        )
        start_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(
            button_frame,
            text="PAUSE",
            width=10,
            bg="orange",
            command=self.pause_timer
        )
        self.pause_button.grid(row=0, column=1, padx=5)

        reset_button = tk.Button(
            button_frame,
            text="RESET",
            width=10,
            bg="blue",
            fg="white",
            command=self.reset_timer
        )
        reset_button.grid(row=0, column=2, padx=5)

        stop_button = tk.Button(
            button_frame,
            text="STOP",
            width=10,
            bg="red",
            fg="white",
            command=self.stop_timer
        )
        stop_button.grid(row=0, column=3, padx=5)

        tk.Label(
            root,
            text="Timer History",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.history_list = tk.Listbox(
            root,
            width=60,
            height=8
        )
        self.history_list.pack()

        clear_button = tk.Button(
            root,
            text="Clear History",
            command=self.clear_history
        )
        clear_button.pack(pady=10)

    def get_time(self):
        try:
            minutes = int(self.minute_entry.get())
            seconds = int(self.second_entry.get())

            if minutes < 0 or seconds < 0:
                raise ValueError

            if seconds >= 60:
                messagebox.showerror(
                    "Invalid Input",
                    "Seconds must be between 0 and 59."
                )
                return None

            total = minutes * 60 + seconds

            if total <= 0:
                messagebox.showerror(
                    "Invalid Input",
                    "Please enter a time greater than zero."
                )
                return None

            return total

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter numbers only."
            )
            return None

    def start_timer(self):
        if self.running:
            messagebox.showinfo(
                "Timer",
                "Timer is already running."
            )
            return

        total = self.get_time()

        if total is None:
            return

        self.total_seconds = total
        self.original_seconds = total

        self.running = True
        self.paused = False

        self.timer_label.config(fg="blue")

        self.status_label.config(
            text="Timer Running...",
            fg="green"
        )

        self.pause_button.config(text="PAUSE")

        self.add_history("Started")

        self.update_timer()

    def update_timer(self):
        if not self.running:
            return

        if self.paused:
            return

        minutes = self.total_seconds // 60
        seconds = self.total_seconds % 60

        self.timer_label.config(
            text=f"{minutes:02d}:{seconds:02d}"
        )

        if self.total_seconds == 0:
            self.running = False

            self.timer_label.config(
                text="00:00",
                fg="red"
            )

            self.status_label.config(
                text="TIME'S UP!",
                fg="red"
            )

            self.add_history("Completed")

            self.play_alarm()

            messagebox.showinfo(
                "Timer Finished",
                "TIME'S UP!"
            )

            return

        self.total_seconds -= 1

        self.timer_id = self.root.after(
            1000,
            self.update_timer
        )

    def pause_timer(self):
        if not self.running:
            messagebox.showinfo(
                "Timer",
                "Start the timer first."
            )
            return

        if self.paused:
            self.paused = False

            self.status_label.config(
                text="Timer Running...",
                fg="green"
            )

            self.pause_button.config(text="PAUSE")

            self.add_history("Resumed")

            self.update_timer()

        else:
            self.paused = True

            if self.timer_id is not None:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None

            self.status_label.config(
                text="Timer Paused",
                fg="orange"
            )

            self.pause_button.config(text="RESUME")

            self.add_history("Paused")

    def reset_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.running = False
        self.paused = False

        total = self.get_time()

        if total is None:
            return

        self.total_seconds = total
        self.original_seconds = total

        minutes = total // 60
        seconds = total % 60

        self.timer_label.config(
            text=f"{minutes:02d}:{seconds:02d}",
            fg="blue"
        )

        self.status_label.config(
            text="Timer Reset",
            fg="blue"
        )

        self.pause_button.config(text="PAUSE")

        self.add_history("Reset")

    def stop_timer(self):
        if not self.running:
            self.status_label.config(
                text="Timer is not running",
                fg="gray"
            )
            return

        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.running = False
        self.paused = False

        self.status_label.config(
            text="Timer Stopped",
            fg="red"
        )

        self.pause_button.config(text="PAUSE")

        self.add_history("Stopped")

    def add_history(self, status):
        current_time = time.strftime("%H:%M:%S")

        minutes = self.original_seconds // 60
        seconds = self.original_seconds % 60

        information = (
            f"{current_time} | "
            f"{minutes:02d}:{seconds:02d} | "
            f"{status}"
        )

        self.history_list.insert(
            tk.END,
            information
        )

    def clear_history(self):
        self.history_list.delete(
            0,
            tk.END
        )

    def play_alarm(self):
        try:
            import winsound

            winsound.Beep(1000, 500)
            winsound.Beep(1000, 500)
            winsound.Beep(1000, 500)

        except:
            self.root.bell()


if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
