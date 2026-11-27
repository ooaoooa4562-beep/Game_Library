"""Launch one of the ten classic games in a separate process."""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
GAMES = ["zmeyka","tetris","pacman","mario","pong","asteroids","breakout","space_invaders","minesweeper","tank_battle"]
def launch(name):
    try:
        subprocess.Popen([sys.executable, str(ROOT / (name + ".py"))], cwd=ROOT)
    except OSError as exc:
        messagebox.showerror("Launch error", str(exc))

def main():
    root = tk.Tk()
    root.title("Game Library — Classic Edition")
    root.geometry("520x460")
    frame = ttk.Frame(root, padding=24)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="Classic Edition", font=("Arial", 22, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
    for i, name in enumerate(GAMES):
        ttk.Button(frame, text=name.replace("_", " ").title(), command=lambda n=name: launch(n)).grid(row=1+i//2, column=i%2, sticky="ew", padx=6, pady=8)
    for i in range(2):
        frame.columnconfigure(i, weight=1)
    root.mainloop()

if __name__ == "__main__":
    main()
