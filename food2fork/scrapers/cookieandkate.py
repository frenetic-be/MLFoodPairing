#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.cookieandkate
.. moduleauthor:: Julien Spronck
.. created:: April 2018
'''

from food2fork.scrapers.base import Scraper, checkstatus


class CookieAndKate(Scraper):
    '''CookieAndKate scraper class
    '''

    @checkstatus
    def get_rating(self):
        '''Get rating from web page
        '''
        rating = self.soup.select('span.average')
        if rating:
            return float(rating[0].text)

    @checkstatus
    def get_reviews(self):
        '''Get number of reviews from web page
        '''
        reviews = self.soup.select('span.count')
        if reviews:
            return int(reviews[0].text)

    @checkstatus
    def get_prep_time(self):
        '''Get prep time from web page
        '''
        time = self.soup.select('span.tasty-recipes-prep-time')
        if time:
            return time[0].text

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        time = self.soup.select('span.tasty-recipes-cook-time')
        if time:
            return time[0].text
