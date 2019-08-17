import numpy as np
import nltk
from collections import defaultdict
import random

MARKOV_ORDER = 6 # markov chain order

def gen_dicts(tagged):
    markov_dict = defaultdict(dict)
    tag_dict = defaultdict(dict)

    # fill markov dict
    tag_length = len(tagged)
    for i in range(0, (tag_length - MARKOV_ORDER)):
        for j in range(i+1, i+MARKOV_ORDER):
            try:
                markov_dict[tagged[i]][tagged[j]] += 1
            except KeyError:
                markov_dict[tagged[i]][tagged[j]] = 1

    # fill tag dict
    for i in range(0, (tag_length - MARKOV_ORDER)):
        for j in range(i+1, i+MARKOV_ORDER):
            try:
                tag_dict[tagged[i][1]][tagged[j][1]] += 1
            except KeyError:
                tag_dict[tagged[i][1]][tagged[j][1]] = 1

    return markov_dict, tag_dict


def gen_mnemonic(corpus_path, input_string):
    first_letters = gen_input(input_string)
    corpus = open(corpus_path, encoding='utf8').read()
    corpus = corpus.lower()

    tokens = nltk.WhitespaceTokenizer().tokenize(corpus)
    for i in tokens:
        i = i.lower()

    tagged = nltk.pos_tag([i for i in tokens if i], tagset='universal')
    markov_dict, tag_dict = gen_dicts(tagged)

    # initialize sequence
    init_wordpool = []
    for pair in markov_dict:
        if pair[0][0] == first_letters[0]:
            init_wordpool.append(pair)

    first_word = random.choice(init_wordpool)

    mnemonic = [first_word]
    # check if next beginning letter in sequence is part of markov sequence for
    # previous word
    for i in range(1, len(first_letters)):
        choices = []
        markov_chain = markov_dict.get(mnemonic[i-1])
        # sort markov_chain
        markov_chain = sorted(markov_chain, key=markov_chain.get)

        tag_chain = tag_dict.get(mnemonic[i-1][1])
        tag_chain = sorted(tag_chain, key=tag_chain.get)

        for pair in markov_chain:
            if pair[0][0] == first_letters[i]:
                choices.append(pair)

        for pair in markov_dict:
            # go through everything in tag_dict
            for k in range(0, MARKOV_ORDER-1):
                if pair[0][0] == first_letters[i] and pair[1] == tag_chain[k]:
                    choices.append(pair)

        random_flag = 0
        if not choices:
            random_flag += 1
            for pair in markov_dict:
                if pair[0][0] == first_letters[i]:
                    choices.append(pair)

        if random_flag == 0:
            mnemonic.append(choices[0])
        else:
            mnemonic.append(random.choice(choices))

    out = [i[0] for i in mnemonic]
    return " ".join(out)
