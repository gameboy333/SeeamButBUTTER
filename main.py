import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
try:
    import pandas
    import ursina
    import pygame
    import PyQt6
    import preferredsoundplayer
    import Pillow
    import Requests
except:
    os.system("pip install pandas ursina==6.0.0 pygame PyQt6 preferredsoundplayer Pillow Requests")
os.system("python src/main.py")