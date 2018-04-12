'''
This script was used to create the `token_pos_tagged.tsv` file that contains
training data for the crf model. To create that file, we looped through 2000
recipes (`recipes.json`) and then looped through each ingredient sentence of
each recipe. Each sentence was analyzed and each word was tagged semi-manually
(known words were tagged automatically).
'''

import json
import os
import sys

from colorama import Fore, Back, Style
import nltk


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


INPUT_FILE = 'recipes.json'
OUTPUT_FILE = 'token_pos_tagged.tsv'
KNOWN_FEATURES_FILE = 'known_features.json'
PROCESSED_RECIPES_FILE = 'processed_recipes.json'


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


KNOWN_FEATURES = read_json(KNOWN_FEATURES_FILE)
UNITS = KNOWN_FEATURES['units']
INGREDIENTS = KNOWN_FEATURES['ingredients']
MISSPELLED_INGREDIENTS = KNOWN_FEATURES['misspelled_ingredients']
PROCESSES = KNOWN_FEATURES['processes']
SKIP = KNOWN_FEATURES['skip']
QUANTITIES = KNOWN_FEATURES['quantities']

PROCESSED_RECIPES = read_json(PROCESSED_RECIPES_FILE)


def save_lists():
    '''Saves lists to json files
    '''
    write_json(KNOWN_FEATURES, KNOWN_FEATURES_FILE)
    write_json(PROCESSED_RECIPES, PROCESSED_RECIPES_FILE)


with open(OUTPUT_FILE, 'a') as outfil:
    with open(INPUT_FILE) as inpfil:
        for line in inpfil:
            data = json.loads(line)
            if data['url'] in PROCESSED_RECIPES:
                continue
            for ingredient in data['ingredients']:
                print()
                print('-'*(len(ingredient)+4))
                print(f'- {ingredient} -')
                print('-'*(len(ingredient)+4))
                print()
                tokens = nltk.word_tokenize(ingredient.strip())
                tagged_tokens = nltk.pos_tag(tokens)

                colored_tokens = []
                for token, pos in tagged_tokens:
                    token = token.lower()
                    try:
                        cat = ''
                        if (token in INGREDIENTS or
                                token in MISSPELLED_INGREDIENTS):
                            cat = 'NAME'
                        elif token in UNITS:
                            cat = 'UNIT'
                        elif (pos == 'CD' or
                              token in ['a', 'an'] or
                              token in QUANTITIES):
                            cat = 'QTY'
                        elif token in PROCESSES:
                            cat = 'PROC'
                        elif token in SKIP:
                            cat = 'COM'
                        if not cat:
                            print(f'Category for {token.encode("utf8")} '
                                  f'({pos}): ')
                            print('`i` for ingredient')
                            print('`m` for misspelled ingredient')
                            print('`u` for unit')
                            print('`y` for quantity')
                            print('`p` for process')
                            print('`c` for comment')
                            print('`s` to skip')
                            print('`q` to quit')
                            print()

                            inp = input('')
                            if inp == 'i':
                                cat = 'NAME'
                                INGREDIENTS.append(token)
                            elif inp == 'm':
                                cat = 'NAME'
                                MISSPELLED_INGREDIENTS.append(token)
                            elif inp == 'u':
                                cat = 'UNIT'
                                UNITS.append(token)
                            elif inp == 'y':
                                cat = 'QTY'
                                QUANTITIES.append(token)
                            elif inp == 'p':
                                cat = 'PROC'
                                PROCESSES.append(token)
                            elif inp == 'c':
                                cat = 'COM'
                            elif inp == 's' or inp == '':
                                cat = 'COM'
                                SKIP.append(token)
                            elif inp == 'sr':
                                break
                            elif inp == 'q':
                                save_lists()
                                sys.exit()
                            # print(f'{token.encode("utf8")}\t{pos}\t{cat}')
                        if cat:
                            if cat == 'NAME':
                                colored_tokens.append(red(token))
                            elif cat == 'QTY':
                                colored_tokens.append(green(token))
                            elif cat == 'UNIT':
                                colored_tokens.append(cyan(token))
                            else:
                                colored_tokens.append(white(token))
                            print(f'{token}\t{pos}\t{cat}', file=outfil)

                    except Exception as error:
                        print(error)
                        print("Error writing token:", token)

                print(file=outfil)

                print()
                print(' '.join(colored_tokens))
                print()

            PROCESSED_RECIPES.append(data['url'])
        save_lists()
