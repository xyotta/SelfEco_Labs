from Client import GameClient
from Stats import Stats
import tkinter as tk


class Overlay:
    def __init__(self):
        self.client = GameClient()
        self.stats_logic = Stats()

        self.window = tk.Tk()
        self.window.title("SeltECO Overlay")

        window_width = 300
        window_height = 150
        screen_width = self.window.winfo_screenwidth()
        x_pos = screen_width - window_width - 20
        y_pos = 50
        self.window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        self.window.attributes("-topmost", True)
        self.window.configure(bg='black')
        self.window.overrideredirect(True)
        self.window.attributes("-alpha", 0.7)

        # Рух вікна
        self.window.bind('<Button-1>', self.start_move)
        self.window.bind('<B1-Motion>', self.do_move)

        self.close_btn = tk.Button(self.window, text="X", command=self.window.destroy, bg="red", fg="white",
                                   font=("Arial", 8))
        self.close_btn.pack(anchor="ne", padx=5, pady=5)

        self.label_gpm = tk.Label(self.window, text="Waiting...", font=("Arial", 16, "bold"), fg="#FFD700", bg="black")
        self.label_gpm.pack(pady=5)

        self.label_cspm = tk.Label(self.window, text="---", font=("Arial", 14), fg="white", bg="black")
        self.label_cspm.pack(pady=5)

        self.label_status = tk.Label(self.window, text="Init...", font=("Arial", 8), fg="gray", bg="black")
        self.label_status.pack(side="bottom", pady=5)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.window.winfo_x() + (event.x - self.x)
        y = self.window.winfo_y() + (event.y - self.y)
        self.window.geometry(f"+{x}+{y}")

    def update_display(self):
        raw_data = self.client.get_game_data()

        if raw_data:
            gold, cs, time = self.client.parse_player_stats(raw_data)


            self.stats_logic.update_stats(gold, cs, time)


            gpm = self.stats_logic.calculate_gpm()
            cspm = self.stats_logic.calculate_cspm()

            if time < 60:
                gpm_text = "GPM: Warmup..."
                cspm_val = 0.0
            else:
                gpm_text = f"GPM: {gpm:.1f}"
                cspm_val = cspm

            self.label_gpm.config(text=gpm_text)
            self.label_cspm.config(text=f"CSPM: {cspm_val:.1f} (CS: {cs})")

            self.label_status.config(text=f"Time: {time:.0f}s | OK", fg="green")
        else:
            self.label_status.config(text="Searching for LoL...", fg="red")

        self.window.after(1000, self.update_display)

    def run(self):
        self.update_display()
        self.window.mainloop()