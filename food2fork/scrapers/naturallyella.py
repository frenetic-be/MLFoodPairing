#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.naturallyella
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

from food2fork.scrapers.base import Scraper, checkstatus


class NaturallyElla(Scraper):
    '''NaturallyElla scraper class
    '''

    @checkstatus
    def get_rating(self):
        '''Get rating from web page
        '''
        data = self.soup.select('span.rating-label span.average')
        if data:
            return float(data[0].text.strip())

    @checkstatus
    def get_reviews(self):
        '''Get number of reviews from web page
        '''
        data = self.soup.select('span.rating-label span.count')
        if data:
            return int(data[0].text.strip())

    @checkstatus
    def get_prep_time(self):
        '''Get prep time from web page
        '''
        data = self.soup.select('span.tasty-recipes-prep-time')
        if data:
            return data[0].text.strip()

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        data = self.soup.select('span.tasty-recipes-cook-time')
        if data:
            return data[0].text.strip()
