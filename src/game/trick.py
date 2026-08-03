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
    winner_index: int | None

    @property
    def tied(self) -> bool:
        return self.winner_index is None


@dataclass(frozen=True)
class PlayResult:
    player_id: str
    card: Card
    trick_result: TrickResult | None = None


class Trick:
    def __init__(self, players_order: list[str], turn_card: Card):
        self.players_order = players_order
        self.plays: list[Card] = []
        self.manilha = self._get_manilha(turn_card)
        self.result: TrickResult | None = None

    @staticmethod
    def _get_manilha(turn_card: Card) -> str:
        index = CARD_ORDER.index(turn_card.number)
        return CARD_ORDER[(index + 1) % len(CARD_ORDER)]

    def _get_card_power(self, card: Card) -> int:
        base_power = CARD_ORDER.index(card.number)

        if card.number != self.manilha:
            return base_power

        return len(CARD_ORDER) + SUIT_POWER[card.suit]

    def _resolve(self) -> TrickResult:
        powers = [self._get_card_power(card) for card in self.plays]
        highest_power = max(powers)

        if powers.count(highest_power) > 1:
            return TrickResult(winner_index=None)

        return TrickResult(winner_index=powers.index(highest_power))

    def add_play(self, card: Card) -> Result[PlayResult]:
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
