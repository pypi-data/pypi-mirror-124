"""Second seat card play for defender."""

from typing import List, Union, Tuple
from termcolor import colored

from bridgeobjects import SUITS, Card, Denomination
from bfgsupport import Board, Trick
import bfgcardplay.source.global_variables as global_vars
from .player import Player
from .second_seat import SecondSeat

class SecondSeatDefender(SecondSeat):
    def __init__(self, player: Player):
        super().__init__(player)

    def selected_card(self) -> Card:
        """Return the card if the second seat."""
        player = self.player
        manager = global_vars.manager
        trick = player.board.tricks[-1]
        cards = player.cards_for_trick_suit(trick)

        # cover honour with honour
        # TODO see this web site http://www.rpbridge.net/4l00.htm
        cover_allowed = True
        if player.dummy_on_right:
            if player.dummy_holds_adjacent_card(trick.cards[0]):
                cover_allowed = False

        suit_cards = player.suit_cards[trick.suit.name]
        if (len(suit_cards) > 1 and
                suit_cards[0].value == suit_cards[1].value + 1 and
                suit_cards[1].value >= 9):
            return suit_cards[1]


        if cover_allowed and trick.cards[0].value >= 8: # nine or above
            if len(cards) >= 2:
                if cards[1].value >=9:
                    for card in cards[::-1]:
                        if card.value > trick.cards[0].value:
                            return card


        # If winner and last opportunity to play it
        if player.trump_suit and cards:
            opponents_trumps = len(player.opponents_unplayed_cards[player.trump_suit.name])
            safe_tricks = 13 - len(player.board.tricks) - opponents_trumps
            opponents_cards = player.opponents_unplayed_cards[trick.suit.name]
            if opponents_cards:
                opponents_top_card = player.opponents_unplayed_cards[trick.suit.name][0].value
                winners = 0
                for card in cards:
                    if card.value > opponents_top_card:
                        winners +=1
                    else:
                        break
                if safe_tricks <= winners:
                    return cards[0]
        # else:  # TODO add something for NT contracts
        #         for card in cards[::-1]:
        #             if card.value > trick.cards[0].value:
        #                 return card

        if cards:
            return cards[-1]

        return self._select_card_if_void(player, trick)
