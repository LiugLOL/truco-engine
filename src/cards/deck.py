import random
from typing import List
from src.cards.card import Card
from src.cards.suits import Suits


class Deck:
    def __init__(self) -> None:
        self.cards: List[Card] = []
        self.create_deck()
        self.shuffle()


    def create_deck(self) -> None:
        suits: List[Suits] = [Suits.CLUBS, Suits.DIAMONDS, Suits.HEARTS, Suits.SPADES]
        numbers: List[str] = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
        for suit in suits:
            for number in numbers:
                self.cards.append(Card(suit, number))


    def shuffle(self):
        random.shuffle(self.cards)


    def draw(self):
        return self.cards.pop()