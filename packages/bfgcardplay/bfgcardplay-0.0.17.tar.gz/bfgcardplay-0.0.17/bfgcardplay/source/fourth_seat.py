"""Fourth seat card play."""

from typing import List, Union, Tuple

import inspect
from ..logger import log

from bridgeobjects import SUITS, Card, Denomination, Suit
from bfgsupport import Board, Trick
from .player import Player

class FourthSeat():
    def __init__(self, player: Player):
        self.player = player

    def _winning_card(self, trick: Trick) -> Union[Card, None]:
        """Return the card if can win trick."""
        player = self.player
        cards = self.player.cards_for_trick_suit(trick)

        (value_0, value_1, value_2) = self._trick_card_values(trick, player.trump_suit)
        if cards:
            for card in cards[::-1]:
                card_value = card.value
                if card.suit == player.trump_suit:
                    card_value += 13
                if card_value > value_0 and card_value > value_2:
                    return card

        # No cards in trick suit, look for trump winner
        elif player.trump_cards:
            for card in player.trump_cards[::-1]:
                if card.value + 13 > value_2:
                    return card
        return None

    def _second_player_winning_trick(self, cards: List[Card], trick: Trick, trumps: Denomination) -> bool:
        """Return True if the second player is winning the trick."""
        (value_0, value_1, value_2) = self._trick_card_values(trick, trumps)
        if value_1 > value_0 and value_1 > value_2:
            return True
        return False

    @staticmethod
    def _trick_card_values(trick: Trick, trumps: Denomination) -> Tuple[int, int, int]:
        """Return a tuple of card values."""
        value_0 = trick.cards[0].value
        if trick.cards[1].suit == trick.cards[0].suit:
            value_1 = trick.cards[1].value
        else:
            value_1 = 0
        if trick.cards[2].suit == trick.cards[0].suit:
            value_2 = trick.cards[2].value
        else:
            value_2 = 0
        if trumps:
            if trick.cards[0].suit == trumps:
                value_0 += 13
            if trick.cards[1].suit == trumps:
                value_1 = trick.cards[1].value + 13
            if trick.cards[2].suit == trumps:
                value_2 = trick.cards[2].value + 13
        return (value_0, value_1, value_2)

    def _select_card_if_void(self, player: Player, trick: Trick) -> Card:
        """Return card if cannot follow suit."""
        player.record_void(trick.suit)
        # Trump if appropriate
        (value_0, value_1, value_2) = self._trick_card_values(trick, player.trump_suit)
        if player.trump_suit:
            if player.trump_cards:
                if value_0 > value_1 or value_2 > value_1:
                    for card in player.trump_cards[::-1]:
                        if card.value + 13 > value_0 and card.value + 13 > value_2:
                            log(inspect.stack(), f'{card}')
                            return card

        suit = self._best_suit(player)
        suit_cards = player.suit_cards[suit.name]
        for card in suit_cards:
            if not card.is_honour:
                log(inspect.stack(), f'{card}')
                return card

        retain_suit = {suit_name: False for suit_name in SUITS}
        if player.is_defender:
            for suit_name in SUITS:
                cards = player.unplayed_cards[suit_name]
                if cards:
                    if len(cards) == 1 and player.is_winner(card):
                        retain_suit[suit_name] = True

        other_suit = player.other_suit_for_signals(suit)
        other_suit_cards = player.suit_cards[other_suit]
        if other_suit_cards and not retain_suit[other_suit]:
            log(inspect.stack(), f'{other_suit_cards[-1]}')
            return other_suit_cards[-1]

        for suit_name in SUITS:
            if suit_name != suit.name and suit_name != other_suit:
                final_suit_cards = player.suit_cards[suit_name]
                if final_suit_cards:
                    log(inspect.stack(), f'{final_suit_cards[-1]}')
                    return final_suit_cards[-1]

        cards = player.suit_cards[suit.name]
        if len(cards) == 1:
            log(inspect.stack(), f'{cards[0]}')
            return cards[0]

        for index, card in enumerate(cards[:-1]):
            if card.value > cards[index+1].value + 1:
                log(inspect.stack(), f'{card}')
                return card

        log(inspect.stack(), f'{cards[-1]}')
        return cards[-1]

    def _best_suit(self, player: Player) -> Suit:
        """Select suit for signal."""
        # TODO handle no points and equal suits
        cards = player.hand_cards.list
        suit_points = player.get_suit_strength(cards)
        max_points = 0
        best_suit = None
        for suit in SUITS:
            hcp = suit_points[suit]
            if hcp > max_points:
                max_points = hcp
                best_suit = suit
        if not best_suit:
            return player.longest_suit
        return Suit(best_suit)
