#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.bbcgoodfood
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

from food2fork.scrapers.base import Scraper, checkstatus


class BBCGoodFood(Scraper):
    '''BBCGoodFood scraper class
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
        rating = self.soup.select('meta[itemprop="ratingValue"]')
        if rating and 'content' in rating[0].attrs:
            return float(rating[0].attrs['content'])

    @checkstatus
    def get_reviews(self):
        '''Get number of reviews from web page
        '''
        reviews = self.soup.select('meta[itemprop="ratingCount"]')
        if reviews and 'content' in reviews[0].attrs:
            return int(reviews[0].attrs['content'])

    @checkstatus
    def get_difficulty(self):
        '''Get difficulty from web page
        '''
        level = self.soup.select('section.recipe-details__item--skill-level')
        if level:
            return level[0].text.strip()

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        time = self.soup.select('span.recipe-details__cooking-time-cook')
        if time:
            return time[0].text.split(':')[-1].strip()
