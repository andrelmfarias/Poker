import pandas as pd
import numpy as np
from numpy.random import shuffle


class Player:
    # This class simulate a player

    def __init__(self, bankroll):
        # Initiate a player
        self.bankroll = bankroll
        self.handval = {}
        self.statue = True
        self.cards = []

    def give_card(self, card):
        # give initial cards
        self.cards.append(card)

    def bet(self, bet):
        # bet chips
        self.bankroll -= bet
        return bet

    def fold(self):
        # fold the hand
        self.statue = False

    def update(self, board):
        # update the hand given what cards are in the board
        self.hand = self.cards + board
        self.heads = [s[0] for s in self.hand]
        self.colors = [s[1] for s in self.hand]

    def win(self, pot):
        self.bankroll += pot


class Deck:
    # This class simulate a full deck of card

    def __init__(self):
        # initiate the deck with the 52 cards
        heads = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['s', 'c', 'd', 'h']
        self.deck = [h+c for h in heads for s in suits]

    def shuff(self):
        # shuffle the deck
        shuffle(self.deck)

    def pick_card(self):
        # remove the top card of the deck
        return self.deck.pop(0)


class Board:
    # Simulate a board and the chips on the board

    def __init__(self, button, players):
        # initiate the board
        self.pot = 0
        self.bet_sup = 0
        self.cards = []
        self.button = button
        self.players = players

    def give_card(self, card):
        self.cards.append(card)

    def get_bet(self, bet):
        self.pot += bet
        if bet > self.bet_sup:
            self.bet_sup == bet
