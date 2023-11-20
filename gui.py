import PySimpleGUI as sg
import configparser
from threading import Thread
import time


def _menu():
    """
    Top menu of the gui
    :return: The top menu
    :rtype: list
    """

    theme_1 = ["Black", "BlueMono", "BluePurple", "BrightColors", "BrownBlue", "Dark", "Dark2", "DarkAmber",
               "DarkBlack", "DarkBlack1", "DarkBlue", "DarkBlue1", "DarkBlue10", "DarkBlue11", "DarkBlue12",
               "DarkBlue13", "DarkBlue14", "DarkBlue15", "DarkBlue16", "DarkBlue17", "DarkBlue2", "DarkBlue3",
               "DarkBlue4", "DarkBlue5", "DarkBlue6", "DarkBlue7", "DarkBlue8", "DarkBlue9", "DarkBrown", "DarkBrown1",
               "DarkBrown2", "DarkBrown3", "DarkBrown4", "DarkBrown5", "DarkBrown6", "DarkGreen", "DarkGreen1",
               "DarkGreen2", "DarkGreen3", "DarkGreen4", "DarkGreen5", "DarkGreen6", "DarkGrey", "DarkGrey1",
               "DarkGrey2", "DarkGrey3", "DarkGrey4", "DarkGrey5", "DarkGrey6", "DarkGrey7"]
    theme_2 = ["DarkPurple", "DarkPurple1", "DarkPurple2", "DarkPurple3", "DarkPurple4", "DarkPurple5", "DarkPurple6",
               "DarkRed", "DarkRed1", "DarkRed2", "DarkTanBlue", "DarkTeal", "DarkTeal1", "DarkTeal10", "DarkTeal11",
               "DarkTeal12", "DarkTeal2", "DarkTeal3", "DarkTeal4", "DarkTeal5", "DarkTeal6", "DarkTeal7", "DarkTeal8",
               "DarkTeal9", "Default", "Default1", "DefaultNoMoreNagging", "Green", "GreenMono", "GreenTan",
               "HotDogStand", "Kayak", "LightBlue", "LightBlue1", "LightBlue2", "LightBlue3", "LightBlue4",
               "LightBlue5", "LightBlue6", "LightBlue7"]
    theme_3 = ["LightBrown", "LightBrown1", "LightBrown10", "LightBrown11", "LightBrown12", "LightBrown13",
               "LightBrown2", "LightBrown3", "LightBrown4", "LightBrown5", "LightBrown6", "LightBrown7", "LightBrown8",
               "LightBrown9", "LightGray1", "LightGreen", "LightGreen1", "LightGreen10", "LightGreen2", "LightGreen3",
               "LightGreen4", "LightGreen5", "LightGreen6", "LightGreen7", "LightGreen8", "LightGreen9", "LightGrey",
               "LightGrey1", "LightGrey2", "LightGrey3", "LightGrey4", "LightGrey5", "LightGrey6", "LightPurple",
               "LightTeal", "LightYellow", "Material1", "Material2", "NeutralBlue", "Purple", "Reddit", "Reds",
               "SandyBeach", "SystemDefault", "SystemDefault1", "SystemDefaultForReal", "Tan", "TanBlue", "TealMono",
               "Topanga"]


    menu_top_def = [
        # ["&File", ["&Open    Ctrl-O", "&Save    Ctrl-S", "---", '&Properties', "&Exit", ]],
        ["&Settings", ["Folder", ["In", "Out", ], "reset"], ],
        ["&Bonus", ["Sorting", "Sorting Info"]],
        ["&Help", ["Info", "About", "Theme 1", [theme_1], "Theme 2", [theme_2], "Theme 3", [theme_3]]],
    ]
    layout = [[sg.Menu(menu_top_def)]]
    return layout


def _gui_main_layout():
    """
    The main layout for the gui
    :return: The main layout for the gui
    :rtype: list
    """

    main = sg.Frame("Listening", [[
        sg.Column([
            [sg.T("File moved this session: 0", key="-FILE_COUNTER_INFO-"), sg.T(key="-FILE_COUNTER-", visible=False)],
            [sg.Radio("Copy", group_id=1, key="-RADIO_COPY-",
                      tooltip="Will copy the files to the destination folder"),
             sg.Radio("Move", group_id=1, key="-RADIO_MOVE-",
                      tooltip="Will Move the file to the destination folder"),
             sg.Checkbox("Date sorting", key="-DATE_SORTING-",
                         tooltip="If true, Will create folders based on year and month in destination folder")],
            [sg.ProgressBar(100, key="-BAR-", size=(25, 5), expand_x=True),
             sg.Checkbox("KILL", visible=False, key="-KILL-")],
            [sg.Button("Listen", key="-LISTEN-", expand_x=True,
                       tooltip="starts the program that listen to the folder for files"),
             sg.Button("Kill", key="-KILL_BUTTON-", expand_x=True,
                       tooltip="stops the program that listen to the folder for files"),
             sg.Button("Close", key="-CLOSE-", expand_x=True,
                       tooltip="Closes the whole program")],
            [sg.Text(key="-TIME_TEXT-", visible=False),
             sg.Text(key="-INIT_TIME_TEXT-", visible=False),
             sg.T(key="-LAST_FOLDER-", visible=False)],

        ]),
    ]])

    layout = [[main]]

    return layout


def main_layout(theme):
    """
    The main setup for the layout for the gui
    :return: The setup and layout for the gui
    :rtype: sg.Window
    """

    sg.theme(theme)
    top_menu = _menu()

    layout = [[
        top_menu,
        _gui_main_layout()
    ]]

    return sg.Window("Folder Mover", layout, finalize=True, resizable=True)

