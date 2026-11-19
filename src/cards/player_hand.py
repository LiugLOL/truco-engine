"""Cards currently held by an individual player."""

from dataclasses import dataclass, field
from src.cards.card import Card
from src.core.error_types import ErrorType
from src.core.result import Failure, InternalError, Result, Success


@dataclass
class PlayerHand:
    """Store a player's cards and expose card-play validation."""

    cards: list[Card] = field(default_factory=list)

    def add_card(self, card: Card) -> None:
        """Add a card to the player's hand.

        Args:
            card: Card to append to the hand.
        """
        self.cards.append(card)

    def play_card(self, index: int) -> Result[Card]:
        """Remove and return a card selected by its zero-based index.

        Args:
            index: Position of the card to play.

        Returns:
            A success containing the removed card, or a failure when the index
            is outside the hand.
        """
        if index<0 or index>=len(self.cards):
            return Failure(
                InternalError(
                    code=ErrorType.INVALID_CARD_INDEX,
                    message=f"Invalid card index {index}"))
        return Success(self.cards.pop(index))
