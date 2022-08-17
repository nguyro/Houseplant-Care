"""
Tests functions and methods in scrape.py

test_get_data() takes a few minutes
"""

import pytest
import os
from bs4 import BeautifulSoup
from scrape import(
    get_data,
    find_soil,
    remove_repeats,
    read_411_page,
    clean_trop,
    read_trop_page,
    scrape_html)

def test_get_data():
    os.remove("plant_data.csv")
    get_data()
    assert os.path.exists("plant_data.csv")

def test_find_soil():
    small_list = [{'name':["not this","nope"],'soil':"no"},{'name':['save this','matches'],'soil':"yes"}]
    plant_dict = {'name':['entry1','matches'],'categories':'ok'}
    assert find_soil(plant_dict,small_list) == {'name':['entry1','matches','save this'],'categories':'ok','soil':"yes"}

    plant_dict = {'name':['entry1'],'categories':'matches'}
    assert find_soil(plant_dict,small_list) == {'name':['entry1','save this','matches'],'categories':'matches','soil':"yes"}

    plant_dict = {'name':['no match'],'categories':'na'}
    assert find_soil(plant_dict,small_list) == {'name':['no match'],'categories':'na','soil':'No information available'}

def test_remove_repeats():
    data_dict = ([{'name':['valid','valid plant2'],'other':1},
                {'name':['plant3','valid'],'other':2},
                {'name':['not valid'],'other':3}])
    test = remove_repeats(data_dict)
    result = ([{'name':['valid','valid plant2','plant3'],'other':1},
                {'name':['not valid'],'other':3}])
    assert test == result

def test_read_411_page():
    """ Tests if data from houseplant411 is read correctly using read_411_page()"""
    url = "https://www.houseplant411.com/houseplant/african-violet-how-to-grow-care-guide"
    result = ({'name': ['african violet plant','saintpaulia ionanthais'],
            'soil': 'The soil should be a rich, airy, potting mixture. Special soil for '
            'African Violet plants is available at most garden centers. These '
            'plants benefit from some fresh, new soil every 6-12 months. Changing '
            'the soil prevents unwanted salts from fertilizers building up in the '
            'soil and burning the roots and leaves.'})
    assert read_411_page(url) == result


def test_trop():
    """ Tests read_trop_page() and clean_trop() """
    url = "http://www.tropicopia.com/house-plant/detail.np/detail-01.html"
    plant = read_trop_page(url)
    result = ({'appeal': 'Foliage','avaibility': 'Regular',
    'available sizes (pot ø)': '4in to 8in Ø  / 10cm to 20cm Ø',
    'bearing': 'Clump','blooming season': None,'categories': 'Fern',
    'climat': 'Tropical','color of blooms': None,'color of leaf': 'Dark green  &  Light green',
    'common name': 'Rosy Maidenhair, Autralian maidenhair','common name (fr.)': 'Capillaire rosée',
    'description': None,'disease': 'Gray mold','family': 'Polypodiaceae','growth': 'Regular',
    'height at purchase (m)': '0.25','height potential (m)': '0.61',
    'insects': 'Mealy bug  ,  Aphid  &  Snail','latin name': 'Adiantum hispidulum',
    'light ideal': 'Strong light ( 21,500 to 3,200 lux/2000 to 300 fc)',
    'light tolered': 'Diffuse light ( Less than 5,300 lux / 500 fc)',
    'origin': 'Australia & New Guinea','other names': None,'perfume': None,'pot diameter (cm)': '15',
    'pruning': 'Never','style': None,'temperature max. (c°)': '30','temperature min. (c°)': '12',
    'use': 'Table top  ,  Ground cover  &  Tertiary','watering': 'Keep moist between watering  &  Must not dry between watering',
    'width at purchase (m)': '0.15','width potential (m)': '0.91','zone': '10,,,8',})
    assert plant == result

    cleaned = clean_trop(plant)
    result = ({'appeal': 'Foliage','avaibility': 'Regular',
    'available sizes (pot ø)': '4in to 8in Ø  / 10cm to 20cm Ø',
    'bearing': 'Clump','blooming season': None,'categories': 'Fern',
    'climat': 'Tropical','color of blooms': None,'color of leaf': 'Dark green  &  Light green',
    'common name (fr.)': 'Capillaire rosée','description': None,'disease': 'Gray mold',
    'family': 'Polypodiaceae','growth': 'Regular','height at purchase (m)': '0.25',
    'height potential (m)': '0.61','insects': 'Mealy bug  ,  Aphid  &  Snail',
    'light ideal': 'Strong light ( 21,500 to 3,200 lux/2000 to 300 fc)',
    'light tolered': 'Diffuse light ( Less than 5,300 lux / 500 fc)',
    'name': ['adiantum hispidulum','rosy maidenhair','autralian maidenhair'],
    'origin': 'Australia & New Guinea','perfume': None,'pot diameter (cm)': '15',
    'pruning': 'Never','style': None,'temperature max. (c°)': '30','temperature min. (c°)': '12',
    'use': 'Table top  ,  Ground cover  &  Tertiary',
    'watering': 'Keep moist between watering  &  Must not dry between watering',
    'width at purchase (m)': '0.15','width potential (m)': '0.91','zone': '10,,,8',})
    assert cleaned == result

def test_scrape_html():
    url = "http://www.tropicopia.com/house-plant/detail.np/detail-01.html"
    assert isinstance(scrape_html(url), BeautifulSoup)
