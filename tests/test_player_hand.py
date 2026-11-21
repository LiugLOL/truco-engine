import pytest

from truco_engine.cards.card import Card
from truco_engine.cards.player_hand import PlayerHand
from truco_engine.cards.suits import Suits
from truco_engine.core.error_types import ErrorType
from truco_engine.core.result import Failure, Success


def test_add_card_appends_to_hand():
    hand = PlayerHand()
    card = Card(Suits.CLUBS, "4")

    hand.add_card(card)

    assert hand.cards == [card]


def test_play_card_removes_and_returns_selected_card():
    first = Card(Suits.CLUBS, "4")
    second = Card(Suits.HEARTS, "A")
    hand = PlayerHand([first, second])

    result = hand.play_card(1)

    assert isinstance(result, Success)
    assert result.value is second
    assert hand.cards == [first]


@pytest.mark.parametrize("index", [-1, 0, 3])
def test_play_card_rejects_invalid_index(index):
    hand = PlayerHand([
        Card(Suits.CLUBS, "4"),
        Card(Suits.DIAMONDS, "5"),
        Card(Suits.SPADES, "3"),
    ])

    if index == 0:
        hand.cards = []

    result = hand.play_card(index)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_CARD_INDEX
