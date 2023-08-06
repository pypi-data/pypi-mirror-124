"""The manager supervises play and holds persistant data. It is created in global.py."""
from typing import List, Dict, Union, Tuple
from termcolor import colored

from bridgeobjects import SEATS, SUITS, Card, Hand, Suit, RANKS
from bfgsupport import Board

DECLARER_STRATEGY = {
    0: 'Draw trumps and establish long suit',
}

ranks = [rank for rank in RANKS]
ranks.reverse()
RANKS = ranks[:-1]

class Manager():
    def __init__(self):
        self.initialise()

    def initialise(self):
        """Initialise variables at start of board."""
        # print('manager initialised')
        self._board = None
        self.threats = None
        self.winning_suit = None
        self.long_player = None
        self.draw_trumps = False
        self.working_suit = {seat: None for seat in SEATS}
        self._suit_to_develop = {seat: None for seat in SEATS}
        self._suit_strategy = {seat: {suit: '' for suit in SUITS} for seat in SEATS}
        self.card_to_play = {seat: [] for seat in SEATS}
        self.voids = {seat: {suit_name: False for suit_name in SUITS} for seat in SEATS}
        self.win_trick = {seat: False for seat in SEATS}
        self.signal_card = {seat: None for seat in SEATS}

    def __repr__(self):
        return f'Manager {self.suit_to_develop("E")} {self.suit_strategy("E")}'

    @property
    def board(self):
        """Return the current Board."""
        return self._board

    @board.setter
    def board(self, value):
        """Set the value of the current board"""
        self._board = value

    def suit_to_develop(self, seat: str) -> Suit:
        """Return the suit to develop for a seat."""
        return self._suit_to_develop[seat]

    def set_suit_to_develop(self, seat: str, suit: Suit):
        """Set the suit to develop for a seat."""
        partners_seat = self._partners_seat(seat)
        self._suit_to_develop[seat] = suit
        self._suit_to_develop[partners_seat] = suit

    def suit_strategy(self, seat: str) -> str:
        """Return the suit to develop for a seat."""
        return self._suit_strategy[seat]

    def set_suit_strategy(self, seat: str, suit: str, strategy: str):
        """Set the suit to develop for a seat."""
        partners_seat = self._partners_seat(seat)
        self._suit_strategy[seat][suit] = strategy
        self._suit_strategy[partners_seat][suit]  = strategy

    @staticmethod
    def _partners_seat(seat: str) -> str:
        """Return partners's seat name"""
        seat_index = SEATS.index(seat)
        partners_index = (seat_index + 2) % 4
        partners_seat = SEATS[partners_index]
        return partners_seat


    # def set_declarer_strategy(self):
    #     """Set the declarers initial strategy."""
    #     board = self.board
    #     declarer = self.board.contract.declarer
    #     declarer_index = SEATS.index(declarer)
    #     dummy_index = (declarer_index + 2) % 4
    #     dummy = SEATS[dummy_index]
    #     declarers_hand = board.hands[declarer]
    #     dummys_hand = board.hands[dummy]
    #     if board.contract.is_nt:
    #         pass
    #     else:
    #         trump_suit = board.contract.denomination.name
    #         (long_hand, short_hand) = Manager.get_long_hand(declarers_hand, dummys_hand, trump_suit)
    #         threats = self._get_declarers_threats(long_hand, short_hand, trump_suit)
    #         shortages_in_short_hand = self._get_shortages_in_short_hand(long_hand, short_hand, trump_suit)
    #         trumps_remaining_after_drawing = 0
    #         # for suit, cards in threats.items():

    #         # print(f'{shortages_in_short_hand=}')

    # @staticmethod
    # def _get_shortages_in_short_hand(long_hand: Hand, short_hand: Hand, trump_suit: Suit) -> Dict[str, Card]:
    #     """Return a dict of cards by suit that represent a shortage in the short hand."""
    #     shortages = {suit: 0 for suit in SUITS}
    #     for suit in SUITS:
    #         if not suit == trump_suit:
    #             long_hand_cards = long_hand.cards_by_suit[suit]
    #             short_hand_cards = short_hand.cards_by_suit[suit]
    #             if len(long_hand_cards) > len(short_hand_cards):
    #                 shortages[suit] = len(long_hand_cards)-len(short_hand_cards)
    #     return shortages

    # @staticmethod
    # def get_long_hand(declarers_hand: Hand, dummys_hand: Hand, trump_suit: Suit) -> Tuple[Hand, Hand]:
    #     """Return a tuple of long_hand and sort hand."""
    #     declarers_trumps = declarers_hand.cards_by_suit[trump_suit]
    #     dummys_trumps = dummys_hand.cards_by_suit[trump_suit]
    #     if len(dummys_trumps) > len(declarers_trumps):
    #         long_hand = dummys_hand
    #         short_hand = declarers_hand
    #     else:
    #         long_hand = declarers_hand
    #         short_hand = dummys_hand
    #     return(long_hand, short_hand)

    # def unplayed_cards(self) -> Dict[str, Card]:
    #     """Return a dict of suits with a list of unplayed cards in descending order."""
    #     unplayed = {suit: [] for suit in SUITS}
    #     for seat in SEATS:
    #         for card in self.board.hands[seat]:
    #             unplayed[card.suit.name].append(card)

    #     for suit in SUITS:
    #         sorted_cards = []
    #         for rank in RANKS:
    #             if Card(rank, suit) in unplayed[suit]:
    #                 sorted_cards.append(card)
    #         unplayed[suit] = [card for card in sorted_cards]
        return unplayed