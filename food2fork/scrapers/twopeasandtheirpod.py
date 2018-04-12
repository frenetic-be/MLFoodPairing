#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.twopeasandtheirpod
.. moduleauthor:: Julien Spronck
.. created:: April 2018
'''


from food2fork.scrapers.base import Scraper, checkstatus


class TwoPeasAndTheirPod(Scraper):
    '''TwoPeasAndTheirPod scraper class
    '''

    @checkstatus
    def get_rating(self):
        '''Get rating from web page
        '''
        rating = self.soup.select('span.crfp-rating')
        if rating:
            return float(rating[0].text)

    @checkstatus
    def get_reviews(self):
        '''Get number of reviews from web page
        '''
        reviews = self.soup.select('div.review-total a.reviews')
        if reviews:
            return int(reviews[0].text.split()[0])

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
