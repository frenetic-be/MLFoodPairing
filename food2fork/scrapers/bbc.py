#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.bbc
.. moduleauthor:: Julien Spronck
.. created:: April 2018
'''

from food2fork.scrapers.base import Scraper, checkstatus


class BBC(Scraper):
    '''BBC scraper class
    '''

    @checkstatus
    def get_prep_time(self):
        '''Get prep time from web page
        '''
        time = self.soup.select('p.recipe-metadata__prep-time')
        if time and 'content' in time[0].attrs:
            return time[0].attrs['content']

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        time = self.soup.select('p.recipe-metadata__cook-time')
        if time and 'content' in time[0].attrs:
            return time[0].attrs['content']
