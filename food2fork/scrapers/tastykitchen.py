#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.tastykitchen
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

import re

from food2fork.scrapers.base import Scraper, checkstatus


class TastyKitchen(Scraper):
    '''TastyKitchen scraper class
    '''

    @checkstatus
    def get_rating(self):
        '''Get rating from web page
        '''
        reviews = self.soup.select('div.post-ratings span.average a')
        if reviews:
            match = re.match(r'([\d\.]+) Mitt\(s\)?', reviews[0].text)
            if match:
                return float(match.group(1))

    @checkstatus
    def get_reviews(self):
        '''Get number of reviews from web page
        '''
        reviews = self.soup.select('div.post-ratings span.total a')
        if reviews:
            match = re.match(r'(\d+) Rating\(s\)?', reviews[0].text)
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
        time = self.soup.select('time[itemprop="cookTime"]')
        if time and 'datetime' in time[0].attrs:
            return time[0].attrs['datetime']

    @checkstatus
    def get_difficulty(self):
        '''Get difficulty from web page
        '''
        pars = self.soup.select('div.recent-recipe-meta form p')
        for par in pars:
            match = re.match(r'Level:\s*(.+)', par.text.strip())
            if match:
                return match.group(1).strip()
