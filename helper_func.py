import os
import sys
from pathlib import Path
from os.path import getctime
from datetime import datetime

import configparser


def config_writer(config, heading, data_dict):
    """
    The code is a function for writing data to a configuration file using the configparser library.
    The function takes in a config object (the handler for the configuration file), a heading string
    (the section heading in the configuration file), and a data_dict dictionary (the key-value pairs to be written to
    the configuration file). The function iterates through the key-value pairs in the data_dict and sets the values in
    the config object using the config.set method. Finally, the function opens the configuration file for writing,
    writes the config object to the file, and closes the file.
    :param config: The config handler, with all the default information in the config file.
    :type config: configparser.ConfigParser
    :param heading: The heading of the specific configuration
    :type heading: str
    :param data_dict: The data that needs to be added to the dict
    :type data_dict: dict
    :return:
    """

    # Iterate through each key-value pair in the data dictionary
    for data in data_dict:
        # Set the value in the config file for the given heading and data
        config.set(heading, data, data_dict[data])
    # Open the config file for writing
    with open("./stuff/config.ini", "w") as config_file:
        # Write the config data to the file
        config.write(config_file)


def list_of_folder(folder):
    """
    Generates a list of folders inside a folder
    :param folder: The path of folder where the folders are
    :type folder: str
    :return: A list of folders
    :rtype: list
    """
    try:
        temp_folder = Path(folder)
    except TypeError as e:
        print("-------------")
        print(folder)
        print(e)
        return

    return [f for f in temp_folder.iterdir() if f.is_dir()]


def c_to_m(month_in_number):
    """
    Translate base numbers into months
    :param month_in_number: The month in number formate
    :type month_in_number: int
    :return: The name of the month with a leading number for sorting
    :rtype: str
    """
    number_to_name = {1: "01-January", 2: "02-February", 3: "03-Marts", 4: "04-April", 5: "05-May", 6: "06-June",
                      7: "07-July", 8: "08-August", 9: "09-September", 10: "10-October", 11: "11-November",
                      12: "12-December"}
    return number_to_name[month_in_number]


def folder_guard(folder):
    """
    This is a really basic guard. It is looking at a folder, of the name is numbers is will check the length,
    if the length is 4, it assumes that the folder is a year and skips the folder
    :param folder: the name of the folder that needs to be checked
    :type folder: str
    :return: False of True depending on the guard status
    :rtype: bool
    """
    folder_name = folder.name

    # Check if the folder name is a year.
    # Should do a check for sub folder to see if it contains months to avoid skipping folders
    try:
        int(folder_name)
    except ValueError as e:
        pass
    else:
        if len(folder_name) == 4:
            return False
        else:
            pass
    return True


def grab_time(folder):
    """
    This grabs the creation date of the folder and returns the year month and day
    :param folder: The path to the folder
    :type folder: str
    :return: The year, month and day of the folder being created
    :rtype: str, str, str
    """

    temp_time = getctime(folder)
    temp_date = datetime.fromtimestamp(temp_time)
    date = str(temp_date).split(" ")[0]
    year, month, day = date.split("-")
    name_month = c_to_m(int(month))

    return year, name_month, day


def folder_layout_check(top_destination_folder, year, month):
    """
    Check if the layout is in place for sorting, if not it will create the missing folders
    :param top_destination_folder: The path to the main destination folder
    :type top_destination_folder: str
    :param year: The year that needs to be checked if a folder exist with that name
    :type year: str
    :param month: The month that needs to be checked if a folder exist with that name
    :type month: str
    :return: The new path to the folder
    :rtype: str
    """
    top_destination_folder = Path(top_destination_folder)
    temp_folder = top_destination_folder / year
    try:
        temp_folder.mkdir()
    except FileExistsError:
        pass
    temp_folder = top_destination_folder / year / month
    try:
        temp_folder.mkdir()
    except FileExistsError:
        pass

    return temp_folder


def create_new_folder_with_data_sorting(top_destination_folder, source_folder):
    """
    Create the destination folder, based on the name of the source folder and based on the current_date
    :param top_destination_folder: The path to the top folder
    :type top_destination_folder: str
    :param source_folder: the path to where the content is coming from
    :type source_folder: str
    :param current_date: The current date for when the last folder was created
    :type current_date: str
    :return: destination_folder
    :rtype: str or <class 'pathlib.WindowsPath'>
    """

    year, month, _ = grab_time(source_folder)

    top_destination_folder = Path(top_destination_folder)

    source_folder = Path(source_folder)

    folder_name = source_folder.name
    temp_folder = folder_layout_check(top_destination_folder, year, month)

    destination_folder = temp_folder / folder_name
    try:
        destination_folder.mkdir()
    except FileExistsError:
        pass

    return str(destination_folder)


def create_new_folder(top_destination_folder, source_folder):
    """
    Create the destination folder, based on the name of the source folder
    :param top_destination_folder: The path to the top folder
    :type top_destination_folder: str
    :param source_folder: the path to where the content is coming from
    :type source_folder: str
    :return: destination_folder
    :rtype: str
    """
    source_folder = Path(source_folder)
    top_destination_folder = Path(top_destination_folder)
    folder_name = source_folder.name

    destination_folder = top_destination_folder / folder_name

    return str(destination_folder)


def config_handler():
    config = configparser.ConfigParser()
    config_file = "config.ini"
    config_file = resource_path(config_file)
    config.read(config_file)
    return config

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    top_destination_folder = r"C:/Users/phch/Desktop/testing/output"
    folder = Path(top_destination_folder)
    temp = folder.glob("\\")
    bah = ([f for f in folder.iterdir() if f.is_dir()])
    for folders in bah:
        print(folders)