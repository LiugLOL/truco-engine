"""Deck construction, shuffling, and card drawing."""

import random
from truco_engine.cards.card import Card
from truco_engine.cards.suits import Suits


class Deck:
    """Manage the complete Truco deck used to deal cards."""

    def __init__(self) -> None:
        """Create, populate, and shuffle a new deck."""
        self.cards: list[Card] = []
        self.create_deck()
        self.shuffle()


    def create_deck(self) -> None:
        """Populate the deck with every supported suit and rank combination."""
        self.cards.clear()
        suits: list[Suits] = [Suits.CLUBS, Suits.DIAMONDS, Suits.HEARTS, Suits.SPADES]
        numbers: list[str] = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
        for suit in suits:
            for number in numbers:
                self.cards.append(Card(suit, number))


    def shuffle(self) -> None:
        """Randomize the order of the cards currently in the deck."""
        random.shuffle(self.cards)


    def draw(self) -> Card:
        """Remove and return the next card from the top of the deck."""
        return self.cards.pop()