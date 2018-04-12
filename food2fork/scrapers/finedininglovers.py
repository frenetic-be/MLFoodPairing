#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.finedininglovers
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

from food2fork.scrapers.base import Scraper, checkstatus


class FineDiningLovers(Scraper):
    '''FineDiningLovers scraper class
    '''

    @checkstatus
    def get_rating(self):
        '''Get rating from web page
        '''
        data = self.soup.select('meta[itemprop="ratingValue"]')
        if data and 'content' in data[0].attrs:
            return float(data[0].attrs['content'])

    @checkstatus
    def get_reviews(self):
        '''Get reviews from web page
        '''
        data = self.soup.select('meta[itemprop="ratingCount"]')
        if data and 'content' in data[0].attrs:
            return int(data[0].attrs['content'])

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
