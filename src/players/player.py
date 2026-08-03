from dataclasses import dataclass
from src.cards.player_hand import PlayerHand

@dataclass
class Player:
    id: int
    hand: PlayerHand