#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.base
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

import requests
from bs4 import BeautifulSoup


def checkstatus(func):
    '''Decorator function that checks the status of the http requests
    before executing the function and returns an empty dictionary
    if the status is not OK.
    '''

    def wrap(self):
        '''Wrapper function
        '''
        if self.status != 200:
            print(f'Warning: bad HTTP request status ({self.status})')
            return {}
        return func(self)

    return wrap


class Scraper(object):
    '''General scraper class
    '''
    def __init__(self, url, headers=None):
        '''Initialization

        Args:
            url (str): url

        Keyword args:
            headers (dic): HTTP headers to use for the HTTP request
        '''
        self.url = url
        if headers:
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url)
        self.status = response.status_code

        self.soup = None
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'lxml')

    @checkstatus
    def get_rating(self):
        '''Get rating from web page
        '''
        pass

    @checkstatus
    def get_reviews(self):
        '''Get number of reviews from web page
        '''
        pass

    @checkstatus
    def get_prep_time(self):
        '''Get prep time from web page
        '''
        pass

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        pass

    @checkstatus
    def get_difficulty(self):
        '''Get difficulty from web page
        '''
        pass

    @checkstatus
    def get_all_info(self):
        '''Get all information from web page
        '''
        info = {}
        rating = self.get_rating()
        if rating:
            info['rating'] = rating
        reviews = self.get_reviews()
        if reviews:
            info['reviews'] = reviews
        preptime = self.get_prep_time()
        if preptime:
            info['preptime'] = preptime
        cooktime = self.get_cooking_time()
        if cooktime:
            info['cooktime'] = cooktime
        difficulty = self.get_difficulty()
        if difficulty:
            info['difficulty'] = difficulty
        return info
