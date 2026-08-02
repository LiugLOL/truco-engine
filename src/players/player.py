from dataclasses import dataclass
from src.cards.player_hand import PlayerHand

@dataclass
class Player:
    def __init__(self):
        self.id = id
        self.hand = PlayerHand()