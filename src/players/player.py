"""Player identity and card ownership model."""

from dataclasses import dataclass
from src.cards.player_hand import PlayerHand


@dataclass
class Player:
    """Associate a player identifier with their current hand.

    Args:
        id: Unique player identifier.
        hand: Cards currently held by the player.
    """

    id: int
    hand: PlayerHand