"""
==============================
Houseplant care information project
==============================

Project submission for Harvard's CS50P independent Final Project

This program outputs houseplant care information for a user requested plant,
the information is from web scraped data.


Data sources:
    https://www.tropicopia.com/
    https://www.houseplant411.com/houseplant


Notes:
    -Web scraping data takes a few minutes
    (could be refactored to save space and time)
    (purposely limited use of pandas library to practice using different data
     structures in base python)

    -Final data is not completely clean
    (some duplicate name entries in different Plant objects and other anamolies)

    -Final data is based on all the plants listed in tropicopia
    (houseplant411 could be re-scraped to add even more plants)
"""

import sys # to exit program
import re # cleaning up data
import pandas as pd # translating csv to dataframe
import string # to format plant care info
from scrape import get_data # web scrapes tropicopia and houseplant411


class Plant:
    """
    Class to store care info of a plant

    Attributes
    ----------
        name : list of str
            all the different names of the plant
        soil : str
            soil type for the plant
        temp : tuple(int/float, int/float)
            ideal temperature (°C) for the plant
        light : tuple(str, str)
            light requirements for the plant
        water : str
            water frequency for the plant
    """

    def __init__(self, name, soil=None, temp=None, light=None, water=None):
        """ Constructor for Plant class """
        self.name = name
        self.soil = soil
        self.temp = temp
        self.light = light
        self.water = water


    @property
    def name(self):
        """ Gets name property """
        return self._name

    @name.setter
    def name(self, val):
        if type(val) is list:
            self._name = [x.lower() for x in val]
        elif type(val) is str:
            self._name = val.lower().split(",")
        else:
            raise ValueError("Invalid name type")

    @property
    def soil(self):
        """ Gets soil property """
        return self._soil

    @soil.setter
    def soil(self, val):
        if type(val) is str:
            self._soil = val
        else:
            self._soil = None

    @property
    def temp(self):
        """ Gets temp property """
        return self._temp

    @temp.setter
    def temp(self, val):
        # plant has both a ideal temp and min temp
        if type(val) is tuple:
            if (isinstance(val[0], (int,float)) and
                isinstance(val[1], (int,float))):
                self._temp = (val[0], val[1])
        # plant only has an ideal temp
        elif isinstance(val, (int,float,str)):
            self._temp = (int(val), None)
        else:
            self._temp = None


    @property
    def light(self):
        """ Gets light property """
        return self._light
    @light.setter
    def light(self, val):
        # plant has both a ideal light and min light
        if type(val) is tuple:
            self._light = (val[0], val[1])
        # plant only has an ideal light
        elif type(val) is str:
            self._light = (val, None)
        else:
            self._light = None

    @property
    def water(self):
        """ Gets water property """
        return self._water
    @water.setter
    def water(self, val):
        if type(val) is str:
            self._water = val
        else:
            self._water = None


    def add_names(self, val):
        """
        Adds a name(s) to the name property

        Parameters:
            val : list or str
                if its a list, each list item is a name to be added
                if its a str value, the names are seperated by ","

        Returns:
            list : list of names with added names

        Raises:
            ValueError: Invalid name type
        """
        if type(val) is list:
            return self.name.extend([x.lower() for x in val])
        elif type(val) is str:
            return self.name.extend(val.lower().split(","))
        else:
            raise ValueError("Invalid name type")


    def format(self, prop, string, val):
        """
        Helper to format the text for the __str__ method

        Parameters:
            prop : Plant object property
            string : str
                text that comes before property value
            val : str or tuple(str, str)
                property value

        Returns:
            str : formatted property value string

        Raises:
            ValueError: Invalid property
        """
        na = "No information available"

        if prop in ["temp","light"]:
            if val is None:
                return string + na
            elif pd.isna(val[1]):
                return string + str(val[0])
            elif prop == "temp":
                return string + str(val[1]) + " to " + str(val[0])
            else:
                return string + val[1] + "\n" + "-Light Ideal: " + val[0]
        elif prop in ["water","soil"]:
            if val is None:
                return string + na
            else:
                return string + val
        else:
            raise ValueError("Invalid property")



    def __str__(self):
        """ Represents class properties as a formatted string """
        # title() capitalizes wrong sometimes (ex: thing's -> Thing'S)
        names = string.capwords(" / ".join(self.name))
        temp_string = self.format("temp","-Ideal Temperature (°C): ",self.temp)
        light_string = self.format("light","-Light Requirements: ",self.light)
        soil_string = self.format("soil","-Soil: ",self.soil)
        water_string = self.format("water","-Water Frequency: ",self.water)

        return (names + "\n"
                f"---------------\n" +
                soil_string + "\n" +
                temp_string + "\n" +
                light_string + "\n" +
                water_string + "\n")


def main():
    # read and store data from plant_data.csv
    data = gather_info()

    while True:
        action = ask_action()
        # structural pattern matching is only for Python 3.10+
        match action:
            # prints complete list of plant names
            case 1:
                # the * unpacks the list
                print(*all_plants(data), sep="\n")
            # prints care info for the requested plant
            case 2:
                print(find_info(data))
            # scrapes data and saves it into a csv file
            case 3:
                get_data()
            case 4:
                sys.exit()


def gather_info():
    """
    Reads and stores plant information
    (names, temp max/min, light ideal/min and soil)
    from plant_data.csv in a list of Plant objects

    Returns:
        (list) : list of Plant objects created using plant_data.csv
    """
    # only relevant information from the csv file
    csv_col_names = ['temperature max. (c°)',
                    'temperature min. (c°)',
                    'light ideal',
                    'light tolered',
                    'watering',
                    'name',
                    'soil']
    try:
        data = pd.read_csv("plant_data.csv",
                       usecols=csv_col_names)
    except FileNotFoundError:
        print("plant_data.csv not found, data will be scraped...")
        # from scrape.py
        get_data()
        data = pd.read_csv("plant_data.csv",
                       usecols=csv_col_names)

    # change variable names for accessibility
    new_col_names = ['temp max',
                    'temp min',
                    'light ideal',
                    'light tolerated',
                    'water',
                    'name',
                    'soil']
    data.columns = new_col_names

    return format_data(data)


def format_data(data):
    """
    Stores data from a DataFrame into Plant objects

    Parameters:
        data : pandas DataFrame object

    Returns:
        plant list : list
            list of Plant objects
    """
    plant_list = []
    for index, row in data.iterrows():
        # read_csv returns name as str instead of list of str, remove "[,],',"
        # Plant object needs names to be in a list
        # also fitting in edge cases where names like
        # "devil's Ivy" was not getting rid of the quotation marks
        list_names = re.sub(r"\'," ,",",
                        re.sub(r"\[\'| \'|(\')?\]|\"", "", row['name']))
        plant = Plant(name = list_names,
                     soil = row['soil'],
                     temp = (row['temp max'],row['temp min']),
                     light = (row['light ideal'],row['light tolerated']),
                     water = row['water'])

        plant_list.append(plant)

    # temp min, light tolerated have None/NaN values
    # print(data.isna().any())

    return plant_list


def ask_action():
    """
    If user enters invalid action (not 1-4) it prompts user to
    enter a valid action

    Returns:
        (int): action the user wishes to take
    """
    while True:
        action = user_input()
        # try catches if input is anything that isn't an int
        try:
            if int(action) not in [1,2,3,4]:
                print("\n*** Enter a number from 1-4 ***")
            else:
                break
        except ValueError:
            print("\n*** Use numerical values only ***")

    return int(action)

def user_input():
    """
    Prompts user with 4 actions and returns user's answer

    Returns:
        (str) : user's input
    """
    user_input = input("---------------------------------------------- \n" +
                    "1: View the names of all the plants available \n" +
                    "2: Find plant care information for a specific plant \n" +
                    "3: Scrape plant data and save as a file \n" +
                    "4: Exit application \n" +
                    "\n What would you like to do?: "
                    )
    return user_input



def all_plants(data):
    """
    Creates list of the names of all the plants in data,
    plants with more than one name are combined into one string

    Parameters:
        data : list
            list of Plants

    Returns:
        (list) : list of strings for all the Plant names
    """
    name_list = []
    for Plant in data:
        # title() capitalizes wrong sometimes (ex: thing's -> Thing'S)
        name_list.append(string.capwords("+ " + " / ".join(Plant.name)))

    return name_list


def find_info(data):
    """
    Asks user for the name of the plant and prints the care information.
    If the plant is not in the data, prints sorry message

    Parameters:
        data : list
            list of Plants
    """
    chosen = plant_info(data, input("Plant name: ").lower().strip())
    if chosen is not None:
        return chosen
    else:
        return "Sorry, we don't have information for this plant"


def plant_info(data, plant_name):
    """
    Searches through data for Plant object that has
    soil, temp, light and water info for the specified plant

    Parameters:
        plant_name (str): alphabetical string
            user inputted name to check for

    Returns:
        (Plant) or None
    """
    for Plant in data:
        if plant_name in Plant.name:
            return Plant

    # if plant is not found, return None
    return None


if __name__ == "__main__":
    main()
