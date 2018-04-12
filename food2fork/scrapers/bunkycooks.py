#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.bunkycooks
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

import re

from food2fork.scrapers.base import Scraper, checkstatus


class BunkyCooks(Scraper):
    '''BunkyCooks scraper class
    '''

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
