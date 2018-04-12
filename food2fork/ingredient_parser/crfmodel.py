#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
.. module:: food2fork.ingredient_parser.cfrmodel
.. moduleauthor:: Julien Spronck
.. created:: March 2018
'''

import os

from sklearn.model_selection import train_test_split
import pycrfsuite
from food2fork.ingredient_parser.utils import MODEL_FILE

PATH, _ = os.path.split(__file__)


def get_data():
    '''Transforms data file into list of list of tuples.
    '''
    fpath = os.path.join(PATH, 'token_pos_tagged_corr.tsv')
    with open(fpath) as inpfil:
        tokens = []
        data = []
        for line in inpfil:
            try:
                token, tag, cat = line.strip().split('\t')
                tokens.append((token, tag, cat))
            except ValueError:
                if tokens:
                    data.append(tokens)
                tokens = []
        return data


def data2labels(data):
    '''Retrieves labels from data
    '''
    return [[label for _, _, label in d] for d in data]


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


def train_model():
    '''Trains the CRF Model
    '''
    data = get_data()
    labels = data2labels(data)
    features = data2features(data)

    x_train, x_test, y_train, y_test = train_test_split(features, labels)

    trainer = pycrfsuite.Trainer(verbose=False)

    for xseq, yseq in zip(x_train, y_train):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 1.0,   # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 50,  # stop earlier

        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })

    trainer.train(os.path.join(PATH, MODEL_FILE))

    return x_train, x_test, y_train, y_test


def evaluate(xdata, ydata):
    '''Evaluate model accuracy
    '''
    from collections import defaultdict
    tagger = pycrfsuite.Tagger()
    tagger.open(os.path.join(PATH, MODEL_FILE))
    matches = defaultdict(int)
    model = defaultdict(int)
    ref = defaultdict(int)
    for xxx, yyy in zip(xdata, ydata):
        prediction = tagger.tag(xxx)
        correct = yyy
        for predtag, cortag in zip(prediction, correct):
            if predtag == cortag:
                matches[cortag] += 1
            model[predtag] += 1
            ref[cortag] += 1

    print('Performance by label (#match, #model, #ref) '
          '(precision, recall, F1):')
    for tag in ['QTY', 'UNIT', 'NAME', 'COM']:
        precision = matches[tag]/model[tag]
        recall = matches[tag]/ref[tag]
        f1score = 2 * precision * recall / (precision + recall)
        print(f'    {tag}: ({matches[tag]}, {model[tag]}, {ref[tag]})'
              f' ({precision:.4}, {recall:.4}, {f1score:.4})')


def predict(xdata):
    '''Make a prediction based on features
    '''
    tagger = pycrfsuite.Tagger()
    tagger.open(os.path.join(PATH, MODEL_FILE))
    return tagger.tag(xdata)
