#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''
import json
import re

import pymongo
import requests
from bs4 import BeautifulSoup

from food2fork.config import FOOD2FORK_API_KEY
import food2fork.ingredient_parser as parser
import food2fork.scrapers as scrapers

__version__ = '1.0'

# Database connection
client = pymongo.MongoClient('mongodb://localhost:27017')
dbfood = client.food2forkDB.food2fork


def scrape_f2f_recipe(url):
    '''Scrapes information from recipe web page

    Args:
        url (str): URL for the recipe
    '''
    info = {}

    response = requests.get(url)

    if response.status_code != 200:
        return {}

    soup = BeautifulSoup(response.text, "lxml")

    # Get ingredient list
    ingredients = soup.select('li[itemprop="ingredients"]')
    # ingredients = [parser.get_ingredient_from_phrase(ingredient.text.strip())
    #                for ingredient in ingredients]
    ingredients = [ingredient.text.strip() for ingredient in ingredients]
    if ingredients:
        info['raw_ingredients'] = ingredients

    # Get social media stats
    social = soup.select('div.social-info div.pull-left')
    media = {}
    for span in social:
        match = re.search(r'(\d+)\s+(likes|tweets|plusses|pins|views)',
                          span.text.lower())
        if match:
            number = int(match.group(1))
            network = match.group(2)
            media[network] = number
    if media:
        info['media'] = media

    # Get rank
    rank = soup.select('div.rating span')
    if rank:
        info['social_rank'] = rank[0].text

    # Get title
    title = soup.select('h1.recipe-title')
    if title:
        info['title'] = title[0].text

    # Get nutritional information
    nutrition_rows = soup.select('table.nutrition tr')
    nutrition = {}
    for row in nutrition_rows:
        match = re.search(r'^(\w[\w\s]*)\s+([\d\.]+m?g?)$',
                          row.text.strip().lower())
        if match:
            cat = match.group(1)
            number = match.group(2)
            nutrition[cat] = number
    if nutrition:
        info['nutrition'] = nutrition

    return info


def scrape_original_recipe(url, publisher):
    '''Scrapes information from original recipe web page

    Args:
        url (str): URL for the recipe
    '''
    scraping_dict = {
        "All Recipes": scrapers.AllRecipes,
        "101 Cookbooks": scrapers.OneOOneCookbooks,
        "Simply Recipes": scrapers.SimplyRecipes,
        "Two Peas and Their Pod": scrapers.TwoPeasAndTheirPod,
        "The Pioneer Woman": scrapers.ThePioneerWoman,
        "Closet Cooking": scrapers.ClosetCooking,
        "Cookie and Kate": scrapers.CookieAndKate,
        "Jamie Oliver": scrapers.JamieOliver,
        "BBC Food": scrapers.BBC,
        "BBC Good Food": scrapers.BBCGoodFood,
        "Bon Appetit": scrapers.BonAppetit,
        "Bunky Cooks": scrapers.BunkyCooks,
        "Chow": scrapers.Chow,
        "Cookin Canuck": scrapers.CookinCanuck,
        "Epicurious": scrapers.Epicurious,
        "Fine Dining Lovers": scrapers.FineDiningLovers,
        "Healthy Delicious": scrapers.HealthyDelicious,
        "My Baking Addiction": scrapers.MyBakingAddiction,
        "Naturally Ella": scrapers.NaturallyElla,
        "Steamy Kitchen": scrapers.SteamyKitchen,
        "Tasty Kitchen": scrapers.TastyKitchen,
    }

    if publisher not in scraping_dict:
        return {}

    scraper_cls = scraping_dict[publisher]
    scraper = scraper_cls(url)
    return scraper.get_all_info()


def add_recipe_to_db(recipe):
    '''Adds a recipe to the database

    Args:
        recipe (dict): dictionary with recipe data
    '''
    if dbfood.find_one({'recipe_id': recipe['recipe_id']}) is None:
        dbfood.insert_one(recipe)


def get_api_data(page=0):
    '''Retrieve data from the food2fork API
    '''
    url = 'http://food2fork.com/api/search'
    params = {
        'key': FOOD2FORK_API_KEY,
        'page': page
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f'Bad HTTP request ({response.status_code})')
        return

    for j, recipe in enumerate(response.json()['recipes']):
        print(f'Processing {j+1}/30')

        if dbfood.find_one({'recipe_id': recipe['recipe_id']}) is not None:
            continue
        try:
            # Add data from food2fork
            info1 = scrape_f2f_recipe(recipe['f2f_url'])
            for key, val in info1.items():
                if key not in recipe:
                    recipe[key] = val

            # Add data from publisher
            info2 = scrape_original_recipe(recipe['source_url'],
                                           recipe['publisher'])
            for key, val in info2.items():
                if key not in recipe:
                    recipe[key] = val

            # Add recipe to database
            add_recipe_to_db(recipe)
        except (requests.TooManyRedirects, requests.ConnectionError):
            continue


if __name__ == '__main__':

    #     import sys
    #     def usage(exit_status):
    #         msg = '\n ... \n'
    #
    #         print(msg)
    #         sys.exit(exit_status)
    #
    #     import getopt
    #
    #    # parse command line options/arguments
    #     try:
    #         opts, args = getopt.getopt(sys.argv[1:],
    #                                    'hd:', ['help', 'dir='])
    #     except getopt.GetoptError:
    #         usage(3)
    #
    #     for opt, arg in opts:
    #         if opt in ('-h', '--help'):
    #             usage(0)
    #         if opt in ('-d', '--dir'):
    #             thedir = arg

    pass
