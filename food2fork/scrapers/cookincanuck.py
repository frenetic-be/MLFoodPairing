#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.cookincanuck
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

import re

from food2fork.scrapers.base import Scraper, checkstatus


class CookinCanuck(Scraper):
    '''CookinCanuck scraper class
    '''

    @checkstatus
    def get_rating(self):
        '''Get rating from web page
        '''
        rating = self.soup.select('div.recipe-rating span.screen-reader-text')
        if rating:
            match = re.match(r'([\d\.]+) rating', rating[0].text)
            if match:
                return float(match.group(1))

    @checkstatus
    def get_reviews(self):
        '''Get number of reviews from web page
        '''
        reviews = self.soup.select('div.sum-ratings')
        if reviews:
            match = re.match(r'(\d+)\s+reviews?', reviews[0].text)
            if match:
                return int(match.group(1))

    @checkstatus
    def get_prep_time(self):
        '''Get prep time from web page
        '''
        time = self.soup.select('meta[itemprop="prepTime"]')
        if time and 'content' in time[0].attrs:
            return time[0].attrs['content']

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        time = self.soup.select('meta[itemprop="cookTime"]')
        if time and 'content' in time[0].attrs:
            return time[0].attrs['content']
