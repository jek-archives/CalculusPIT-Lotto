import random
from itertools import combinations
from collections import Counter
from datetime import datetime
import csv

import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt

# Constants
WINDOW_WIDTH = 820
WINDOW_HEIGHT = 600
MIN_WINDOW_WIDTH = 720
MIN_WINDOW_HEIGHT = 500

FONT_TITLE = ("Helvetica", 22, "bold")
FONT_LABEL = ("Helvetica", 16, "bold")
FONT_BTN = ("Helvetica", 12)

COLOR_PRIMARY = "#2980B9"
COLOR_ACCENT = "#27AE60"
COLOR_BG = "#FFC0CB"
COLOR_LABEL_BG = "#34495E"
COLOR_LABEL_TEXT = "white"


class LottoApp:
    """
    A GUI application for generating and analyzing Megalotto 6/45 numbers.
    """

    def __init__(self, root):
        """
        Initialize the LottoApp with the main Tkinter root window.
        """
        self.root = root
        self.root.title("Megalotto 6/45")

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position to center the window
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2

        # Set window geometry and position
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.root.configure(bg=COLOR_BG)

        # Data and UI elements
        self.lucky_labels = []
        self.frequency = Counter()
        self.history = []
        self.all_combinations = self.generate_combinations()

        # Build the UI
        self.build_ui()

    def generate_combinations(self):
        """
        Generate all possible combinations of 6 numbers from 1 to 45.
        """
        return list(combinations(range(1, 46), 6))

    def build_ui(self):
        """
        Build the main user interface for the LottoApp.
        """
        self.create_main_frame()
        self.create_title_section()
        self.create_lucky_numbers_section()
        self.create_buttons()
        self.create_history_section()

    def create_main_frame(self):
        """
        Create the main frame for the application.
        """
        self.main_frame = tk.Frame(self.root, bg=COLOR_BG, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill="both")

    def create_title_section(self):
        """
        Create the title and subtitle section.
        """
        title = tk.Label(
            self.main_frame,
            text="MEGALOTTO",
            font=("Anton", 22, "bold"),
            fg="#FBBF24",
            bg="red",
            padx=10,
            pady=5,
        )
        title.pack()

        lotto_label = tk.Label(
            self.main_frame,
            text="6/45",
            font=("Anton", 69, "bold"),
            fg="#1a1a66",
            bg="white",
        )
        lotto_label.pack(pady=(0, 20))

        self.time_label = tk.Label(
            self.main_frame,
            text="",
            font=("Helvetica", 12),
            fg="#2C3E50",
            bg=COLOR_BG,
        )
        self.time_label.place(x=20, y=10)
        self.update_time_and_date()

    def create_lucky_numbers_section(self):
        """
        Create the section to display lucky numbers.
        """
        lucky_numbers_label = tk.Label(
            self.main_frame,
            text="LUCKY NUMBERS",
            font=("Helvetica", 16, "bold"),
            fg="#2C3E50",
            bg=COLOR_BG,
        )
        lucky_numbers_label.place(relx=0.5, y=160, anchor="center")

        lucky_frame = tk.Frame(self.main_frame, bg=COLOR_BG)
        lucky_frame.pack(pady=30)

        for i in range(6):
            lbl = tk.Label(
                lucky_frame,
                text="--",
                font=FONT_LABEL,
                width=4,
                height=2,
                bg=COLOR_LABEL_BG,
                fg=COLOR_LABEL_TEXT,
                relief="groove",
                bd=2,
            )
            lbl.grid(row=0, column=i, padx=8, sticky="ew")
            self.lucky_labels.append(lbl)

    def create_buttons(self):
        """
        Create the buttons for user actions.
        """
        button_frame = tk.Frame(self.main_frame, bg=COLOR_BG)
        button_frame.pack(pady=20, fill="x")
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.buttons = [
            tk.Button(
                button_frame,
                text="🔁 Regenerate Numbers",
                command=self.refresh_lucky_numbers,
            ),
            tk.Button(
                button_frame, text="📈 Frequency Table", command=self.show_frequencies
            ),
            tk.Button(
                button_frame, text="📊 Show Bar Chart", command=self.show_bar_chart
            ),
            tk.Button(
                button_frame, text="📥 Export History", command=self.save_history_to_csv
            ),
        ]

        # Place buttons
        self.buttons[0].grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.buttons[1].grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.buttons[2].grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.buttons[3].grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        # Style buttons
        for btn in self.buttons:
            btn.configure(
                font=FONT_BTN,
                bg=COLOR_PRIMARY,
                fg="black",
                height=2,
                padx=8,
                pady=6,
            )

    def create_history_section(self):
        """
        Create the history section to display generated numbers.
        """
        history_frame = tk.LabelFrame(
            self.main_frame,
            text="Generated History",
            font=FONT_BTN,
            bg=COLOR_BG,
            fg="#2C3E50",
        )
        history_frame.pack(fill="both", expand=True, pady=10)

        self.history_listbox = tk.Listbox(
            history_frame, height=10, font=("Courier", 12)
        )
        self.history_listbox.pack(
            side="left", fill="both", expand=True, padx=(5, 0), pady=5
        )

        scrollbar = ttk.Scrollbar(
            history_frame, orient="vertical", command=self.history_listbox.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

    def update_time_and_date(self):
        """
        Update the time and date displayed in the UI.
        """
        current_time = datetime.now().strftime("%A, %B %d, %Y - %I:%M:%S %p")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time_and_date)

    def refresh_lucky_numbers(self):
        """
        Refresh the lucky numbers with a spinning animation.
        """
        def spin_numbers():
            for lbl in self.lucky_labels:
                lbl.config(text=f"{random.randint(1, 45):02}", bg=COLOR_LABEL_BG)
            self.root.update()

        def stop_spinning():
            new_picks = random.choices(self.all_combinations, k=1000)
            flat = [num for combo in new_picks for num in combo]
            self.frequency = Counter(flat)
            top_6 = sorted([num for num, _ in self.frequency.most_common(6)])
            timestamp = datetime.now().strftime("%A, %B %d, %Y - %I:%M:%S %p")
            display = f"{timestamp}  {' '.join(f'{n:02}' for n in top_6)}"
            self.history_listbox.insert(0, display)
            self.history.append(display)

            for i, num in enumerate(top_6):
                self.lucky_labels[i].config(text=f"{num:02}", bg=COLOR_PRIMARY)

        for _ in range(20):
            spin_numbers()
            self.root.after(50)

        stop_spinning()

    def show_frequencies(self):
        """
        Display a frequency table of the generated numbers.
        """
        freq_window = tk.Toplevel(self.root)
        freq_window.title("📈 Frequency Table")
        freq_window.geometry("400x500")
        freq_window.configure(bg=COLOR_BG)

        label = tk.Label(
            freq_window,
            text="Number Frequencies",
            font=("Helvetica", 16, "bold"),
            bg=COLOR_BG,
            fg="#2C3E50",
        )
        label.pack(pady=(10, 5))

        tree = ttk.Treeview(
            freq_window, columns=("Number", "Count"), show="headings", height=20
        )
        tree.heading("Number", text="Number")
        tree.heading("Count", text="Times Drawn")
        tree.column("Number", width=100, anchor="center")
        tree.column("Count", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(freq_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        sorted_freq = sorted(self.frequency.items())
        for num, count in sorted_freq:
            tree.insert("", "end", values=(f"{num:02}", count))

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    def show_bar_chart(self):
        """
        Display a bar chart of the number frequencies.
        """
        nums = [num for num, _ in sorted(self.frequency.items())]
        counts = [self.frequency[num] for num in nums]

        plt.figure(figsize=(12, 6))
        plt.bar(nums, counts, color=COLOR_PRIMARY)
        plt.title("Number Frequency (Lotto 6/45)")
        plt.xlabel("Number")
        plt.ylabel("Times Drawn")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    def save_history_to_csv(self):
        """
        Save the history of generated numbers to a CSV file.
        """
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save History Data",
            )
            if filename:
                with open(filename, mode="w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Date & Time", "Numbers"])
                    for entry in reversed(self.history_listbox.get(0, tk.END)):
                        writer.writerow([entry.split()[0], " ".join(entry.split()[1:])])
                print(f"History saved to {filename}")
        except Exception as e:
            print(f"Error saving history: {e}")


# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LottoApp(root)
    root.mainloop()