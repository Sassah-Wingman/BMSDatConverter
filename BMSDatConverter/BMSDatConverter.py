# This is a application designed to convert .dat files to proto for Falcon BMS 
# using Pysimplegui 3.17.
# Sao Paulo, Brazil
# jun 2024
#__version__ = "1.0 - jun 2024"

import PySimpleGUI as sg
import os
#my moodules
import MyWindows
import MyFunctions

#global configurations
__version__ = "v1.0 - 2024."
sg.set_options(font = "Arial, 14")
BMSBlueGray = {'BACKGROUND': '#91a6be',
             "TEXT": "#000000",
             "INPUT": "#ffffff",
             "TEXT_INPUT": "#000000",
             "SCROLL": "#64778d",
             "BUTTON": ("#ffffff", "#4b586e"),
             "PROGRESS": ("#64778d", "#d4d7dd"),
             "BORDER": 1, "SLIDER_DEPTH": 0, "PROGRESS_DEPTH": 0}
sg.theme_add_new("BMSBlueGray", BMSBlueGray)
sg.theme("BMSBlueGray")

Settings_file = sg.user_settings_filename(os.path.join(os.path.dirname(__file__), "settings.cfg"))
#Settings_file = sg.user_settings_filename("settings.cfg")
print("==> MAIN Config file location : ", Settings_file)

#program entry point
def main():
    window = MyWindows.open_window()
    
if __name__ == "__main__":    
    main()        
