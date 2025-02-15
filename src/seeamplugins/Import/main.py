import requests
import pathlib
import os
from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import simpledialog, messagebox
import shutil
import pathvalidate

# Create the main application window (hidden)
root = tk.Tk()
root.withdraw()  # Hide the root window

# Ask for Steam User ID
steam_id = simpledialog.askstring("Steam User ID", """Please enter your Steam User ID
this can be found in the top bar at [your username] > Account Details, and will appear in small text under your name. """)

# Process the user input
if steam_id:
    uid = steam_id
    root.destroy()
else:
    print("No Steam User ID was entered.")
    root.destroy()






def get_game_library(api_key, user_id):
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={user_id}&format=json"
    response = requests.get(url)
    data = response.json()

    if "response" in data and "games" in data["response"]:
        games = data["response"]["games"]
        return [game["appid"] for game in games]
    else:
        print("Failed to retrieve the game library.")
        return []
    

def get_game_details(api_key, app_ids):
    os.chdir('SeeamApps')
    for app_id in app_ids:
        url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
        response = requests.get(url)
        data = response.json()

        if data and str(app_id) in data and data[str(app_id)]["success"]:
            name = data[str(app_id)]["data"]["name"]
            name = pathvalidate.sanitize_filepath(name)
            name = (name[:20]) if len(name) > 20 else name
            if name[len(name)-1] == ' ': name = name[:19]
            description = data[str(app_id)]["data"]["detailed_description"]
            if os.path.exists(name):
                shutil.rmtree(pathvalidate.sanitize_filepath(name))
            os.makedirs(pathvalidate.sanitize_filepath(name))
            response = requests.get(f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{app_id}/header.jpg")
            img = Image.open(BytesIO(response.content))
            img.save(pathlib.Path(f".\\{name}\\thumbnail.png"))
            with open(f'.\\{name}\\main.py', 'w') as m:
                m.write(f"""
import webbrowser
webbrowser.open(f"steam://rungameid/{app_id}")
                        """)
                m.close()
            with open(f".\\{name}\\description.txt", 'w') as desc:
                try:desc.write(description)
                except:desc.write("dam this description sucks (bad charachter L)")

            #print(f"Game: {name} (App ID: {app_id}), Review Score: {review_score}")
        else:
            print(f"Failed to retrieve game details for App ID: {app_id}")
            print(data)  # Print API response for troubleshooting
    messagebox.showinfo("Steam importer",  "Import Complete! restart seeam for your changes to take affect.") 
api_key="E60936FA0B6D764F62E7D28F0CFD56CA"
app_ids = get_game_library(api_key, uid)
get_game_details(api_key, app_ids)