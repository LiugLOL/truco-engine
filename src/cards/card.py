"""Immutable playing-card value objects."""

from dataclasses import dataclass
from src.cards.suits import Suits


@dataclass(frozen=True)
class Card:
    """Represent one card by its suit and rank.

    Args:
        suit: Suit associated with the card.
        number: Rank label used by the Truco card order.
    """

    suit: Suits
    number: str
