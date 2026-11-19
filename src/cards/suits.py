"""Suit definitions used by cards and Truco ranking rules."""

from enum import Enum


class Suits(Enum):
    """Enumerate the four suits in the Truco deck."""

    CLUBS = "c"
    DIAMONDS = "d"
    HEARTS = "h"
    SPADES = "s"