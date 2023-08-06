"""Fourth seat card play for defender."""

from typing import List, Union, Tuple

import inspect
from ..logger import log

from bridgeobjects import SUITS, Card, Denomination
from bfgsupport import Board, Trick
import bfgcardplay.source.global_variables as global_vars
from .player import Player
from .fourth_seat import FourthSeat

class FourthSeatDefender(FourthSeat):
    def __init__(self, player: Player):
        super().__init__(player)

    def selected_card(self) -> Card:
        """Return the card if the third seat."""
        player = self.player
        trick = player.board.tricks[-1]
        cards = player.cards_for_trick_suit(trick)

        if cards:
            # play singleton
            if len(cards) == 1:
                log(inspect.stack(), f'{cards[0]}')
                return cards[0]

            # play low if partner is winning trick
            if self._second_player_winning_trick(cards, trick, player.trump_suit):
                log(inspect.stack(), f'{cards[-1]}')
                return cards[-1]

            # win trick if possible
            winning_card = self._winning_card(trick)
            if winning_card:
                log(inspect.stack(), f'{winning_card}')
                return winning_card

            # play smallest card
            if cards:
                log(inspect.stack(), f'{cards[-1]}')
                return cards[-1]

        return self._select_card_if_void(player, trick)