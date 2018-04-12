#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.bonappetit
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

import re

from food2fork.scrapers.base import Scraper, checkstatus


class BonAppetit(Scraper):
    '''BonAppetit scraper class
    '''

    @checkstatus
    def get_rating(self):
        '''Get rating from web page
        '''
        rating = self.soup.select('div.review-rating-container')
        if rating and 'class' in rating[0].attrs:
            for clas in rating[0].attrs['class']:
                match = re.match(r'([\d\.]+)-stars', clas)
                if match:
                    return float(match.group(1))

    @checkstatus
    def get_reviews(self):
        '''Get number of reviews from web page
        '''
        reviews = self.soup.select('span.review-count')
        if reviews:
            match = re.match(r'(\d+) Ratings?', reviews[0].text)
            if match:
                return int(match.group(1))
