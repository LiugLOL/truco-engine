"""Trick resolution, card power, and mobile-manilha rules."""

from dataclasses import dataclass
from src.cards.card import Card
from src.cards.suits import Suits
from src.core.error_types import ErrorType
from src.core.result import Failure, InternalError, Result, Success


CARD_ORDER = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]

SUIT_POWER = {
    Suits.CLUBS: 3,
    Suits.HEARTS: 2,
    Suits.SPADES: 1,
    Suits.DIAMONDS: 0,
}


@dataclass(frozen=True)
class TrickResult:
    """Describe the outcome of a completed trick.

    Args:
        winner_index: Position of the winning play, or ``None`` for a tie.
    """

    winner_index: int | None

    @property
    def tied(self) -> bool:
        """Return whether the trick ended without a unique winner."""
        return self.winner_index is None


@dataclass(frozen=True)
class PlayResult:
    """Describe a card play and any trick result it completed.

    Args:
        player_id: Identifier of the player assigned to the play position.
        card: Card played.
        trick_result: Completed trick result, or ``None`` before completion.
    """

    player_id: str
    card: Card
    trick_result: TrickResult | None = None


class Trick:
    """Collect plays and resolve their relative Truco strength."""

    def __init__(self, players_order: list[str], turn_card: Card):
        """Create an empty trick using the vira to determine the manilha.

        Args:
            players_order: Player sequence for this trick.
            turn_card: Vira card that defines the mobile manilha.
        """
        self.players_order = players_order
        self.plays: list[Card] = []
        self.manilha = self._get_manilha(turn_card)
        self.result: TrickResult | None = None

    @staticmethod
    def _get_manilha(turn_card: Card) -> str:
        """Return the rank immediately above the vira in Truco order.

        Args:
            turn_card: Vira card whose rank determines the manilha.

        Returns:
            The mobile-manilha rank, wrapping after ``3``.
        """
        index = CARD_ORDER.index(turn_card.number)
        return CARD_ORDER[(index + 1) % len(CARD_ORDER)]

    def _get_card_power(self, card: Card) -> int:
        """Calculate a card's comparison power for this trick.

        Args:
            card: Card whose power should be evaluated.

        Returns:
            Numeric power including suit strength for a manilha.
        """
        base_power = CARD_ORDER.index(card.number)

        if card.number != self.manilha:
            return base_power

        return len(CARD_ORDER) + SUIT_POWER[card.suit]

    def _resolve(self) -> TrickResult:
        """Resolve the current plays into a winner or tie."""
        powers = [self._get_card_power(card) for card in self.plays]
        highest_power = max(powers)

        if powers.count(highest_power) > 1:
            return TrickResult(winner_index=None)

        return TrickResult(winner_index=powers.index(highest_power))

    def add_play(self, card: Card) -> Result[PlayResult]:
        """Add one play and resolve the trick when all players have played.

        Args:
            card: Card submitted by the player at the current position.

        Returns:
            A success containing the play, or a failure if the trick is
            already complete.
        """
        if self.result is not None:
            return Failure(
                InternalError(
                    code=ErrorType.INVALID_TRICK_RESULT,
                    message="Cannot add a play to a finished trick.",
                )
            )

        player_id = self.players_order[len(self.plays)]
        self.plays.append(card)

        if len(self.plays) == len(self.players_order):
            self.result = self._resolve()

        return Success(
            PlayResult(
                player_id=player_id,
                card=card,
                trick_result=self.result,
            )
        )
