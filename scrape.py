"""
Scrapes houseplant care information from multiple pages from
https://www.tropicopia.com/ and
https://www.houseplant411.com/houseplant
and stores it in a file called "plant_data.csv"

This module is made for project.py, but can be run seperately to
generate "plant_data.csv"

Notes:
    -scraping from houseplant411 takes especially long

    -some redunant code when trying to clean data
    (raw data scraped from houseplant411 is particularly messy)

    -these websites were chosen specifically to practice scraping from messy
    sources and combining the information from the two different sources

    -for data cleaning the pandas library was not used in order to practice
    using different data structures in base python
"""
import requests # to get html from webpages
from bs4 import BeautifulSoup as bs # extract data from html
import re # to clean data
import csv # to save data into a separate file


def main():
    get_data()

def get_data():
    """ Creates plant_data.csv from web scraped data """
    save_file(combine(scrape_trop(), scrape_411()))
    print("Data is saved in plant_data.csv")

def save_file(data_dict):
    """
    Saves formatted and cleaned data to a csv file

    Parameters:
        data_dict : list
            data in the form of a list of dictionaries
    """
    print("Saving data to file...")
    with open('plant_data.csv', 'w', encoding='utf8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data_dict[0].keys())
        writer.writeheader()
        writer.writerows(data_dict)


def combine(big_list, small_list):
    """
    Combines data from big_list and small_list

    Parameters:
        big_list : list
            tropicopia's list of dictionaries representing plants
            and all but soil data
        small_list: list
            houseplant411's list of dictionaries representing plants
            with data on name and soil

    Returns:
        list : list of dictionaries containing all scraped data
        about houseplants from tropicopia and houseplant411
    """
    print("Combining data from both websites...")
    combined = [find_soil(d, small_list) for d in big_list]
    return remove_repeats(combined)

def find_soil(plant_dict, small_list):
    """
    Adds small_list's soil data and any additional alternative
    names for a plant to the dictionary plant_dict

    Parameters:
        plant_dict : dictionary
            A dictionary that represents a plant without soil data
        small_list : list
            list of dictionaries,
            each represent a plant with only name and soil data

    Returns:
        dict : plant dictionary that has soil data
    """
    for plants in small_list:
        for name in plants['name']:
            if (name in plant_dict['name'] or
                plant_dict['categories'].lower().find(name) != -1):
                alt_names = [alt_name for alt_name in plants['name'] if alt_name not in plant_dict['name']]
                plant_dict['name'].extend(alt_names)
                soil_info = next(d['soil'] for d in small_list if d["name"] == plants['name'])
                plant_dict['soil'] = soil_info
                return plant_dict

    plant_dict['soil'] = "No information available"
    return plant_dict


def scrape_411():
    """
    Scrapes data from houseplant411 and stores each plant in a
    dictionary where all the keys are name and soil

    There are 141 houseplant webpages on houseplant411

    Note: it takes a few minutes to process all the data

    Returns:
        list : list of dicts with each dict being a single plant
    """
    # URL has list of all the urls for each plant care page
    URL = "https://www.houseplant411.com/houseplant?popup=2"
    soup411 = scrape_html(URL)

    plant411_urls = []
    for link in soup411.find_all('a'):
        plant411_urls.append(link.get('href'))

    print("Reading houseplant411 pages...")
    plant_list = []
    for link in plant411_urls:
        plant_list.append(read_411_page(link))

    return remove_repeats(plant_list)


def read_411_page(url):
    """
    Stores information from a houseplant411 webpage into a dictionary
    Only names and soil information are stored

    Parameters:
        url : str
            webpage url as a string

    ReturnsL
        dict : contains name and soil information on the plant
    """
    data = []
    var_name = ["name","soil"]
    soup = scrape_html(url)

    # some names contain “ double quotations that aren't the normal kind
    # anything after a en or em hyphen can be discarded
    names = [re.sub(r"–(.+)|-(.+)|“(.+)”", "", soup.find("h1").text.lower())]
    sci_name = soup.find("div", {"class": "clear resultSpecies"})
    other_names = soup.find("div", {"class": "clear resultAltName"})

    if sci_name:
        names.append(re.sub(r"(c|d|r)\.(.+)|-(.+)","",sci_name.text.lower()))
    if other_names:
        if sci_name is None or other_names not in sci_name:
            # bars, new lines and commas are supposed to be seperate names
            names.extend(re.split(r" \| |\r\n|, ",
                            re.sub(r" -|^\'|\'$","",other_names.text.lower())))

    # removing double spaces to any of the names and empty names
    names = [" ".join(name.split()) for name in names if name]
    # remove duplicate names and add to data list
    data.append(names)

    # find where the soil information is
    info_keys = soup.find_all(class_="post-meta-key")
    for i, keys in enumerate(info_keys):
        soil = None
        if keys.text == "Soil":
            soil_info = soup.find_all(class_="post-meta-value")[i]
            # remove any popup text within the soil information
            pop_text = soil_info.find("a", {"class": "popUpMain"})
            if pop_text:
                keep = pop_text.next_element
                pop_text.decompose()
                text = soil_info.text.replace("  ", " " + keep)
            else:
                text = soil_info.text
            # gets rid of "best soil for a __:"
            soil = re.sub(r"(.+): ","",text)
            break

    data.append(soil)

    return {var_name[i]: data[i] for i in range(len(var_name))}


def scrape_trop():
    """
    Scrapes all houseplant data from tropicopia and stores each plant in a
    dictionary where all the keys are plant variables and the values are the
    information

    There are 355 houseplant webpages on tropicopia

    Note: it takes a few minutes to process all the data

    Returns:
        list : list of dicts with each dict being a single plant
    """
    # tropicopia's urls for each plant are in the form
    # "http://www.tropicopia.com/house-plant/detail.np/detail-##.html"
    # numbers < 10 have a zero in front and it goes all the way to 355
    print("Reading tropicopia pages...")
    plant_list = []
    for i in range(355):
        plant_list.append(clean_trop(read_trop_page(
            "http://www.tropicopia.com/house-plant/detail.np/detail-"+
            f"{i+1:02}" + ".html")))

    return remove_repeats(plant_list)


def clean_trop(plant_dict):
    """
    Merges all name type variables into one key "name" for a
    dictionary that contains a plant's data from one tropicopia webpage

    Parameters:
        plant_dict : dict
            a dictionary containing all the information in original form of a
            single plant from trop

    Returns:
        plant_dict : dict
            a dictionary with all the name type keys combined into one key
    """

    name_vars = ['latin name', 'other names','common name']
    raw_names = []
    names = []
    for name in name_vars:
        if plant_dict[name] is not None:
            # split names if there is more than one name
            if plant_dict[name].find(',') != -1:
                raw_names.extend(plant_dict[name].split(","))
            else:
                raw_names.append(plant_dict[name])

    # get rid of name variants that are in quotation marks
    # ex: "Aglaonema 'Amelia'", get rid of 'Amelia'
    # also " var."/" var$" or " x "  or "a."/"c."/"x." in other names
    for name in raw_names:
        temp = re.sub(
            r"(\'|\"|\()(.+)(\'|\"|\))| (x) (.+)?| x$|^(a|c|x). (.+)| var.(.+)?| var$",
            "", name.lower()).strip()
        if temp:
            names.append(temp)

    plant_dict['name'] = names
    for keys in name_vars:
        del plant_dict[keys]

    return plant_dict


def read_trop_page(url):
    """
    Stores information from a tropicopia webpage into a dictionary
    Each key is a variable for the plant

    Parameters:
        url : str
            webpage url as a string

    ReturnsL
        dict : contains information on the plant
    """
    plant_page = scrape_html(url)
    # <p class="ar12D"> contains all the relevant information
    page = plant_page.find_all("p",class_="ar12D")
    raw_data = []

    for info in page:
        # variable names like "Latin Name: " are bolded
        if info.find('b') is not None:
            raw_data.append(info.find('b').text.strip())
        else:
            # data for a variable is not bolded
            raw_data.append(info.text.strip())

    # organizing into variable names and their values
    var_names = []
    values = []

    for index, data in enumerate(raw_data):
        if data.find(":") != -1:
            var_names.append(re.sub(r" :$","",data).lower())
            # seperate if statements to avoid IndexError for the last variable
            # if plant variable has a value, the next entry will not have a ":"
            if raw_data[index+1].find(":") == -1:
                values.append(raw_data[index+1])
            else:
                values.append(None)

    # make var_name into keys and data in values
    return {var : values[i] for i, var in enumerate(var_names)}


def remove_repeats(data_dict):
    """
    Combines plants that have the same name into one entry

    Parameters:
        data_dict : list
            list of plant dictionaries

    Returns:
        data_dict : list
            shorter list of plant dictionaries with name repeats
            combined into one dictionary
    """
    name_list = [d['name'] for d in data_dict]
    # index of repeated plants
    repeats = []

    for i, plant in enumerate(data_dict):
        names = plant['name']
        other_plants = name_list[i+1:]

        for j, other_names in enumerate(other_plants):
            for name in names:
                if name in other_names:
                    data_dict[i]['name'].extend(other_names)
                    # index of repeated plant, add 1 because index starts at 0
                    repeats.extend([i+j+1])
                    break

    indices = sorted(list(set(repeats)), reverse=True)
    # removes duplicate plant using index
    for i in indices:
        if i < len(data_dict):
            data_dict.pop(i)

    # removing any repeated names in individual plants that slipped through
    for d in data_dict:
        d['name'] = list(set(d['name']))

    return data_dict


def scrape_html(url):
    """
    Returns the html content for a webpage

    Parameters:
        url : str
            webpage url as a string

    Returns:
        BeautifulSoup object : representation of the parsed html
    """
    page = requests.get(url)
    return bs(page.content, "html.parser")


if __name__ == "__main__":
    main()