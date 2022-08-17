""" Tests functions/methods in project.py"""

import pytest
import pandas as pd
from project import (
    Plant,
    format_data,
    ask_action,
    all_plants,
    find_info)

def test_plant():
    """ Tests all functionality of the Plant class """
    # Test Plant properties and format()
    p = Plant("name")
    p.name = "name1"
    assert p.name == ["name1"]
    p.name = ["Name1","Name2"]
    assert p.name == ["name1","name2"]
    with pytest.raises(ValueError):
        p.name = 1

    p.soil = 1
    assert p.soil is None
    p.soil = "soil"
    assert p.soil == "soil"
    assert p.format("soil","-Soil: ",p.soil) == "-Soil: soil"

    p.water = 1
    assert p.water is None
    p.water = "water"
    assert p.water == "water"
    assert p.format("water","-Water: ",p.water) == "-Water: water"

    assert p.temp is None
    p.temp = 50
    assert p.temp == (50,None)
    assert p.format("temp","-Ideal Temperature (°C): ",p.temp) == "-Ideal Temperature (°C): 50"
    p.temp = (100,50)
    assert p.temp == (100,50)
    assert p.format("temp","-Ideal Temperature (°C): ",p.temp) == (
                "-Ideal Temperature (°C): 50 to 100")

    p.light = 1
    assert p.light is None
    p.light = "light1"
    assert p.light == ("light1",None)
    assert p.format("light","-Light Requirements: ",p.light) == "-Light Requirements: light1"
    p.light = ("light1","light2", "light3")
    assert p.light == ("light1","light2")
    assert p.format("light","-Light Requirements: ",p.light) == (
                "-Light Requirements: light2\n-Light Ideal: light1")

    # Test add_names
    p.add_names("name3")
    assert p.name == ["name1","name2","name3"]
    p.add_names(["a","b"])
    assert p.name == ["name1","name2","name3","a","b"]
    with pytest.raises(ValueError):
        p.add_names(1)

    # Test that str(Plant()) returns care information
    p = Plant(name=["a","b","c"],soil="clay",temp=(10,5),light=("some","high"),water="often")
    assert str(p) == ("A / B / C\n---------------\n-Soil: clay\n" +
                    "-Ideal Temperature (°C): 5 to 10\n-Light Requirements: high\n" +
                    "-Light Ideal: some\n-Water Frequency: often\n")


def test_format_data():
    """ Tests to make sure data is read and stored from csv correctly"""
    d = {"name":["a,b"],"soil":["soil"],"temp max":[1],"temp min":[2],
        "light ideal":"light i","light tolerated":"light t","water":["water"]}
    df = pd.DataFrame(data=d)
    plant_list = format_data(df)
    assert plant_list[0].name == ["a","b"]
    assert plant_list[0].soil == "soil"
    assert plant_list[0].temp == (1,2)
    assert plant_list[0].light == ("light i","light t")
    assert plant_list[0].water == "water"

def test_ask_action(monkeypatch):
    """ Tests if returning correct user input """
    # monkeypatch is built into pytest
    # allows to test input
    monkeypatch.setattr('builtins.input', lambda _:"1")
    assert ask_action() == 1
    monkeypatch.setattr('builtins.input', lambda _:"2")
    assert ask_action() == 2
    monkeypatch.setattr('builtins.input', lambda _:"3")
    assert ask_action() == 3
    monkeypatch.setattr('builtins.input', lambda _:"4")
    assert ask_action() == 4
    monkeypatch.setattr('builtins.input', lambda _:"abc")

def test_all_plants():
    """ Test that all the names are returned in format"""
    plant_list = ([Plant(["aa","cc"],"soil"),
                    Plant("bb","soil")])
    assert all_plants(plant_list) == ["+ Aa / Cc", "+ Bb"]

def test_find_info(monkeypatch):
    # monkeypatch is built into pytest
    # allows to test input
    monkeypatch.setattr('builtins.input', lambda _:"b")
    p = Plant(name=["a","b","c"],soil="clay",temp=(10,5),
                light=("some","high"),water="often")
    plant_list = ([Plant(["not","this"],"soil"),
                    Plant("nope","soil"),p])
    find_info(plant_list) == ("A / B / C\n---------------\n-Soil: clay\n" +
                    "-Ideal Temperature (°C): 5 to 10\n-Light Requirements: high\n" +
                    "-Light Ideal: some\n-Water Frequency: often\n")

