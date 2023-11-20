from os import path


import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

from shutil import move, copytree
import time

from helper_func import create_new_folder, create_new_folder_with_data_sorting, list_of_folder, grab_time, \
    folder_guard, folder_layout_check


class MyEventHandler(FileSystemEventHandler):
    def __str__(self):
        """This is a standard class for watchdog.
        This is the class that is listening for files being created, moved or deleted.
        ATM the system only react to newly created files"""

    def __init__(self, window):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.source_folder = self.config["Folder"]["in"]
        self.top_destination_folder = self.config["Folder"]["out"]
        self.window = window

    def on_created(self, event):
        """
        This event is triggered when a new file or folder appears in the target folder or sub folders
        :param event: The full event, including the path to the file that have been created
        """

        # checks if path is a directory
        if path.isdir(event.src_path):
            temp_dir = event.src_path

            # This make sure that the event is only trigger on new folders being created in the main input folder,
            # and avoids triggers on sub folders being created
            if len(temp_dir.split("\\")) == 2:

                last_folder = self.window["-LAST_FOLDER-"].get()
                file_amount = int(self.window["-FILE_COUNTER-"].get())
                copy = self.window["-RADIO_COPY-"].get()
                date_sorting = self.window["-DATE_SORTING-"].get()
                time_for_folder = self.window["-TIME_TEXT-"].get()

                # Check if the program have been running. If it has just started this should be empty
                if last_folder:

                    # gives time for the computer to generate the PDF file of the data.
                    time.sleep(10)

                    if copy:
                        if date_sorting:
                            destination_folder = create_new_folder_with_data_sorting(self.top_destination_folder,
                                                                                     last_folder)
                        else:
                            destination_folder = create_new_folder(self.top_destination_folder, last_folder)

                        copytree(last_folder, destination_folder)
                    else:
                        if date_sorting:
                            destination_folder = create_new_folder_with_data_sorting(self.top_destination_folder,
                                                                                     last_folder)
                        else:
                            destination_folder = self.top_destination_folder

                        move(last_folder, destination_folder)
                file_amount += 1
                self.window["-FILE_COUNTER-"].update(value=file_amount)
                self.window["-FILE_COUNTER_INFO-"].update(value=(f"File moved this session: {file_amount}"))
                self.window["-LAST_FOLDER-"].update(value=temp_dir)
                # Gets time-code for when file was created.
                self.window["-TIME_TEXT-"].update(value=datetime.now())

        else:
            print(event.src_path)
            print(f"{datetime.now()} - A File have been created... this should not have happend")

    # def on_deleted(self, event):
    #     """
    #     This event is triggered when a file is removed from the folder, either by deletion or moved.
    #     :param event:
    #     :return:
    #     """
    #     print("delet")
    #     print(event)

    # def on_modified(self, event):
    #     """
    #     This event is triggered when a file is modified.
    #     :param event:
    #     :return:
    #     """
    #     print("mod")
    #     print(event)


def listening_controller(config, run, window):
    """
    main controller for listening for files.
    :param config: The config handler, with all the default information in the config file.
    :type config: configparser.ConfigParser
    :param run: A state to tell if the listening is active or not
    :type run: bool
    :param window: The window where the activation of the listening is.
    :type window: PySimpleGUI.PySimpleGUI.Window
    :return:
    """

    path = config["Folder"]["in"]

    event_handler = MyEventHandler(window)

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while run:
            time.sleep(1)
            if window["-KILL-"].get():
                run = False

    finally:
        observer.stop()
        observer.join()
        print(f"{datetime.now()} - done")


def sorting_folder(source_folder, top_destination_folder):
    """
    Moving files from one folder to another, while sorting based on dates
    If source and destination folder is the same folder, it will sort out that folder
    :param source_folder: The source folder
    :type source_folder: str
    :param top_destination_folder: The destination folder for the files, can be the same as the source folder
    :type top_destination_folder: str
    :return: Amount of folders moved
    :rtype: int
    """

    all_folders = list_of_folder(source_folder)
    amount_of_folders = len(all_folders)
    for folder in all_folders:

        if folder_guard(folder):
            year, month, _ = grab_time(folder)
            destination_folder = folder_layout_check(top_destination_folder, year, month)

            move(folder, destination_folder)

    return amount_of_folders

if __name__ == "__main__":
    top_destination_folder = r"V:\OrganiskKEMI\01 - Dataopsamling\SQD2_122a\raw_backup"
    sorting_folder(top_destination_folder)
