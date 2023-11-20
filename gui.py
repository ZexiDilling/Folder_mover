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
    menu_top_def = [
        # ["&File", ["&Open    Ctrl-O", "&Save    Ctrl-S", "---", '&Properties', "&Exit", ]],
        ["&Settings", ["Folder", ["In", "Out", ], "reset"], ],
        ["&Bonus", ["Sorting", "Sorting Info"]],
        ["&Help", ["Info", "About"]],
    ]
    layout = [[sg.Menu(menu_top_def)]]
    return layout


def _gui_main_layout():
    """
    The main layout for the gui
    :return: The main layout for the gui
    :rtype: list
    """
    tool_tip_plate_number = "This is the amount of Destination plates for the transfer"

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


def main_layout():
    """
    The main setup for the layout for the gui
    :return: The setup and layout for the gui
    :rtype: sg.Window
    """

    # sg.theme()
    top_menu = _menu()

    layout = [[
        top_menu,
        _gui_main_layout()
    ]]

    return sg.Window("Echo Data", layout, finalize=True, resizable=True)

