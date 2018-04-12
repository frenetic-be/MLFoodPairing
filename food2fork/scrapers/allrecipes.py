#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.allrecipes
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

import re

from food2fork.scrapers.base import Scraper, checkstatus


class AllRecipes(Scraper):
    '''AllRecipes scraper class
    '''

    @checkstatus
    def get_rating(self):
        '''Get rating from web page
        '''
        rating = self.soup.select('div.rating-stars')
        if rating and 'data-ratingstars' in rating[0].attrs:
            return float(rating[0].attrs['data-ratingstars'])

    @checkstatus
    def get_reviews(self):
        '''Get number of reviews from web page
        '''
        reviews = self.soup.select('span.review-count')
        if reviews:
            match = re.match(r'(\d+) reviews?', reviews[0].text)
            if match:
                return int(match.group(1))

    @checkstatus
    def get_prep_time(self):
        '''Get prep time from web page
        '''
        time = self.soup.select('time[itemprop="prepTime"]')
        if time and 'datetime' in time[0].attrs:
            return time[0].attrs['datetime']

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        time = self.soup.select('time[itemprop="totalTime"]')
        if time and 'datetime' in time[0].attrs:
            return time[0].attrs['datetime']
