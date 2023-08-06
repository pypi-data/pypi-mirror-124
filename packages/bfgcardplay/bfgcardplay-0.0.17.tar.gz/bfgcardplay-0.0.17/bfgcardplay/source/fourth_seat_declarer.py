"""Fourth seat card play for declarer."""

from typing import List, Union, Tuple

from bridgeobjects import SUITS, Card, Denomination
from bfgsupport import Board, Trick
from .player import Player
from .fourth_seat import FourthSeat
import bfgcardplay.source.global_variables as global_vars

class FourthSeatDeclarer(FourthSeat):
    def __init__(self, player: Player):
        super().__init__(player)

    def selected_card(self) -> Card:
        """Return the card if the third seat."""
        player = self.player
        trick = player.board.tricks[-1]
        cards = player.cards_for_trick_suit(trick)
        manager = global_vars.manager
        if manager.suit_strategy == '':
            pass

        if cards:
            # play singleton
            if len(cards) == 1:
                return cards[0]

            # play low if partner is winning trick
            if self._second_player_winning_trick(cards, trick, player.trump_suit):
                return cards[-1]

            # win trick if possible
            winning_card = self._winning_card(trick)
            if winning_card:
                return winning_card

            # play smallest card
            if cards:
                return cards[-1]

        return self._select_card_if_void(player, trick)