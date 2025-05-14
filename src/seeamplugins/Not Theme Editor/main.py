import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

if messagebox.askyesno("Too Bad","There is no theme editor for you."):
    root.destroy()
else:
    whay = messagebox.askokcancel("No.","There really isn't.")
    root.destroy()