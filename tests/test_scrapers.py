#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for food2fork.scrapers
'''
# import os
# import sys
import unittest

from food2fork.scrapers import (
    AllRecipes,
    BBC,
    BBCGoodFood,
    BonAppetit,
    BunkyCooks,
    Chow,
    ClosetCooking,
    CookieAndKate,
    CookinCanuck,
    Epicurious,
    FineDiningLovers,
    HealthyDelicious,
    JamieOliver,
    MyBakingAddiction,
    NaturallyElla,
    OneOOneCookbooks,
    SimplyRecipes,
    SteamyKitchen,
    TastyKitchen,
    ThePioneerWoman,
    TwoPeasAndTheirPod
)


class TestScraping(unittest.TestCase):
    '''Class to test web scraping
    '''

    def test_allrecipes(self):
        '''Testing the AllRecipes scraper
        '''
        url = 'http://allrecipes.com/Recipe/Basic-Crepes/Detail.aspx'
        scraper = AllRecipes(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, ['cooktime', 'preptime', 'rating', 'reviews'])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_bbc(self):
        '''Testing the BBC scraper
        '''
        url = 'http://www.bbc.co.uk/food/recipes/naan_86626'
        scraper = BBC(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, ['cooktime', 'preptime'])
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_bbc_good_food(self):
        '''Testing the BBCGoodFood scraper
        '''
        url = 'http://www.bbcgoodfood.com/recipes/2538/beef-wellington'
        scraper = BBCGoodFood(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, ['cooktime', 'difficulty', 'rating', 'reviews'])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['difficulty'])

    def test_closet_cooking(self):
        '''Testing the ClosetCooking scraper
        '''
        url = ('http://www.closetcooking.com/2011/08/'
               'buffalo-chicken-grilled-cheese-sandwich.html')
        scraper = ClosetCooking(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, ['cooktime', 'preptime'])
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_101_cookbooks(self):
        '''Testing the OneOOneCookbooks scraper
        '''
        url = ('http://www.101cookbooks.com/archives/'
               'cilantro-salad-recipe.html')
        scraper = OneOOneCookbooks(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, ['cooktime', 'preptime'])
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_the_pioneer_woman(self):
        '''Testing the ThePioneerWoman scraper
        '''
        url = ('http://thepioneerwoman.com/cooking/2008/03/'
               'my_most_favorite_salad_ever_ever_ever_ever/')
        scraper = ThePioneerWoman(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, ['cooktime', 'preptime'])
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_jamie_oliver(self):
        '''Testing the JamieOliver scraper
        '''
        url = ('http://www.jamieoliver.com/recipes/chicken-recipes/'
               'perfect-roast-chicken')
        scraper = JamieOliver(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, ['cooktime', 'difficulty'])
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['difficulty'])

    def test_cookie_and_kate(self):
        '''Testing the CookieAndKate scraper
        '''
        url = 'http://cookieandkate.com/2010/baked-sweet-potato-fries/'
        scraper = CookieAndKate(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, ['cooktime', 'preptime', 'rating', 'reviews'])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_simply_recipes(self):
        '''Testing the SimplyRecipes scraper
        '''
        url = 'http://www.simplyrecipes.com/recipes/cheesy_bread/'
        scraper = SimplyRecipes(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, ['cooktime', 'preptime', 'rating', 'reviews'])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_two_peas_and_their_pod(self):
        '''Testing the TwoPeasAndTheirPod scraper
        '''
        url = ('http://www.twopeasandtheirpod.com/'
               'guacamole-grilled-cheese-sandwich/')
        scraper = TwoPeasAndTheirPod(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, ['cooktime', 'preptime', 'rating', 'reviews'])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_bon_appetit(self):
        '''Testing the BonAppetit scraper
        '''
        url = 'https://www.bonappetit.com/recipe/quinoa-tabbouleh'
        scraper = BonAppetit(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, ['rating', 'reviews'])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))

    def test_bunkycooks(self):
        '''Testing the BunkyCooks scraper
        '''
        url = ('http://www.bunkycooks.com/2011/12/'
               'the-best-three-cheese-lasagna-recipe/')
        scraper = BunkyCooks(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, [
            'cooktime',
            'preptime'
        ])
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_chow(self):
        '''Testing the Chow scraper
        '''
        url = ('http://www.chow.com/recipes/'
               '13563-roasted-spaghetti-squash-with-parmigiano-reggiano')
        scraper = Chow(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, [
            'cooktime',
            'difficulty',
            'rating',
            'reviews',
        ])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['difficulty'])

    def test_cookincanuck(self):
        '''Testing the CookinCanuck scraper
        '''
        url = ('http://www.cookincanuck.com/2011/11/'
               'cannellini-bean-vegetarian-meatballs'
               '-with-tomato-sauce-recipe/')
        scraper = CookinCanuck(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, [
            'cooktime',
            'preptime',
            'rating',
            'reviews',
        ])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_epicurious(self):
        '''Testing the Epicurious scraper
        '''
        url = ('https://www.epicurious.com/recipes/food/views/'
               'Poached-Eggs-in-Tomato-Sauce-with-Chickpeas-and-Feta-368963')
        scraper = Epicurious(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, [
            'cooktime',
            'preptime',
            'rating',
            'reviews',
        ])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_finedininglovers(self):
        '''Testing the FineDiningLovers scraper
        '''
        url = ('https://www.finedininglovers.com/recipes/side/'
               'vegetable-lasagna-recipe/')
        scraper = FineDiningLovers(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, [
            'cooktime',
            'preptime',
            'rating',
            'reviews'
        ])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_healthydelicious(self):
        '''Testing the HealthyDelicious scraper
        '''
        url = ('https://www.healthy-delicious.com/'
               'baked-chicken-and-spinach-flautas/')
        scraper = HealthyDelicious(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, [
            'cooktime',
            'preptime',
            'rating',
            'reviews',
        ])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_mybakingaddiction(self):
        '''Testing the MyBakingAddiction scraper
        '''
        url = ('https://www.mybakingaddiction.com/'
               'mac-and-cheese-roasted-chicken-and-goat-cheese/')
        scraper = MyBakingAddiction(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, [
            'cooktime',
            'preptime',
        ])
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_naturallyella(self):
        '''Testing the NaturallyElla scraper
        '''
        url = 'https://naturallyella.com/black-bean-tacos/'
        scraper = NaturallyElla(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, [
            'cooktime',
            'preptime',
            'rating',
            'reviews',
        ])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_steamykitchen(self):
        '''Testing the SteamyKitchen scraper
        '''
        url = 'https://steamykitchen.com/271-vietnamese-pho-recipe.html'
        scraper = SteamyKitchen(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, [
            'cooktime',
            'preptime',
            'rating',
            'reviews',
        ])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])

    def test_tastykitchen(self):
        '''Testing the TastyKitchen scraper
        '''
        url = 'http://tastykitchen.com/recipes/drinks/frozen-hot-chocolate-2/'
        scraper = TastyKitchen(url)
        self.assertEqual(scraper.status, 200)
        info = scraper.get_all_info()
        keys = sorted(info.keys())
        self.assertEqual(keys, [
            'cooktime',
            'difficulty',
            'preptime',
            'rating',
            'reviews',
        ])
        self.assertTrue(isinstance(info['rating'], float))
        self.assertTrue(isinstance(info['reviews'], int))
        self.assertIsNotNone(info['cooktime'])
        self.assertIsNotNone(info['preptime'])
        self.assertIsNotNone(info['difficulty'])

if __name__ == '__main__':
    unittest.main()
