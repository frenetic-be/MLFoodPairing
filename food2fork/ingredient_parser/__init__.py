'''
.. module:: food2fork.ingredient_parser
.. moduleauthor:: Julien Spronck
.. created:: April 2018

Ingredient parser
'''

import nltk

from food2fork.ingredient_parser.utils import print_tokens
from food2fork.ingredient_parser.crfmodel import (
    data2features,
    predict
)


def parse(phrase):
    '''Parse ingredient phrase to quantity, units and ingredients

    Args:
        phrase (str): ingredient phrase, e.g. `3 cups milk`

    Returns:
        tokens (list): list of tuples (token, tag, predicted label).
    '''
    tokens = nltk.word_tokenize(phrase.lower().strip())
    tagged_tokens = nltk.pos_tag(tokens)
    predictions = predict(data2features([tagged_tokens])[0])
    out = []
    for (token, tag), prediction in zip(tagged_tokens, predictions):
        out.append((token, tag, prediction))
    return out


def get_ingredient(tokens):
    '''Transforms a list of tagged predicted tokens to a ingredient string

    Args:
        tokens (list): list of tuples (token, tag, predicted label).

    Returns:
        str containing the parsed ingredient name
    '''
    return ' '.join(token for token, _, label in tokens if label == 'NAME')


def get_ingredient_from_phrase(phrase):
    '''Parse ingredient phrase to quantity, units and ingredients and returns
    ingredient string.

    Args:
        phrase (str): ingredient phrase, e.g. `3 cups milk`

    Returns:
        str containing the parsed ingredient name
    '''
    return get_ingredient(parse(phrase))
