"""Immutable playing-card value objects."""

from dataclasses import dataclass
from truco_engine.cards.suits import Suits

VALID_NUMBERS: tuple[str, ...] = ("4", "5", "6", "7", "Q", "J", "K", "A", "2", "3")


@dataclass(frozen=True)
class Card:
    """Represent one card by its suit and rank.

    Args:
        suit: Suit associated with the card.
        number: Rank label used by the Truco card order.
    """

    suit: Suits
    number: str

    def __post_init__(self) -> None:
        if not isinstance(self.suit, Suits):
            raise ValueError(f"Invalid card suit: {self.suit!r}.")
        if self.number not in VALID_NUMBERS:
            raise ValueError(f"Invalid card number: {self.number!r}.")

    def to_dict(self) -> dict:
        """Convert this card to JSON-ready primitive values."""
        return {
            "suit": self.suit.name,
            "number": self.number,
        }