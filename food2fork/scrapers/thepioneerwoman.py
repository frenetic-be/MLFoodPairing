#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.scrapers.thepioneerwoman
.. moduleauthor:: Julien Spronck
.. created:: April 2018
'''

from food2fork.scrapers.base import Scraper, checkstatus


class ThePioneerWoman(Scraper):
    '''ThePioneerWoman scraper class
    '''

    @checkstatus
    def get_prep_time(self):
        '''Get prep time from web page
        '''
        time = self.soup.select('div.recipe-summary-time')
        if time:
            dts = time[0].select('dt')
            dds = time[0].select('dd')
            for ddt, ddd in zip(dts, dds):
                if ddt.text.strip() == 'Prep Time:':
                    return ddd.text.strip()

    @checkstatus
    def get_cooking_time(self):
        '''Get cooking time from web page
        '''
        time = self.soup.select('div.recipe-summary-time')
        if time:
            dts = time[0].select('dt')
            dds = time[0].select('dd')
            for ddt, ddd in zip(dts, dds):
                if ddt.text.strip() == 'Cook Time:':
                    return ddd.text.strip()
