#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers._101cookbooks
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

from food2fork.scrapers.base import Scraper, checkstatus


class OneOOneCookbooks(Scraper):
    '''101cookbook scraper class
    '''

    @checkstatus
    def get_prep_time(self):
        '''Get prep time from web page
        '''
        time = self.soup.select('span.preptime span.value-title')
        if time and 'title' in time[0].attrs:
            return time[0].attrs['title']

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        time = self.soup.select('span.cooktime span.value-title')
        if time and 'title' in time[0].attrs:
            return time[0].attrs['title']
