from dataclasses import dataclass
from src.cards.suits import Suits


@dataclass(frozen=True)
class Card:
    suit: Suits
    number: str
