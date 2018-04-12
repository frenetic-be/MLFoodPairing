#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.ingredient_parser.utils
.. moduleauthor:: Julien Spronck
.. created:: March 2018

Utitilies for the CRF model building scripts
'''

import os
import json

from colorama import Fore, Back, Style

MODEL_FILE = 'recipes.crfmodel'


def green(string):
    '''Returns green string
    '''
    return Back.GREEN + Fore.WHITE + string + Style.RESET_ALL


def red(string):
    '''Returns red string
    '''
    return Back.RED + Fore.WHITE + string + Style.RESET_ALL


def cyan(string):
    '''Returns cyan string
    '''
    return Back.CYAN + Fore.WHITE + string + Style.RESET_ALL


def white(string):
    '''Returns white string
    '''
    return Back.WHITE + Fore.BLACK + string + Style.RESET_ALL


def print_tokens(tokens):
    '''Prints colored TOKENS
    '''
    colored_tokens = []
    for tok, _, category in tokens:
        if category == 'NAME':
            colored_tokens.append(red(tok))
        elif category == 'QTY':
            colored_tokens.append(green(tok))
        elif category == 'UNIT':
            colored_tokens.append(cyan(tok))
        else:
            colored_tokens.append(white(tok))
    print(' '.join(colored_tokens))
    return ' '.join(colored_tokens)


def create_file(fname):
    '''Creates a file with an empty list if it does not exist
    '''
    if not os.path.exists(fname):
        with open(fname, 'w') as fil:
            json.dump([], fil)


def read_json(fname):
    '''Gets the content of json file
    '''
    create_file(fname)
    with open(fname) as fil:
        return json.load(fil)


def write_json(data, fname):
    '''Writes to json file
    '''
    with open(fname, 'w') as fil:
        return json.dump(data, fil, indent=4, sort_keys=True)
