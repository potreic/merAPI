import os
import json
import tkinter as tk
from tkinter import font
from datetime import datetime

CLEAN_DIR = "clean_data"
VOLCANO = "Merapi"
REFRESH_INTERVAL_MS = 60 * 1000  # 1 menit

def get_latest_clean_file():
    files = sorted(
        f for f in os.listdir(CLEAN_DIR)
        if f.startswith(f"{VOLCANO.lower()}_") and f.endswith(".json")
    )
    if not files:
        raise FileNotFoundError("No clean JSON found.")
    return os.path.join(CLEAN_DIR, files[-1])

def load_merapi_data():
    path = get_latest_clean_file()
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    entry = data[VOLCANO]
   
    ts = datetime.fromisoformat(entry["timestamp"])
    
    bulan_id = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    formatted_ts = ts.strftime(f"%d {bulan_id[ts.month]} %Y: %I.%M %p")
    return entry["Status"], formatted_ts

class MerapiStatusUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Merapi Status")
        self.configure(bg="#f0f0f0")
        self.geometry("500x300")
        self.resizable(False, False)

        self.font_title = font.Font(family="Helvetica", size=32, weight="bold")
        self.font_level = font.Font(family="Arial", size=20)
        self.font_time  = font.Font(family="Arial", size=16, slant="italic")

        tk.Label(self, text="Merapi", bg="#f0f0f0", fg="#333333", font=self.font_title)\
          .pack(pady=(30, 10))

        frm_status = tk.Frame(self, bg="#f0f0f0")
        frm_status.pack(pady=5)
        self.canvas_dot = tk.Canvas(frm_status, width=20, height=20,
                                    bg="#f0f0f0", highlightthickness=0)
        self.canvas_dot.pack(side="left", padx=(0, 10))
        self.lbl_level = tk.Label(frm_status, text="", bg="#f0f0f0",
                                  fg="#222222", font=self.font_level)
        self.lbl_level.pack(side="left")

        self.lbl_time = tk.Label(self, text="", bg="#f0f0f0",
                                 fg="#555555", font=self.font_time)
        self.lbl_time.pack(pady=(10, 0))

        self.update_display()

    def update_display(self):
        try:
            status, ts = load_merapi_data()
            
            self.lbl_level.config(text=status)
            self.lbl_time.config(text=ts)

            color_map = {
                "Level I (Normal)":    "#00CC66",  # hijau
                "Level II (Waspada)":  "#FFCC00",  # kuning
                "Level III (Siaga)":   "#FF6600",  # jingga
                "Level IV (Awas)":     "#CC0000",  # merah
            }
            dot_color = color_map.get(status, "#999999")
            self.canvas_dot.delete("all")
            self.canvas_dot.create_oval(2, 2, 18, 18, fill=dot_color)
        except Exception as e:
            self.lbl_level.config(text="Error")
            self.lbl_time.config(text=str(e))
        finally:
            self.after(REFRESH_INTERVAL_MS, self.update_display)

if __name__ == "__main__":
    app = MerapiStatusUI()
    app.mainloop()
