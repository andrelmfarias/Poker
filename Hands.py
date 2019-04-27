import pandas as pd
import numpy as np
from numpy.random import shuffle
from collections import Counter

from Utils import *

<<<<<<< HEAD
head_converter = {'2': 2,
=======
#A simple dictionnary to give a int value to card figures
head_converter = {'1': 1,
                  '2': 2,
>>>>>>> e8c847bf64a77adc51673e5b51511cf81fe03054
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
    """check if a hand is a straight. If no straight, return None
    output : the value of the lowest card of the straight"""
    cards = list(simili_cards.keys())
    if 14 in cards:
        cards.append(1)
    straight = []
    cards_set = set(cards)
    for card in cards_set:
        if card <= 10:
            t_set = set(range(card, c+5))
            inter = t_set.intersection(cards_set)
            if len(inter) == 5:
                straight.append(card)
    if straight:
        return straight[-1]


def check_straight_flush(hand, simili_colors):
    """check if a hand is a straight flush. If no straight flush, return None
    output : the value of the lowest card of the straight flush"""
    for elmt in simili_colors.keys():
        if simili_colors[elmt] >= 5:
            l = [o[0] for o in hand if o[1] == elmt]
            l = [head_converter[ll] for ll in l]
            straight_flush = check_straight(l)
    if straight_flush:
        return straight_flush


def combi(hand):
    """Return a dictionnaire giving the combinaison of a given set of hand
    input : a list of cards [Cc, Cc, ... ]
    Card combinaison will be represented as a list that can be ordered from 
    the stronger to the smaller"""
    
    # Counter of heads in the head
    cards = Counter([head_converter[h[0]] for h in hand])
    # Counter of colors in the head
    simili_colors = Counter([h[1] for h in hand])
    # Unique heads in the hand of a player
    unique_cards = set(cards)
    
    #Initiation of all lists
    high = []
    pair = []
    thre = []
    squar = []
    flush = []
    DP = []
    full = []
    straight_flush = []
    straight = []
    
    #Check if the combination is a flush
    for k in simili_colors.keys():
        if simili_colors[k]>=5:
            card_flush = [head_converter[h[0]] for h in hand if h[1]==k]
            flush = sorted(card_flush,reverse=True)[:5]
            
    #Using the cards dict, we count the pairs, three of a kind, square
    for k in cards.keys():
        if cards[k]==1:
            high.append(k)
        if cards[k]==2:
            pair.append(k)
        if cards[k]==3:
            thre.append(k)
        if cards[k]==4:
            squar.append(k)

    #Sorting of lists from highest to lowest value
    pair = sorted(pair, reverse = True)
    high = sorted(high, reverse = True)
    thre = sorted(thre, reverse = True)
    
    #Checking of straight
    s = check_straight(cards)
    if s:
        straight.append(s)
        
    #Check DP and Full
    if len(pair)>=2:
        DP = pair[:2]
    if (len(pair) & len(thre)):
        full = [thre[0],pair[0]]
      
    #Check Straight_flush
    if (len(straight) & len(flush)):
        sf = check_straight_flush(hand,simili_colors)
        if sf:
            straight_flush.append(sf)
            

    #Making final hands:
    #For each combination, we take the best list of cards, including High Cards
    if len(pair):
        pair = [pair[0]] + sorted(list(unique_cards-set([pair[0]])), reverse= True)[:3]
        
    if len(DP):
        DP = DP[:2] + [sorted(list(unique_cards-set(DP[:2])), reverse = True)[0]]
        
    if len(thre):
        thre = [thre[0]] + sorted(list(unique_cards-set([thre[0]])), reverse = True)[:2]
        
    if len(squar):
        squar = [squar[0]] + [sorted(list(unique_cards-set([squar[0]])), reverse = True)[0]]
        
    if len(high)>=5:
        high = sorted(high,reverse=True)[:5]
        
    
    return {'high':high,
            '2':pair,
            'DP':DP,
            '3':thre,
            'straight': straight,
            'flush':flush,
            'full':full,
            '4':squar,
            'straight_flush':straight_flush}

def score(combi):
    """Given the dictionnary of combi for a player, return the best hand"""
    
    if len(combi['straight_flush']):
        return [8] +combi['straight_flush']
    
    if len(combi['4']):
        return [7] + combi['4']
    
    if len(combi['full']):
        return [6] + combi['full']
    
    if len(combi['flush']):
        return [5] + combi['flush']
    
    if len(combi['straight']):
        return [4] + combi['straight']
    
    if len(combi['3']):
        return [3] + combi['3']
    
    if len(combi['DP']):
        return [2] + combi['DP']
    
    if len(combi['2']):
        return [1] + combi['2']
    
    else:
        return [0] + combi['high']
    
def custom_order(x):
    '''order a list according to all its element'''
    i=0
    s=0
    for elmt in x:
        s+=100**(5-i)*elmt
        i+=1
    return s

def order_player(players):
    """return the players and their hand from best to lowest"""
    
    ladder = [[p.name,score(combi(p.hand))] for p in players]
    
    #In order to order, we use the curstomized function custom_order
    return sorted(ladder,key=lambda x : custom_order(x[1]), reverse = True)

