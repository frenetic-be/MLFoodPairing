#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for food2fork
'''
# import os
# import sys
import unittest

import requests
import food2fork


class TestAPIKey(unittest.TestCase):
    '''Class to test if API key works
    '''

    def test_food2fork_recipe_request(self):
        '''Testing if food2fork API key works
        '''
        url = 'http://food2fork.com/api/get'
        params = {
            'key': food2fork.FOOD2FORK_API_KEY,
            'rId': 29159
        }
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue('recipe' in data)

    def test_food2fork_search_request(self):
        '''Testing if food2fork API key works
        '''
        url = 'http://food2fork.com/api/search'
        params = {
            'key': food2fork.FOOD2FORK_API_KEY,
            'q': 'avocado'
        }
        response = requests.get(url, params=params)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue('recipes' in data)

if __name__ == '__main__':
    unittest.main()
