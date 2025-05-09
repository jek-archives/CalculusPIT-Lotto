#  /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m pip show matplotlib
#  /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 ~/Desktop/LottoApp.py

import random
from itertools import combinations
from collections import Counter
import tkinter as tk
from tkinter import ttk, filedialog
import csv
import matplotlib.pyplot as plt
from datetime import datetime

class LottoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Megalotto 6/45")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window size
        window_width = 820
        window_height = 600

        # Calculate the position to center the window
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)

        # Set geometry of the window
        self.root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
        self.root.configure(bg="#ECF0F1")
        self.root.minsize(720, 500)

        # --- Style & Data ---
        self.FONT_TITLE = ("Helvetica", 22, "bold")
        self.FONT_LABEL = ("Helvetica", 16, "bold")
        self.FONT_BTN = ("Helvetica", 12)
        self.COLOR_PRIMARY = "#2980B9"
        self.COLOR_ACCENT = "#27AE60"
        self.COLOR_BG = "#FFC0CB"
        self.COLOR_LABEL_BG = "#34495E"
        self.COLOR_LABEL_TEXT = "white"
        self.all_combinations = list(combinations(range(1, 46), 6))
        self.lucky_labels = []
        self.frequency = Counter()
        self.history = []

        self.build_ui()


    def build_ui(self):
        main_frame = tk.Frame(self.root, bg=self.COLOR_BG, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        title = tk.Label(main_frame, text="MEGALOTTO", font=("Anton", 22, "bold"),
                         fg="#FBBF24", bg="red", padx=10, pady=5)
        title.pack()

        # Subtitle label (6/45)
        lotto_label = tk.Label(main_frame, text="6/45", font=("Anton", 69, "bold"),
                               fg="#1a1a66", bg="white")
        lotto_label.pack(pady=(0, 20))

        # Date (Time) Display at Top Left
        self.time_label = tk.Label(main_frame, text="", font=("Helvetica", 12), fg="#2C3E50", bg=self.COLOR_BG)
        self.time_label.place(x=20, y=10)  # Position at the top-left corner
        self.update_time_and_date()

        # LUCKY NUMBERS label positioned just below the title
        lucky_numbers_label = tk.Label(main_frame, text="LUCKY NUMBERS", font=("Helvetica", 16, "bold"),
                                       fg="#2C3E50", bg=self.COLOR_BG)
        lucky_numbers_label.place(relx=0.5, y=160, anchor="center")  
        
        # Lucky Number Display
        lucky_frame = tk.Frame(main_frame, bg=self.COLOR_BG)
        lucky_frame.pack(pady=30)
        for i in range(6):
            lbl = tk.Label(lucky_frame, text="--", font=self.FONT_LABEL,
                           width=4, height=2, bg=   self.COLOR_LABEL_BG,
                           fg=self.COLOR_LABEL_TEXT, relief="groove", bd=2)
            lbl.grid(row=0, column=i, padx=8, sticky="ew")  # Allow grid cells to expand
            self.lucky_labels.append(lbl)

        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.COLOR_BG)
        button_frame.pack(pady=20, fill="x")
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Create and store buttons
        self.buttons = []

        self.buttons.append(tk.Button(button_frame, text="🔁 Regenerate Numbers",
                                      command=self.refresh_lucky_numbers))
        self.buttons.append(tk.Button(button_frame, text="📊 Frequency Table",
                                      command=self.show_frequencies))
        self.buttons.append(tk.Button(button_frame, text="📊 Show Bar Chart",
                                      command=self.show_bar_chart))
        self.buttons.append(tk.Button(button_frame, text="📥 Export History",
                                      command=self.save_history_to_csv))

        # Place the buttons
        self.buttons[0].grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.buttons[1].grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.buttons[2].grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.buttons[3].grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        # Apply uniform styling to all buttons
        for btn in self.buttons:
            btn.configure(font=self.FONT_BTN, bg=self.COLOR_PRIMARY, fg="black", height=2, padx=8, pady=6)

        # History Section
        history_frame = tk.LabelFrame(main_frame, text="Generated History", font=self.FONT_BTN, bg=self.COLOR_BG, fg="#2C3E50")
        history_frame.pack(fill="both", expand=True, pady=10)
        self.history_listbox = tk.Listbox(history_frame, height=10, font=("Courier", 12))
        self.history_listbox.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        # Ensure that history section resizes well
        history_frame.grid_rowconfigure(0, weight=1)
        history_frame.grid_columnconfigure(0, weight=1)

    def update_time_and_date(self):
        # Update time and date
        current_time = datetime.now().strftime("%A, %B %d, %Y - %I:%M:%S %p")
        self.time_label.config(text=current_time)

        # Update every second
        self.root.after(1000, self.update_time_and_date)

    def refresh_lucky_numbers(self):
        new_picks = random.choices(self.all_combinations, k=1000)
        flat = [num for combo in new_picks for num in combo]
        self.frequency = Counter(flat)
        top_6 = sorted([num for num, _ in self.frequency.most_common(6)])
        timestamp = datetime.now().strftime("%A, %B %d, %Y - %I:%M:%S %p")
        display = f"{timestamp}  {' '.join(f'{n:02}' for n in top_6)}"
        self.history_listbox.insert(0, display)
        self.history.append(f"{timestamp}  {' '.join(f'{n:02}' for n in top_6)}")

        for i, num in enumerate(top_6):
            self.lucky_labels[i].config(text=f"{num:02}", bg=self.COLOR_PRIMARY)

    def show_frequencies(self):
        freq_window = tk.Toplevel(self.root)
        freq_window.title("📊 Frequency Table")
        freq_window.geometry("400x500")
        freq_window.configure(bg=self.COLOR_BG)

        label = tk.Label(freq_window, text="Number Frequencies", font=("Helvetica", 16, "bold"),
                         bg=self.COLOR_BG, fg="#2C3E50")
        label.pack(pady=(10, 5))

        tree = ttk.Treeview(freq_window, columns=("Number", "Count"), show="headings", height=20)
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
        nums = [num for num, _ in sorted(self.frequency.items())]
        counts = [self.frequency[num] for num in nums]

        plt.figure(figsize=(12, 6))
        plt.bar(nums, counts, color="#2980B9")
        plt.title("Number Frequency (Lotto 6/45)")
        plt.xlabel("Number")
        plt.ylabel("Times Drawn")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    def save_history_to_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv")],
                                                title="Save History Data")
        if filename:
            with open(filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Date & Time", "Numbers"])
                for entry in reversed(self.history_listbox.get(0, tk.END)):
                    writer.writerow([entry.split()[0], " ".join(entry.split()[1:])])
            print(f"History saved to {filename}")

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LottoApp(root)
    root.mainloop()
