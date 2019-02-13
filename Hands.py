import pandas as pd
import numpy as np
from numpy.random import shuffle
from collections import Counter

from Utils import *

head_converter = {'1': 1,
                  '2': 2,
                  '3': 3,
                  '4': 4,
                  '5': 5,
                  '6': 6,
                  '7': 7,
                  '8': 8,
                  '9': 9,
                  'T': 10,
                  'J': 11,
                  'Q': 12,
                  'K': 13,
                  'A': 14}


def check_straight(simili_cards):
    cards = list(simili_cards.keys())
    if 14 in cards:
        cards.append(1)
    straight = []
    cards_set = set(cards)
    for c in cards_set:
        if c <= 10:
            t_set = set(range(c, c+5))
            inter = t_set.intersection(cards_set)
            if len(inter) == 5:
                straight.append(c)
    if straight:
        return straight[-1]


def check_straight_flush(hand, simili_colors):
    for elmt in simili_colors.keys():
        if simili_colors[elmt] >= 5:
            l = [o[0] for o in hand if o[1] == elmt]
            l = [head_converter[ll] for ll in l]
            straight_flush = check_straight(l)
    if straight_flush:
        return straight_flush


def combi(hand):
    """Return a dictionnaire giving the combinaison of a given set of hand"""
    # Counter for pairs, three of a kind, double pairs, four, and full
    cards = Counter([head_converter[h[0]] for h in hand])
    # Counter for flush and straight flush
    simili_colors = Counter([h[1] for h in hand])
    unique_cards = set(cards)
    high = []
    pair = []
    three = []
    four = []
    flush = []
    DP = []
    full = []
    straight_flush = []
    straight = []
    for k in simili_colors.keys():
        if simili_colors[k] >= 5:
            flush = [k]
    for k in cards.keys():
        if cards[k] == 1:
            high.append(k)
        if cards[k] == 2:
            pair.append(k)
        if cards[k] == 3:
            three.append(k)
        if cards[k] == 4:
            four.append(k)

    # reorganisation des listes
    pair = sorted(pair, reverse=True)
    high = sorted(high, reverse=True)
    three = sorted(three, reverse=True)

    straight = [check_straight(cards)]
    # Check DP and Full
    if len(pair) >= 2:
        DP = pair[:2]
    if (len(pair) & len(three)):
        full = [pair[0], three[0]]

    # Check Straight_flush
        if (len(straight) & len(flush)):
            straight_flush = [check_straight_flush(hand, simili_colors)]

    # Making final hands:
    if len(pair):
        pair = [pair[0]] + [sorted(list(unique_cards-set([pair[0]])), reverse=True)[:3]]

    if len(DP):
        DP = [DP[:2]] + [sorted(list(unique_cards-set(DP[:2])), reverse=True)[0]]

    if len(three):
        three = [three[0]] + [sorted(list(unique_cards-set([three[0]])), reverse=True)[:2]]
    if len()
    return {'high': high,
            '2': pair,
            'DP': DP,
            '3': three,
            'straight': straight,
            'flush': flush,
            'full': full,
            '4': four,
            'straight_flush': straight_flush}


def score(combi, hand):

    if len(combi['straight_flush']):
        best = combi['straight_flush'][-1]*(100) ^ 8
    if len(combi['4']):
        if len(combi['high']):
            best = combi['4']*(100) ^ 7+combi['high'][-1]
