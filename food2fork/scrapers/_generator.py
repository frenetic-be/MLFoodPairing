#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: _generator
.. moduleauthor:: Julien Spronck
.. created:: April 2018
'''

from jinja2 import Template


def generate_file(publisher, rating=True, reviews=True, preptime=True,
                  cooktime=True, difficulty=True):
    '''Generate a scraper file
    '''

    clsname = ''.join(word.title() for word in publisher.split())

    # Generate file
    with open('scraper.template') as fil:
        template = Template(fil.read())

    rendered = template.render(
        clsname=clsname,
        rating=rating,
        reviews=reviews,
        preptime=preptime,
        cooktime=cooktime,
        difficulty=difficulty
    )

    with open(clsname.lower() + '.py', 'w') as outfile:
        print(rendered, file=outfile)

    # Print test script
    print('\n---------------')
    print('- Test script -')
    print('---------------\n')
    print(f'    def test_{clsname.lower()}(self):')
    print(f"        '''Testing the {clsname} scraper")
    print("        '''")
    print("        url = ''")
    print(f"        scraper = {clsname}(url)")
    print("        self.assertEqual(scraper.status, 200)")
    print("        info = scraper.get_all_info()")
    print("        keys = sorted(info.keys())")
    keys = []
    if rating:
        keys.append('rating')
    if reviews:
        keys.append('reviews')
    if cooktime:
        keys.append('cooktime')
    if preptime:
        keys.append('preptime')
    if difficulty:
        keys.append('difficulty')
    keys.sort()

    print("        self.assertEqual(keys, [")
    for key in keys:
        print(f"            '{key}',")
    print("        ])")
    if rating:
        print("        self.assertTrue(isinstance(info['rating'], float))")
    if reviews:
        print("        self.assertTrue(isinstance(info['reviews'], int))")
    if cooktime:
        print("        self.assertIsNotNone(info['cooktime'])")
    if preptime:
        print("        self.assertIsNotNone(info['preptime'])")
    if difficulty:
        print("        self.assertIsNotNone(info['difficulty'])")

    # print import script
    print('\n-----------------')
    print('- import script -')
    print('-----------------\n')
    print(f'from food2fork.scrapers.{clsname.lower()} import {clsname}')

    # print scraping script
    print('\n-------------------')
    print('- scraping script -')
    print('-------------------\n')
    print(f'    elif publisher == "{publisher}":')
    print(f'        scraper_cls = scrapers.{clsname}')

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
