#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.epicurious
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

from food2fork.scrapers.base import Scraper, checkstatus


class Epicurious(Scraper):
    '''Epicurious scraper class
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
        '''Get number of reviews from web page
        '''
        data = self.soup.select('span[itemprop="reviewCount"]')
        if data:
            return int(data[0].text.strip())

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
