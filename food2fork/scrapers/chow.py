#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.chow
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

from food2fork.scrapers.base import Scraper, checkstatus


class Chow(Scraper):
    '''Chow scraper class
    '''

    @checkstatus
    def get_rating(self):
        '''Get rating from web page
        '''
        rating = self.soup.select('span[itemprop="ratingValue"]')
        if rating:
            return float(rating[0].text.strip())

    @checkstatus
    def get_reviews(self):
        '''Get number of reviews from web page
        '''
        reviews = self.soup.select('span[itemprop="reviewCount"]')
        if reviews:
            return int(reviews[0].text.strip())

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        time = self.soup.select('time[itemprop="totalTime"]')
        if time and 'content' in time[0].attrs:
            return time[0].attrs['content']

    @checkstatus
    def get_difficulty(self):
        '''Get difficulty from web page
        '''
        level = self.soup.select('span.frr_difficulty')
        if level:
            return level[0].text.strip()
