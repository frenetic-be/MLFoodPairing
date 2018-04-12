#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.steamykitchen
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

from food2fork.scrapers.base import Scraper, checkstatus


class SteamyKitchen(Scraper):
    '''SteamyKitchen scraper class
    '''

    @checkstatus
    def get_rating(self):
        '''Get rating from web page
        '''
        rating = self.soup.select('span.wprm-recipe-rating-average')
        if rating:
            return float(rating[0].text.strip())

    @checkstatus
    def get_reviews(self):
        '''Get number of reviews from web page
        '''
        reviews = self.soup.select('span.wprm-recipe-rating-count')
        if reviews:
            return int(reviews[0].text.strip())

    @checkstatus
    def get_prep_time(self):
        '''Get prep time from web page
        '''
        divs = self.soup.select('div.wprm-recipe-times-container '
                                'div.wprm-recipe-time-container')
        for div in divs:
            subdiv = div.select('div.wprm-recipe-time-header')
            if subdiv and subdiv[0].text.strip() == 'Prep Time':
                subdiv2 = div.select('div.wprm-recipe-time')
                if subdiv2:
                    return subdiv2[0].text.strip()

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        divs = self.soup.select('div.wprm-recipe-times-container '
                                'div.wprm-recipe-time-container')
        for div in divs:
            subdiv = div.select('div.wprm-recipe-time-header')
            if subdiv and subdiv[0].text.strip() == 'Cook Time':
                subdiv2 = div.select('div.wprm-recipe-time')
                if subdiv2:
                    return subdiv2[0].text.strip()
