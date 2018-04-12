'''
This script was used to check and correct the tags in `token_pos_tagged.tsv`.
'''
import os

from food2fork.ingredient_parser.utils import (
    print_tokens, read_json, write_json
)

INPUT_FILE = 'token_pos_tagged2.tsv'
OUTPUT_FILE = 'token_pos_tagged_corr.tsv'
PROCESSED_TOKENS_FILE = 'processed_tokens.json'

PATH, _ = os.path.split(__file__)

PROCESSED = read_json(os.path.join(PATH, PROCESSED_TOKENS_FILE))


# STARTLINE = 55077
STARTLINE = 10540

with open(os.path.join(PATH, OUTPUT_FILE), 'a') as outfil:
    with open(os.path.join(PATH, INPUT_FILE)) as inpfil:
        j = 0
        PREVJ = STARTLINE
        TOKENS = []
        OPENPAR = False
        for line in inpfil:
            if j < STARTLINE:
                j += 1
                continue
            try:
                token, tag, cat = line.strip().split('\t')
                if token == '(':
                    OPENPAR = True
                elif token == ')':
                    OPENPAR = False
                if OPENPAR:
                    cat = 'COM'
                TOKENS.append([token, tag, cat])
            except ValueError:
                ptok = print_tokens(TOKENS)
                if ptok not in PROCESSED:
                    inp = input('')
                    if inp == 'q':
                        print(PREVJ)
                        break
                    if inp == 'c':
                        print('Correction mode:')

                        print_tokens(TOKENS)
                        print(' '.join(str(i)+(len(t[0])-1)*' '
                                       for i, t in enumerate(TOKENS)))

                        correction = input('Correction: ')
                        while correction != 'q' and correction != '':
                            item, cat = correction.split()
                            if ':' in item:
                                items = item.split(':')
                                if item[-1] == ':':
                                    item = slice(int(items[0]), None)
                                elif item[0] == ':':
                                    item = slice(None, int(items[0]))
                                else:
                                    item = slice(int(items[0]), int(items[1]))
                            else:
                                item = int(item)
                            newcat = ''
                            if cat == 'n':
                                newcat = 'NAME'
                            elif cat == 'c':
                                newcat = 'COM'
                            elif cat == 'u':
                                newcat = 'UNIT'
                            elif cat == 'y':
                                newcat = 'QTY'
                            if newcat:
                                if isinstance(item, int):
                                    TOKENS[item][2] = newcat
                                else:
                                    for token in TOKENS[item]:
                                        token[2] = newcat
                                print_tokens(TOKENS)
                            correction = input('Correction: ')
                    else:
                        PROCESSED.append(ptok)
                for token, tag, cat in TOKENS:
                    print(f'{token}\t{tag}\t{cat}', file=outfil)
                print(file=outfil)

                TOKENS = []
                OPENPAR = False
                PREVJ = j

            j += 1

write_json(PROCESSED, os.path.join(PATH, PROCESSED_TOKENS_FILE))
