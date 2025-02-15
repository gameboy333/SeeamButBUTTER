import tkinter as tk
from tkinter import colorchooser, font, messagebox
import theme
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
class VariableEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Theme Editor")

        # Initialize variables
        self.BG_COLOR = theme.BG_COLOR
        self.BTN_COLOR = theme.BTN_COLOR
        self.TEXT_COLOR = theme.TEXT_COLOR
        self.TITLE_FONT = theme.TITLE_FONT
        self.BUTTON_FONT = theme.BUTTON_FONT
        self.LABEL_FONT = theme.LABEL_FONT

        # UI Elements
        self.create_ui()

    def create_ui(self):
        # Button Color
        tk.Label(self.master, text="Button Color:", font=self.LABEL_FONT).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.btn_color_display = tk.Label(self.master, text=self.BTN_COLOR, bg=self.BTN_COLOR, width=10)
        self.btn_color_display.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.master, text="Pick Color", command=self.change_btn_color, font=self.BUTTON_FONT).grid(row=0, column=2, padx=10, pady=5)

        # Text Color
        tk.Label(self.master, text="Text Color:", font=self.LABEL_FONT).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.text_color_display = tk.Label(self.master, text=self.TEXT_COLOR, bg=self.TEXT_COLOR, width=10)
        self.text_color_display.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.master, text="Pick Color", command=self.change_text_color, font=self.BUTTON_FONT).grid(row=1, column=2, padx=10, pady=5)

        tk.Label(self.master, text="BG Color:", font=self.LABEL_FONT).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.bg_color_display = tk.Label(self.master, text=self.BG_COLOR, bg=self.BG_COLOR, width=10)
        self.bg_color_display.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.master, text="Pick Color", command=self.change_bg_color, font=self.BUTTON_FONT).grid(row=2, column=2, padx=10, pady=5)

        # Title Font
        tk.Label(self.master, text="Title Font:", font=self.LABEL_FONT).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.title_font_display = tk.Label(self.master, text=str(self.TITLE_FONT))
        self.title_font_display.grid(row=3, column=1, padx=10, pady=5, columnspan=2, sticky="w")

        # Button Font
        tk.Label(self.master, text="Button Font:", font=self.LABEL_FONT).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.button_font_display = tk.Label(self.master, text=str(self.BUTTON_FONT))
        self.button_font_display.grid(row=4, column=1, padx=10, pady=5, columnspan=2, sticky="w")

        # Label Font
        tk.Label(self.master, text="Label Font:", font=self.LABEL_FONT).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.label_font_display = tk.Label(self.master, text=str(self.LABEL_FONT))
        self.label_font_display.grid(row=5, column=1, padx=10, pady=5, columnspan=2, sticky="w")

        # Save Button
        tk.Button(self.master, text="Save Changes", command=self.save_changes, font=self.BUTTON_FONT).grid(row=6, column=0, columnspan=3, pady=10)

    def change_btn_color(self):
        color_code = colorchooser.askcolor(title="Choose Button Color", initialcolor=self.BTN_COLOR)[1]
        if color_code:
            self.BTN_COLOR = color_code
            self.btn_color_display.config(text=color_code, bg=color_code)

    def change_bg_color(self):
        color_code = colorchooser.askcolor(title="Choose Button Color", initialcolor=self.BG_COLOR)[1]
        if color_code:
            self.BG_COLOR = color_code
            self.bg_color_display.config(text=color_code, bg=color_code)

    def change_text_color(self):
        color_code = colorchooser.askcolor(title="Choose Text Color", initialcolor=self.TEXT_COLOR)[1]
        if color_code:
            self.TEXT_COLOR = color_code
            self.text_color_display.config(text=color_code, bg=color_code)

    def save_changes(self):
        variables = (f'''
BG_COLOR= "{self.BG_COLOR}"
BTN_COLOR= "{self.BTN_COLOR}"
TEXT_COLOR= "{self.TEXT_COLOR}"
TITLE_FONT= {self.TITLE_FONT}
BUTTON_FONT= {self.BUTTON_FONT}
LABEL_FONT= {self.LABEL_FONT}
                     '''
        )
        with open("./theme.py", 'w') as file:
            variables.replace("#","")
            file.write(variables)
        messagebox.showinfo("Save Changes", "Theme saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = VariableEditor(root)
    root.mainloop()
