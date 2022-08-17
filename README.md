# Houseplant Care Info
## **Video Demo:** https://www.youtube.com/watch?v=8qMc7DV8hhY
&nbsp;
## **Description:**
This code outputs houseplant care information using houseplant data web scraped from http://www.tropicopia.com/house-plant/index.html and https://www.houseplant411.com/houseplant

&nbsp;
&nbsp;
## **Execution example:**
1. Run in the command line using[^1]:
    ```
    python project.py
    ```
2. A prompt will appear asking what action you would like to take:
    ```
    ----------------------------------------------
    1: View the names of all the plants available
    2: Find plant care information for a specific plant
    3: Scrape plant data and save as a file
    4: Exit application

    What would you like to do?:
    ```

3. When you type in 2 a prompt will appear, type in the name of the plant you want care information for[^2][^3]:
    ```
    Plant name: jade plant
    ```

4. The output generated looks like:
    ```
    Crassula Ovata / Jade Plant / Money Plant / Crassula Argentea
    ---------------
    -Soil: Use a loose potting soil that drains quickly.
    -Ideal Temperature (°C): 35
    -Light Requirements: Strong light ( 21,500 to 3,200 lux/2000 to 300 fc)
    -Light Ideal: Full sun (+21,500 lux /+2000 fc )
    -Water Frequency: Must dry between watering  &  Water only when dry
    ```

[^1]: Make sure to ```pip install``` all required libraries in ```requirements.txt```
[^2]: If there is no found care information the output is:
        ```
        Sorry, we do not have information on that plant.
        ```
[^3]: Names are case-insensitive. Both scientific and common names are accepted.

### *\*This is my submission for the final project in Harvard's CS50P.*
&nbsp;

#
## Developer/Project Notes:
This project consists of four python files: ```project.py```, ```scrape.py``` and two seperate test files.


```scrape.py``` is meant to be run from the command line: it scrapes plant care data from all of the relevant houseplant pages on tropicopia.com and houseplant411.com, stores each plant's cleaned data in an individual dictionary, and then writes the list of plant dictionaries to a csv file named ```plant_data.csv```.

- Tropicopia.com contains 355 individual houseplant webpages; houseplant411.com/houseplant contains 141 webpages. The data from these two pages were combined in a "left join" process: all the plants in Tropicopia were preserved and only relevant soil and extra name data from houseplant411 was added to the plants in Tropicopia. 107 plants were left after combining repeated plants (plants with the same common name or plants of the same genus) into one plant entry.

- The ```Beautiful Soup``` package was used to scrape the data. Both websites are popular sources and were chosen specifically to practice web scraping from moderately messy sources.

- ```scrape.py``` intentionally does not use the ```pandas``` library in order to practice using and managing different data structures in Python. The most difficult part of this project was learning how to store and clean the scraped data.

The main file, ```project.py```, is also run from the command line and uses data from ```plant_data.csv``` to provide information on the requested houseplant.

- There are four actions the user can take when project.py is run: print a list of all of the potential plants they can ask about; ask about a specific houseplant; re-scrape the data; or exit the program. The user will be prompted on what action to take until they exit the program.

- If ```plant_data.csv``` is missing from the folder that ```project.py``` is run, then the ```get_data()``` function, from ```scrape.py```, that creates the csv file is automatically run.

- ```pandas``` is used here to create a Dataframe of the data in ```plant_data.csv```. The data from that dataframe is then stored in a list containing individual ```Plant``` objects that, when printed, displays formatted soil, temperature, light, and water information for that plant. The ```Plant``` class also contains methods (such as getters, setters, and ```add_names()```) that would be helpful in the future if care information needed to be updated.

The test files contain unit/functional tests that should be run using the ```pytest``` framework.

&nbsp;
&nbsp;

### A few things that could get changed to improve this project:
- There is probably a way to improve the performance when scraping from the two websites: reading and storing data from houseplant411 takes significantly longer than Tropicopia (up to 5 minutes vs about a minute.)

- Some of the data is still not as clean as it could be: there may be some leftover duplicate names and the soil information in particular is not standardized and may look a bit funky compared to the other information.

- Different sources could be more useful if this project were to be useful for the general public: some common houseplants are missing, a lot of the data is not standardized or it is not in the most accessible format for laymen, and care information could also differ depending on the overall environment the plant would be living in.

- Overall the code in ```scrape.py``` is probably not using the most space or time efficient way to store the plant data. Some of the for loops could potentially be refactored to be more efficient.
