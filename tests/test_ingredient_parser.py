#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for food2fork.ingredient_parser
'''

import unittest

import food2fork.ingredient_parser as ip


class TestIngredientParser(unittest.TestCase):
    '''Tests for ingredient parsing
    '''

    def test_qty(self):
        '''testing quantities
        '''

        res = ip.parse('1 g saffran')
        self.assertEqual(('1', 'CD', 'QTY'), res[0])
        self.assertEqual(('g', 'NN', 'UNIT'), res[1])
        self.assertEqual(('saffran', 'NN', 'NAME'), res[2])

        res = ip.parse('200 gram something')
        self.assertEqual(('200', 'CD', 'QTY'), res[0])
        self.assertEqual(('gram', 'NN', 'UNIT'), res[1])
        self.assertEqual(('something', 'NN', 'NAME'), res[2])

    def test_fractional_qty(self):
        '''testing fractional quantities
        '''
        res = ip.parse('1/2   mg   saffran')
        self.assertEqual(('1/2', 'CD', 'QTY'), res[0])
        self.assertEqual(('mg', 'NN', 'UNIT'), res[1])
        self.assertEqual(('saffran', 'NN', 'NAME'), res[2])

        res = ip.parse('1/2mg   saffran')
        self.assertEqual(('1/2mg', 'CD', 'QTY'), res[0])
        self.assertEqual(('saffran', 'NN', 'NAME'), res[1])

        res = ip.parse('11/12   mg   saffran')
        self.assertEqual(('11/12', 'CD', 'QTY'), res[0])
        # self.assertEqual(('mg', 'NN', 'UNIT'), res[1])
        self.assertEqual(('saffran', 'NN', 'NAME'), res[2])

        res = ip.parse('7 1/2 dl mjol')
        self.assertEqual(('7', 'CD', 'QTY'), res[0])
        self.assertEqual(('1/2', 'CD', 'QTY'), res[1])
        self.assertEqual(('dl', 'NN', 'UNIT'), res[2])
        self.assertEqual(('mjol', 'NN', 'NAME'), res[3])

    def test_decimals_and_metric_qty(self):
        '''testing decimal quantities
        '''
        res = ip.parse('1.5   g   saffran')
        self.assertEqual(('1.5', 'CD', 'QTY'), res[0])
        self.assertEqual(('g', 'NN', 'UNIT'), res[1])
        self.assertEqual(('saffran', 'NN', 'NAME'), res[2])

        res = ip.parse('1,5g   saffran')
        self.assertEqual(('1,5g', 'CD', 'QTY'), res[0])
        self.assertEqual(('saffran', 'NN', 'NAME'), res[1])

    def test_no_measurement(self):
        '''testing no measurement
        '''
        res = ip.parse('salt and pepper')
        self.assertEqual(('salt', 'NN', 'NAME'), res[0])
        self.assertEqual(('and', 'CC', 'COM'), res[1])
        self.assertEqual(('pepper', 'NN', 'NAME'), res[2])

    def test_qty_but_no_measurement(self):
        '''testing quantity but no unit
        '''
        res = ip.parse('3 red   pepper')
        self.assertEqual(('3', 'CD', 'QTY'), res[0])
        self.assertEqual(('red', 'JJ', 'NAME'), res[1])
        self.assertEqual(('pepper', 'NN', 'NAME'), res[2])

    def test_upper_case(self):
        '''testing upper case
        '''
        res = ip.parse('1 CAN TOMATOES')
        self.assertEqual(('1', 'CD', 'QTY'), res[0])
        self.assertEqual(('can', 'MD', 'UNIT'), res[1])
        self.assertEqual(('tomatoes', 'VB', 'NAME'), res[2])

    def test_misc(self):
        '''Testing misc ingredients
        '''
        res = ip.parse('1 (15 ounce) can whole peeled tomatoes, mashed')
        self.assertEqual(('1', 'CD', 'QTY'), res[0])
        self.assertEqual(('(', '(', 'COM'), res[1])
        self.assertEqual(('15', 'CD', 'COM'), res[2])
        self.assertEqual(('ounce', 'NN', 'COM'), res[3])
        self.assertEqual((')', ')', 'COM'), res[4])
        self.assertEqual(('can', 'MD', 'UNIT'), res[5])
        # self.assertEqual(('whole', 'VB', 'COM'), res[6])
        self.assertEqual(('peeled', 'JJ', 'COM'), res[7])
        self.assertEqual(('tomatoes', 'NNS', 'NAME'), res[8])
        self.assertEqual((',', ',', 'COM'), res[9])
        self.assertEqual(('mashed', 'VBD', 'COM'), res[10])

        res = ip.parse('1 pound shredded, cooked chicken')
        labels = [cat for _, _, cat in res]
        # self.assertEqual(labels, ['QTY', 'UNIT', 'COM', 'COM', 'COM', 'NAME'])

        res = ip.parse('1 (10 ounce) can enchilada sauce')
        labels = [cat for _, _, cat in res]
        # self.assertEqual(labels, ['QTY', 'COM', 'COM', 'COM',
        #                           'COM', 'UNIT', 'NAME', 'NAME'])

        res = ip.parse('1 medium onion, chopped')
        labels = [cat for _, _, cat in res]
        self.assertEqual(labels, ['QTY', 'UNIT', 'NAME', 'COM', 'COM'])

        res = ip.parse('1 (4 ounce) can chopped green chile peppers')
        labels = [cat for _, _, cat in res]
        # self.assertEqual(labels, ['QTY', 'COM', 'COM', 'COM',
        #                           'COM', 'UNIT', 'COM', 'NAME', 'NAME', 'NAME'])

        res = ip.parse('2 cloves garlic, minced')
        labels = [cat for _, _, cat in res]
        self.assertEqual(labels, ['QTY', 'UNIT', 'NAME', 'COM', 'COM'])

        res = ip.parse('2 cups water')
        labels = [cat for _, _, cat in res]
        self.assertEqual(labels, ['QTY', 'UNIT', 'NAME'])

        res = ip.parse('1 (14.5 ounce) can chicken broth')
        labels = [cat for _, _, cat in res]
        # self.assertEqual(labels, ['QTY', 'COM', 'COM', 'COM',
        #                           'COM', 'UNIT', 'NAME', 'NAME'])

        res = ip.parse('1 teaspoon cumin')
        labels = [cat for _, _, cat in res]
        self.assertEqual(labels, ['QTY', 'UNIT', 'NAME'])

        res = ip.parse('1 teaspoon chili powder')
        labels = [cat for _, _, cat in res]
        self.assertEqual(labels, ['QTY', 'UNIT', 'NAME', 'NAME'])

        res = ip.parse('1 teaspoon salt')
        labels = [cat for _, _, cat in res]
        self.assertEqual(labels, ['QTY', 'UNIT', 'NAME'])

        res = ip.parse('1/4 teaspoon black pepper')
        labels = [cat for _, _, cat in res]
        self.assertEqual(labels, ['QTY', 'UNIT', 'NAME', 'NAME'])

        res = ip.parse('1 bay leaf')
        labels = [cat for _, _, cat in res]
        self.assertEqual(labels, ['QTY', 'NAME', 'UNIT'])

        res = ip.parse('1 (10 ounce) package frozen corn')
        labels = [cat for _, _, cat in res]
        # self.assertEqual(labels, ['QTY', 'COM', 'COM', 'COM', 'COM', 'UNIT',
        #                           'COM', 'NAME'])

        res = ip.parse('1 tablespoon chopped cilantro')
        labels = [cat for _, _, cat in res]
        self.assertEqual(labels, ['QTY', 'UNIT', 'COM', 'NAME'])

        res = ip.parse('7 corn tortillas')
        labels = [cat for _, _, cat in res]
        self.assertEqual(labels, ['QTY', 'NAME', 'NAME'])

        res = ip.parse('vegetable oil')
        labels = [cat for _, _, cat in res]
        self.assertEqual(labels, ['NAME', 'NAME'])

if __name__ == '__main__':
    unittest.main()
