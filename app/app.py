#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork
.. moduleauthor:: Julien Spronck
.. created:: April 2018
'''

# Import dependencies
import os
from datetime import timedelta
from functools import update_wrapper

from flask import Flask, request, abort, jsonify
from flask import make_response, current_app, render_template

import nltk
import pycrfsuite

__version__ = '1.0'


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    basestring = (str, bytes)
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)
PATH, _ = os.path.split(__file__)
MODEL_FILE = 'recipes.crfmodel'


def data2features(data):
    '''Retrieves features from data.
    '''
    all_features = []
    for row in data:
        openpar = False
        row_features = []
        for j, tokens in enumerate(row):
            token = tokens[0]
            tag = tokens[1]
            if token == '(':
                openpar = True
            elif token == ')':
                openpar = False
            features = [
                f'w[0]={token}',
                f'pos[0]={tag}',
            ]
            if j < len(row)-1:
                features.extend([
                    f'w[1]={row[j+1][0]}',
                    f'pos[1]={row[j+1][1]}',
                    f'w[0]|w[1]={token}|{row[j+1][0]}',
                    f'pos[0]|pos[1]={tag}|{row[j+1][1]}'
                ])
            if j < len(row)-2:
                features.extend([
                    f'w[2]={row[j+2][0]}',
                    f'pos[2]={row[j+2][1]}',
                    f'pos[1]|pos[2]={row[j+1][1]}|{row[j+2][1]}',
                    f'pos[0]pos[1]|pos[2]={tag}|{row[j+1][1]}|{row[j+2][1]}'
                ])
            if j == 0:
                features.append('__BOS__')
            if j == 1:
                features.append('__BOS1__')
            if j == len(row) - 2:
                features.append('__EOS1__')
            if j == len(row) - 1:
                features.append('__EOS__')
            if j > 0:
                features.extend([
                    f'w[-1]={row[j-1][0]}',
                    f'pos[-1]={row[j-1][1]}',
                    f'w[-1]|w[0]={row[j-1][0]}|{token}',
                    f'pos[-1]|pos[0]={row[j-1][1]}|{tag}'
                ])
                if j < len(row)-1:
                    features.extend([
                        f'pos[-1]|pos[0]|pos[1]='
                        f'{row[j-1][1]}|{tag}|{row[j+1][1]}'
                    ])
            if j > 1:
                features.extend([
                    f'w[-2]={row[j-2][0]}',
                    f'pos[-2]={row[j-2][1]}',
                    f'pos[-2]|pos[-1]={row[j-2][1]}|{row[j-1][1]}',
                    f'pos[-2]pos[-1]|pos[0]={row[j-2][1]}|{row[j-1][1]}|{tag}'
                ])
            features.append(f'length={len(row)}')
            features.append(f'openpar={openpar}')

            row_features.append(features)
        all_features.append(row_features)
    return all_features


def predict(xdata):
    '''Make a prediction based on features
    '''
    tagger = pycrfsuite.Tagger()
    tagger.open(os.path.join(PATH, MODEL_FILE))
    return tagger.tag(xdata)


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


# Main route
@app.route('/')
def index():
    '''Main flask route
    '''
    return render_template('index.html')


@app.route('/parse', methods=['GET', 'POST'])
@crossdomain('*')
def parseroute():
    '''Main flask route
    '''
    ing = request.values.get('q', None)
    if ing is None:
        return abort(400)

    tokens = parse(ing)
    return jsonify(tokens)


# # form submission route
# @app.route('/submit', methods=['POST'])
# def submit():
#     # Get data from form
#     name = request.form['name']
#     blah = request.form['blah']

#     # Redirect to home page
#     return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
