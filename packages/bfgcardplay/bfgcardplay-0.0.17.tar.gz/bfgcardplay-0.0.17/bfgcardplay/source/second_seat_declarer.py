"""Second seat card play for declarer."""

from bridgeobjects.source.file_operations import RANKS

from typing import List
from termcolor import colored

import inspect

from ..logger import log

from bridgeobjects import Card
from bfgsupport import Trick
from .player import Player
from .second_seat import SecondSeat
import bfgcardplay.source.global_variables as global_vars

MODULE_COLOUR = 'green'

class SecondSeatDeclarer(SecondSeat):
    def __init__(self, player: Player):
        super().__init__(player)

    def selected_card(self) -> Card:
        """Return the card if the second seat."""
        player = self.player
        manager = global_vars.manager
        trick = player.board.tricks[-1]
        cards = player.cards_for_trick_suit(trick)

        # Look for tenace about a threat card
        card = player.card_from_tenace()
        if card:
            log(inspect.stack(), f'{card}')
            return card

        card = self._card_from_suit_to_develop()
        if card:
            return card

        # When to duck - rule of 7
        duck_trick = False
        if not player.trump_suit:
            duck_trick = self._duck_trick(player, trick, cards)
            if not duck_trick:
                log(inspect.stack(), f'{cards[0]}')
                return cards[0]

        # Cover honour with honour
        # TODO see this web site http://www.rpbridge.net/4l00.htm
        if trick.cards[0].value >= 9 and not duck_trick:
            for card in player.suit_cards[trick.suit.name][::-1]:
                if card.value > trick.cards[0].value:
                    log(inspect.stack(), f'{card}')
                    return card

        suit_cards = player.suit_cards[trick.suit.name]
        if (len(suit_cards) > 1 and
                suit_cards[0].value == suit_cards[1].value + 1 and
                12 > suit_cards[1].value >= 9):
            log(inspect.stack(), f'{suit_cards[1]}')
            return suit_cards[1]

        if trick.cards[0].value >= 8: # nine or above
            if len(cards) >= 2:
                if cards[1].value >=9:
                    for card in cards[::-1]:
                        if card.value > trick.cards[0].value:
                            log(inspect.stack(), f'{card}')
                            return card

        # Play lowest card
        if cards:
            log(inspect.stack(), f'{suit_cards[-1]}')
            return cards[-1]

        return self._select_card_if_void(player, trick)

    def _duck_trick(self, player: Player, trick: Trick, cards: List[Card]) -> bool:
        """Return True if the player is to duck the trick."""
        opponents_unplayed_cards = player.opponents_unplayed_cards[trick.suit.name]
        if cards and opponents_unplayed_cards:
            partners_cards = player.partners_suit_cards[trick.suit.name]
            partner_can_win = False
            if partners_cards:
                if  partners_cards[0].value > trick.cards[0].value:
                    partner_can_win = True
            can_win_trick = (cards[0].value > opponents_unplayed_cards[0].value and
                            cards[0].value > trick.cards[0].value and
                            not partner_can_win)
            if self._rule_of_seven(player, trick) and can_win_trick:
                return False
        return True

    @staticmethod
    def _rule_of_seven(player: Player, trick: Trick) -> bool:
        """Return True if rule of seven applies."""
        our_cards = player.our_cards[trick.suit]
        duck_count = 7 - len(our_cards) - len(player.board.tricks)
        return duck_count < 0

    def _card_from_suit_to_develop(self):
        """Return card from a suit to develop."""
        player = self.player
        manager = global_vars.manager
        trick = player.board.tricks[-1]
        suit_to_develop = manager.suit_to_develop(player.seat)
        if suit_to_develop:
            for card in player.unplayed_cards[trick.suit.name][::-1]:
                if player.is_winner(card):
                    log(inspect.stack(), f'{card}')
                    return card
        return None