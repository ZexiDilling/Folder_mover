from os import path

import PySimpleGUI as sg
import threading
import time


from gui import main_layout
from helper_func import config_writer, config_handler
from main_func import listening_controller, sorting_folder


def main():
    """
    The main GUI setup and control for the whole program
    The while loop, is listening for button presses (Events) and will call different functions depending on
    what have been pushed.
    :return:
    """

    theme = None
    all_themes = sg.theme_list()
    window = main_layout(theme, all_themes)

    config = config_handler()

    while True:

        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "-CLOSE-":
            break

        if event == "-LISTEN-":
            window["-KILL-"].update(value=False)

            window["-FILE_COUNTER_INFO-"].update(value="File moved this session: 0")
            window["-FILE_COUNTER-"].update(value="0")

            if not path.exists(config["Folder"]["in"]):
                folder_in = sg.PopupGetFolder("Please select the folder you would like to listen to")
                config_heading = "Folder"
                sub_heading = "in"
                data_dict = {sub_heading: folder_in}
                config_writer(config, config_heading, data_dict)

            if not path.exists(config["Folder"]["out"]):
                folder_out = sg.PopupGetFolder("Please select the folder where your reports ends up")
                config_heading = "Folder"
                sub_heading = "out"
                data_dict = {sub_heading: folder_out}
                config_writer(config, config_heading, data_dict)

            threading.Thread(target=listening_controller, args=(config, True, window,), daemon=True).start()
            threading.Thread(target=progressbar, args=(True, window,), daemon=True).start()

        if event == "-KILL_BUTTON-":
            window["-KILL-"].update(value=True)

        if event == "-SHOW_PLATE_LIST-":
            window["-TEXT_FIELD-"].update(visible=values["-SHOW_PLATE_LIST-"])

        if event == "reset":
            window["-TIME_TEXT-"].update(value="")
            window["-INIT_TIME_TEXT-"].update(value="")
            window["-FILE_COUNTER_INFO-"].update(value="File moved this session: 0")
            window["-FILE_COUNTER-"].update(value="0")

        if event == "In":
            config_heading = "Folder"
            sub_heading = "in"
            new_folder = sg.PopupGetFolder(f"Current folder: {config[config_heading][sub_heading]}", "Data Folder")
            if new_folder:
                data_dict = {sub_heading: new_folder}
                config_writer(config, config_heading, data_dict)

        if event == "Out":
            config_heading = "Folder"
            sub_heading = "out"
            new_folder = sg.PopupGetFolder(f"Current folder: {config[config_heading][sub_heading]}", "Data Folder")
            if new_folder:
                data_dict = {sub_heading: new_folder}
                config_writer(config, config_heading, data_dict)

        if event == "Sorting":
            source_folder = sg.PopupGetFolder("Please select Source folder")
            destination_folder = sg.PopupGetFolder("Please select Destination folder\n"
                                                   "It can be the same as the source folder")

            amount_of_files = sorting_folder(source_folder, destination_folder)

            sg.Popup(f"Done - {amount_of_files} have been moved")

        if event == "Sorting Info":
            sg.Popup("The sorting function will move folders, from a folder to a new folder, "
                     "or the same folder if chosen.\n"
                     "It will sort the files  based on year and months\n"
                     "-Files will not be touched-")

        if event == "Info":
            with open("README.txt") as file:
                info = file.read()

            sg.Popup(info)

        if event == "About":
            sg.Popup("File Mover and sorter. Programmed By Charlie")

        if event in all_themes:
            selected_theme = event
            window.close()
            window = main_layout(selected_theme, all_themes)
            window.read()


def progressbar(run, window):
    """
    The progress bar, that shows the program working
    :param run: If the bar needs to be running or not
    :type run: bool
    :param window: Where the bar is displayed
    :type window: PySimpleGUI.PySimpleGUI.Window
    :return:
    """
    min_timer = 0
    max_timer = 100
    counter = 0
    runner = "pos"

    while run:
        if counter == min_timer:
            runner = "pos"
        elif counter == max_timer:
            runner = "neg"
        else:
            pass

        if runner == "pos":
            counter += 10
        elif runner == "neg":
            counter -= 10
        else:
            pass

        window["-BAR-"].update(counter)

        time.sleep(0.1)
        if window["-KILL-"].get():
            run = False