#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

import requests
from bs4 import BeautifulSoup

__version__ = '1.0'


def scrape_recipe(url):
    '''Scrapes information from recipe web page

    Args:
        url (str): URL for the recipe
    '''
    info = {}
    return info


if __name__ == '__main__':

    #     import sys
    #     def usage(exit_status):
    #         msg = '\n ... \n'
    #
    #         print(msg)
    #         sys.exit(exit_status)
    #
    #     import getopt
    #
    #    # parse command line options/arguments
    #     try:
    #         opts, args = getopt.getopt(sys.argv[1:],
    #                                    'hd:', ['help', 'dir='])
    #     except getopt.GetoptError:
    #         usage(3)
    #
    #     for opt, arg in opts:
    #         if opt in ('-h', '--help'):
    #             usage(0)
    #         if opt in ('-d', '--dir'):
    #             thedir = arg

    pass
