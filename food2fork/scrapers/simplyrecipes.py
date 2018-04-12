#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.simplyrecipes
.. moduleauthor:: Julien Spronck
.. created:: April 2018
'''

import re

from food2fork.scrapers.base import Scraper, checkstatus


class SimplyRecipes(Scraper):
    '''SimplyRecipe scraper class
    '''

    def __init__(self, url):
        '''Initialization

        Args:
            url (str): url
        '''
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/56.0.2924.76 Safari/537.36')
        }

        super().__init__(url, headers=headers)

    @checkstatus
    def get_rating(self):
        '''Get rating from web page
        '''
        rating = self.soup.select('span.rating-value')
        if rating and 'style' in rating[0].attrs:
            match = re.search(r'width:(\d+)px', rating[0].attrs['style'])
            if match:
                return float(match.group(1))/100*5

    @checkstatus
    def get_reviews(self):
        '''Get number of reviews from web page
        '''
        reviews = self.soup.select('span.total-count.ratings')
        if reviews:
            return int(reviews[0].text)

    @checkstatus
    def get_prep_time(self):
        '''Get prep time from web page
        '''
        time = self.soup.select('span.preptime')
        if time and 'content' in time[0].attrs:
            return time[0].attrs['content']

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        time = self.soup.select('span.cooktime')
        if time and 'content' in time[0].attrs:
            return time[0].attrs['content']
