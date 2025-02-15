from PyQt6 import QtWidgets, QtGui, QtCore
import os
import importlib
import threading
from pathlib import Path
import json
import preferredsoundplayer.preferredsoundplayer as psp
from PIL import Image

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Utility function for reducing brightness
def reduce_brightness(hex_color, factor=0.5):
    r, g, b = [int(hex_color[i:i + 2], 16) for i in range(1, 6, 2)]
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f"#{r:02x}{g:02x}{b:02x}"
importlib.import_module('seeamplugins.Theme Editor.theme')
# Theme settings
theme = importlib.import_module("seeamplugins.Theme Editor.theme")
BG_COLOR = theme.BG_COLOR
BTN_COLOR = theme.BTN_COLOR
TEXT_COLOR = theme.TEXT_COLOR
TITLE_FONT = QtGui.QFont("Helvetica", 16, QtGui.QFont.Weight.Bold)
BUTTON_FONT = QtGui.QFont("Helvetica", 14)
LABEL_FONT = QtGui.QFont("Helvetica", 12)
SB_COLOR = reduce_brightness(BG_COLOR, 0.7)

# Load user data
user_data_path = Path("assets/userdata.txt")
name = user_data_path.read_text() if user_data_path.exists() else "User"

# Paths
logo_path = Path("assets/SeeamLogo.png")
install_game_script = Path("ServerInstall.py")
games_dir = Path("SeeamApps")
plugins_dir = Path("seeamplugins")

# Function to run scripts
def run_script(script_name):
    def target():
        try:
            psp.playsound('assets/launch.mp3')
            os.system(f'python "{script_name}"')
        except Exception as e:
            print(f"Error running script {script_name}: {e}")
    threading.Thread(target=target, daemon=True).start()

# Main window class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seeam Client")
        self.setWindowIcon(QtGui.QIcon('assets/shortcut.ico'))
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet(f"background-color: {BG_COLOR};")

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Navbar
        self.navbar = QtWidgets.QToolBar()
        self.navbar.setStyleSheet(f"background-color: {SB_COLOR};")
        self.navbar.setIconSize(QtCore.QSize(40, 40))
        self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.navbar)
        
        # Logo
        if logo_path.exists():
            pixmap = QtGui.QPixmap(str(logo_path))
            pixmap = pixmap.scaled(100, 50, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            logo_label = QtWidgets.QLabel()
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.navbar.addWidget(logo_label)
        self.navbar.addWidget(QtWidgets.QLabel("                 "))


        #navbar test
        """
        home_button = QtGui.QAction(QtGui.QIcon('assets/home.png'), "Home", self)
        home_button.triggered.connect(lambda: self.display_welcome())
        self.navbar.addAction(home_button)
        self.navbar.addWidget(QtWidgets.QLabel("Home             "))


        settings_button = QtGui.QAction(QtGui.QIcon('assets/settings.png'), "Settings", self)
        settings_button.triggered.connect(lambda: print("Settings clicked"))
        self.navbar.addAction(settings_button)
        self.navbar.addWidget(QtWidgets.QLabel("Settings         "))"""

        # Plugins
        if plugins_dir.exists():
            for plugin_file in os.listdir(plugins_dir):
                if True:
                    plugin_action = QtGui.QAction(QtGui.QIcon(f'seeamplugins\\{plugin_file}\\icon.png'), plugin_file, self)
                    plugin_action.triggered.connect(lambda checked, script=plugin_file: os.system('python "seeamplugins/' + script + '/main.py"'))
                    self.navbar.addAction(plugin_action)
                    self.navbar.addWidget(QtWidgets.QLabel(plugin_file + "           "))
        
        # Main Layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.main_layout)

        # Games [Scrollable! :)]
        self.sidebar_scroll = QtWidgets.QScrollArea()
        self.sidebar_scroll.setFixedWidth(300)
        self.sidebar_scroll.setStyleSheet(f"background-color: {SB_COLOR};")
        self.sidebar_scroll.setWidgetResizable(True)

        self.sidebar = QtWidgets.QWidget()
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebar_scroll.setWidget(self.sidebar)
        self.main_layout.addWidget(self.sidebar_scroll)

       

        # Available Games Label (unnececary but im not taking it out)
        sidebar_label = QtWidgets.QLabel("My Applications:")
        sidebar_label.setFont(TITLE_FONT)
        sidebar_label.setStyleSheet(f"color: {TEXT_COLOR};")
        self.sidebar_layout.addWidget(sidebar_label)

        # Game Buttons

        if games_dir.exists():
            for game_folder in games_dir.iterdir():
                if game_folder.is_dir():
                    button = QtWidgets.QPushButton(game_folder.name)
                    button.setFont(BUTTON_FONT)
                    button.setStyleSheet(f"background-color: {BTN_COLOR}; color: {TEXT_COLOR};")
                    button.clicked.connect(lambda checked, name=game_folder.name: self.display_game_details(name))
                    self.sidebar_layout.addWidget(button)
        def refreshgames():
            # Remove all widgets from the sidebar layout
            while self.sidebar_layout.count():
                child = self.sidebar_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            # Add the "My Applications" label back
            sidebar_label = QtWidgets.QLabel("My Applications:")
            sidebar_label.setFont(TITLE_FONT)
            sidebar_label.setStyleSheet(f"color: {TEXT_COLOR};")
            self.sidebar_layout.addWidget(sidebar_label)

            # Recreate game buttons
            if games_dir.exists():
                for game_folder in games_dir.iterdir():
                    if game_folder.is_dir():
                        button = QtWidgets.QPushButton(game_folder.name)
                        button.setFont(BUTTON_FONT)
                        button.setStyleSheet(f"background-color: {BTN_COLOR}; color: {TEXT_COLOR};")
                        button.clicked.connect(lambda checked, name=game_folder.name: self.display_game_details(name))
                        self.sidebar_layout.addWidget(button)

            # Re-add the Install More Games button
            if install_game_script.exists():
                install_button = QtWidgets.QPushButton("Install More Games")
                install_button.setFont(BUTTON_FONT)
                install_button.setStyleSheet("background-color: #1abc9c; color: {TEXT_COLOR};")
                install_button.clicked.connect(lambda: run_script(install_game_script))
                self.sidebar_layout.addWidget(install_button)

            # Re-add the Refresh Games button
            refreshbtn = QtWidgets.QPushButton("Refresh games")
            refreshbtn.setFont(BUTTON_FONT)
            refreshbtn.setStyleSheet("background-color: #1abc9c; color: {TEXT_COLOR};")
            refreshbtn.clicked.connect(refreshgames)
            self.sidebar_layout.addWidget(refreshbtn)

            # Add spacer to push content up
            self.sidebar_layout.addStretch()

        # Install Games Button
        if install_game_script.exists():
            install_button = QtWidgets.QPushButton("Install More Games")
            install_button.setFont(BUTTON_FONT)
            install_button.setStyleSheet("background-color: #1abc9c; color: {TEXT_COLOR};")
            install_button.clicked.connect(lambda: run_script(install_game_script))
            self.sidebar_layout.addWidget(install_button)
        
        if True:
            refreshbtn = QtWidgets.QPushButton("Refresh games")
            refreshbtn.setFont(BUTTON_FONT)
            refreshbtn.setStyleSheet("background-color: #1abc9c; color: {TEXT_COLOR};")
            refreshbtn.clicked.connect(refreshgames)
            self.sidebar_layout.addWidget(refreshbtn)

        # Spacer to push content up
        self.sidebar_layout.addStretch()

        # Details page
        self.main_content = QtWidgets.QScrollArea()
        self.main_content_widget = QtWidgets.QWidget()
        self.main_content_layout = QtWidgets.QVBoxLayout(self.main_content_widget)
        self.main_content.setWidget(self.main_content_widget)
        self.main_content.setWidgetResizable(True)
        self.main_layout.addWidget(self.main_content)

        # Initial welcome message
        self.display_welcome()
        

    def display_welcome(self):
        for i in reversed(range(self.main_content_layout.count())):
            widget = self.main_content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        welcome_label = QtWidgets.QLabel(f"Welcome, {name}! Select a game to see details.")
        welcome_label.setFont(TITLE_FONT)
        welcome_label.setStyleSheet(f"color: {TEXT_COLOR};")
        self.main_content_layout.addWidget(welcome_label)


    def display_game_details(self, game_name):
        for i in reversed(range(self.main_content_layout.count())):
            widget = self.main_content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        game_dir = games_dir / game_name
        thumbnail_path = game_dir / "thumbnail.png"
        description_path = game_dir / "description.txt"
        script_path = game_dir / "main.py"
        buttons_json = game_dir / "buttons.json"

        # Thumbnail
        if thumbnail_path.exists():
            pixmap = QtGui.QPixmap(str(thumbnail_path))
            pixmap = pixmap.scaled(800, 450, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            thumbnail_label = QtWidgets.QLabel()
            thumbnail_label.setPixmap(pixmap)
            self.main_content_layout.addWidget(thumbnail_label)

        # Description
        description = description_path.read_text() if description_path.exists() else "No description available."
        description_label = QtWidgets.QLabel(description)
        description_label.setFont(LABEL_FONT)
        description_label.setStyleSheet(f"color: {TEXT_COLOR};")
        description_label.setWordWrap(True)
        self.main_content_layout.addWidget(description_label)

        # Play Button
        play_button = QtWidgets.QPushButton("Play")
        play_button.setFont(BUTTON_FONT)
        play_button.setStyleSheet(f"background-color: {BTN_COLOR}; color: {TEXT_COLOR};")
        play_button.clicked.connect(lambda: run_script(script_path))
        self.main_content_layout.addWidget(play_button)

        # Extra Buttons (NEW JSON SUPPORT! (this took way to long) )
        if buttons_json.exists():
            buttons_data = json.loads(buttons_json.read_text())
            for key, info in buttons_data.items():
                btn = QtWidgets.QPushButton(info['Text'])
                btn.setFont(BUTTON_FONT)
                btn.setStyleSheet(f"background-color: {info['Color']}; color: {TEXT_COLOR};")
                btn.clicked.connect(lambda checked, fp=game_dir / info['File']: run_script(fp))
                self.main_content_layout.addWidget(btn)
app = QtWidgets.QApplication([])
window = MainWindow()
window.showMaximized()
app.exec()