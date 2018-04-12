#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.jamieoliver
.. moduleauthor:: Julien Spronck
.. created:: April 2018
'''

from food2fork.scrapers.base import Scraper, checkstatus


class JamieOliver(Scraper):
    '''JamieOliver scraper class
    '''

    @checkstatus
    def get_difficulty(self):
        '''Get difficulty from web page
        '''
        level = self.soup.select('div.recipe-detail.difficulty')
        if level:
            return ' '.join(level[0].findAll(text=True,
                                             recursive=False)).strip()

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        time = self.soup.select('div.recipe-detail.time')
        if time:
            return ' '.join(time[0].findAll(text=True,
                                            recursive=False)).strip()
