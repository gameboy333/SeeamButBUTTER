import os
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import requests
from urllib.parse import urlparse
import zipfile
import io
from PIL import Image, ImageTk

BG_COLOR = "#d8db34"
BTN_COLOR = "#d8db34"
TEXT_COLOR = "#ffffff"
TITLE_FONT = ("Helvetica", 16, "bold")
BUTTON_FONT = ("Helvetica", 14)
LABEL_FONT = ("Helvetica", 12)

def fetch_data(sheet_url):
    sheet_id = sheet_url.split('/d/')[1].split('/')[0]
    export_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet1'
    data = pd.read_csv(export_url)
    return data

def create_app(data):
    root = tk.Tk()
    root.title("Store App")
    root.configure(bg=BG_COLOR)

    title_label = tk.Label(root, text="Available Programs", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    title_label.pack(pady=20)

    filter_frame = tk.Frame(root, bg=BG_COLOR)
    filter_frame.pack(pady=10)

    filter_label = tk.Label(filter_frame, text="Search (case-insensitive):", font=LABEL_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    filter_label.pack(side=tk.LEFT, padx=5)

    tag_var = tk.StringVar()
    tag_entry = tk.Entry(filter_frame, textvariable=tag_var, font=LABEL_FONT)
    tag_entry.pack(side=tk.LEFT, padx=5)

    def apply_filter():
        tag = tag_var.get().lower()
        filtered_data = data[data['Name'].str.lower().str.contains(tag, na=False)]
        update_programs(filtered_data)

    filter_button = tk.Button(filter_frame, text="Search", command=apply_filter, bg=BTN_COLOR, fg=TEXT_COLOR, font=BUTTON_FONT)
    filter_button.pack(side=tk.LEFT, padx=5)

    app_frame = tk.Frame(root, bg=BG_COLOR)
    app_frame.pack(pady=10)

    current_page = 0
    results_per_page = 10

    def update_programs(filtered_data):
        for widget in app_frame.winfo_children():
            widget.destroy()
        start_index = current_page * results_per_page
        end_index = start_index + results_per_page
        page_data = filtered_data.iloc[start_index:end_index]

        for index, row in page_data.iterrows():
            program_frame = tk.Frame(app_frame, bg=BG_COLOR)
            program_frame.pack(pady=5, padx=10, fill=tk.X)

            app_name = tk.Label(program_frame, text=row['Name'], font=LABEL_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
            app_name.pack(side=tk.LEFT, padx=10)

            # Validate and load the thumbnail
            tiurl = row.get('Thumbnail', None)
            if pd.notnull(tiurl):
                try:
                    img_data = Image.open(requests.get(tiurl, stream=True).raw)
                    img_data = img_data.resize((100, 50))
                    thumbnail = ImageTk.PhotoImage(img_data)
                    thumbnail_label = tk.Label(program_frame, image=thumbnail, bg=BG_COLOR)
                    thumbnail_label.image = thumbnail
                    thumbnail_label.pack(side=tk.LEFT)
                except Exception as e:
                    print(f"Error loading thumbnail: {e}")
                    thumbnail_label = tk.Label(program_frame, text="No Image", font=LABEL_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
                    thumbnail_label.pack(side=tk.LEFT)
            else:
                thumbnail_label = tk.Label(program_frame, text="No Image", font=LABEL_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
                thumbnail_label.pack(side=tk.LEFT)

            # Validate and add download button
            link = row.get('Link', None)
            if pd.notnull(link):
                download_button = tk.Button(program_frame, text="Download", command=lambda url=link: download_app(url), bg=BTN_COLOR, fg=TEXT_COLOR, font=BUTTON_FONT)
                download_button.pack(side=tk.LEFT, padx=10)
            else:
                download_button = tk.Label(program_frame, text="No Link", font=LABEL_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
                download_button.pack(side=tk.LEFT)


        update_pagination(len(filtered_data))

    def update_pagination(total_results):
        for widget in pagination_frame.winfo_children():
            widget.destroy()
        total_pages = (total_results // results_per_page) + (1 if total_results % results_per_page > 0 else 0)

        for i in range(total_pages):
            page_button = tk.Button(pagination_frame, text=str(i + 1), command=lambda page=i: change_page(page), bg=BTN_COLOR, fg=TEXT_COLOR, font=BUTTON_FONT)
            page_button.pack(side=tk.LEFT, padx=5)

    def change_page(page):
        nonlocal current_page
        current_page = page
        apply_filter()

    pagination_frame = tk.Frame(root, bg=BG_COLOR)
    pagination_frame.pack(pady=10)

    update_programs(data)

    root.geometry("1280x720")
    root.mainloop()

def download_app(url):
    if not url or not urlparse(url).scheme:
        messagebox.showerror("Invalid URL", "The provided download URL is invalid.")
        return

    try:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path).replace('%20', ' ').rstrip('.zip')
        path = os.path.join('SeeamApps', filename)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            os.makedirs(path, exist_ok=True)
            zip_file.extractall(path)
            reqs_path = os.path.join(path, "requirements.txt")
            if os.path.exists(reqs_path):
                os.system(f'pip install -r {reqs_path}')
            messagebox.showinfo("Download Complete", f"App downloaded and extracted to {path}")
    except Exception as e:
        messagebox.showerror("Download Error", f"An error occurred while downloading: {e}")



if __name__ == "__main__":
    sheet_url = "https://docs.google.com/spreadsheets/d/1J7uSpw6uCX2e094dMKMh1j3EFYPU4yeKCHWjcIzNMkE/edit?gid=0#gid=0"
    data = fetch_data(sheet_url)
    create_app(data)
