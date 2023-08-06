""" First seat card play for defender."""

from typing import List, Dict, Union
import random
from termcolor import colored

import inspect
from ..logger import log

from bridgeobjects import SUITS, Card, Suit, SEATS, CARD_NAMES
from bfgsupport import Board
from .player import Player
from .first_seat import FirstSeat
import bfgcardplay.source.global_variables as global_vars


class FirstSeatDefender(FirstSeat):
    def __init__(self, player: Player):
        super().__init__(player)

    def selected_card(self) -> Card:
        """Return the card if the third seat."""
        player = self.player
        if player.board.contract.is_nt:
            suit = self._select_suit_for_nt_contract()
        else:
            suit = self._select_suit_for_suit_contract()
        card = self._select_card_from_suit(suit)
        return card

    def _select_suit_for_suit_contract(self) -> Suit:
        """Return the trick lead suit for the defending a suit contract."""
        score_reasons = {}

        # Deprecate voidsrainman

        score_reasons['void'] = self._deprecate_suits()

        # Return partner's suit
        score_reasons['partner'] = self._partners_suit()

        # Lead from sequence
        score_reasons['sequences'] = self._sequences()

        # Lead to partner's void
        score_reasons['sequences'] = self._partners_voids()

        # Lead through tenaces not to tenaces
        score_reasons['tenaces'] = self._tenace_check()

        # Lead through or to strength
        score_reasons['weakness'] = self._lead_through_strength()

        # Avoid frozen suits
        score_reasons['frozen'] = self._frozen_suits()

        # Long suits
        score_reasons['long'] = self._long_suits()

        # Short suits
        score_reasons['short'] = self._short_suits()

        # Ruff and discard
        if self.player.trump_suit:
            score_reasons['ruff'] = self._ruff_and_discard()

        # Select best suit
        best_suit = self._best_suit(score_reasons)
        return best_suit

    def _select_suit_for_nt_contract(self) -> Suit:
        """Return the trick lead suit for the defending a suit contract."""
        score_reasons = {}
        player = self.player
        manager = global_vars.manager

        working_suit = manager.working_suit[player.seat]
        if working_suit and working_suit.name:
            if player.suit_cards[working_suit.name]:
                return working_suit

        # Deprecate voids
        score_reasons['void'] = self._deprecate_suits()

        # Return partner's suit
        score_reasons['partner'] = self._partners_suit()

        # Lead from sequence
        score_reasons['sequence'] = self._sequences()

        # Lead through tenaces not to tenaces
        score_reasons['tenaces'] = self._tenace_check()

        # Lead through or to strength
        score_reasons['weakness'] = self._lead_through_strength()

        # Avoid frozen suits
        score_reasons['frozen'] = self._frozen_suits()

        # Long suits
        score_reasons['long'] = self._long_suits()

        # Short suits
        score_reasons['short'] = self._short_suits()

        # Select best suit
        best_suit = self._best_suit(score_reasons)
        return best_suit

    def _select_card_from_suit(self, suit):
        """Return the card to lead from the given suit."""
        player = self.player
        cards = player.suit_cards[suit.name]

        # Winning card
        if cards:
            unplayed_cards = player.total_unplayed_cards[suit.name]
            if cards[0] == unplayed_cards[0]:
                log(inspect.stack(), f'{cards[0]}')
                return cards[0]

        # Top of touching honours
        for index, card in enumerate(cards[:-1]):
            if card.is_honour and card.value == cards[index+1].value + 1:
                log(inspect.stack(), f'{card}')
                return card

        # Top of doubleton
        if len(cards) == 2:
            log(inspect.stack(), f'{card}')
            return cards[0]

        # Return bottom card
        log(inspect.stack(), f'{cards[-1]}')
        return cards[-1]

    def _sequences(self) -> Suit:
        """Return the score for sequences."""
        suit_scores = {suit_name: 0 for suit_name in SUITS}
        player = self.player
        touching_honours = player.hand.touching_honours()
        best_sequence = None
        max_score = 0
        for suit_name in suit_scores:
            if touching_honours[suit_name]:
                suit_scores[suit_name] += self.TOUCHING_HONOURS
                suit_scores[suit_name] += len(touching_honours[suit_name])
                if suit_scores[suit_name] > max_score:
                    max_score = suit_scores[suit_name]
                    best_sequence = suit_name

        manager = global_vars.manager
        manager.working_suit[player.seat] = Suit(best_sequence)
        return [(suit_name, score) for suit_name, score in suit_scores.items()]

    def _partners_voids(self) -> Suit:
        """Return the score for sequences."""
        suit_scores = {suit_name: 0 for suit_name in SUITS}
        player = self.player
        manager = global_vars.manager
        partners_voids = manager.voids[player.seat]
        for suit, void in partners_voids.items():
            if void:
                suit_scores[suit.name] += self.PARTNERS_VOID
        return [(suit_name, score) for suit_name, score in suit_scores.items()]

