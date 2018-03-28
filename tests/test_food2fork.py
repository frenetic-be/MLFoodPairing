#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Tests for food2fork
'''
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import food2fork


class TestStringMethods(unittest.TestCase):
    '''Class to test blah
    '''

    def test_upper(self):
        '''Testing blah ...
        '''
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        '''Testing blah ...
        '''
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        '''Testing blah ...
        '''
        s = 'hello world'
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()