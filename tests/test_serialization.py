import json

from truco_engine.cards.card import Card
from truco_engine.cards.suits import Suits
from truco_engine.core.error_types import ErrorType
from truco_engine.core.result import Failure, Success
from truco_engine.game.match import Match
from tests.test_match import PLAYERS, team_zero_deck


def make_match() -> Match:
    return Match(PLAYERS, lambda: team_zero_deck())


def test_card_to_dict_uses_primitive_values():
    card = Card(Suits.HEARTS, "A")

    assert card.to_dict() == {"suit": "HEARTS", "number": "A"}


def test_match_state_is_json_serializable():
    match = make_match()

    result = match.get_state("p0")

    assert isinstance(result, Success)
    serialized = json.dumps(result.value)
    assert isinstance(json.loads(serialized), dict)


def test_private_hand_is_isolated_across_seats():
    match = make_match()

    for player_id in PLAYERS:
        result = match.get_state(player_id)
        assert isinstance(result, Success)

        hand = result.value["hand"]
        expected_cards = [
            card.to_dict() for card in match.current_hand.hands[player_id].cards
        ]
        assert hand["my_hand"] == expected_cards

        assert set(hand) == {
            "vira",
            "manilha",
            "current_turn",
            "table_cards",
            "trick_wins",
            "finished",
            "winner",
            "my_hand",
            "players",
        }
        assert hand["players"] == [
            {"player_id": pid, "cards_count": 3}
            for pid in match.current_hand.current_players_order
        ]
        for player in hand["players"]:
            assert set(player) == {"player_id", "cards_count"}


def test_blind_hand_hides_my_hand():
    match = make_match()

    result = match.get_state("p2", blind_hand=True)

    assert isinstance(result, Success)
    assert result.value["hand"]["my_hand"] == []


def test_betting_state_reflects_pending_raise():
    match = make_match()

    match.request_raise("p0")
    result = match.get_state("p0")

    assert isinstance(result, Success)
    betting = result.value["betting"]
    assert betting["current_value"] == 1
    assert betting["pending"] is True
    assert betting["pending_value"] == 3
    assert betting["requester_team"] == 0
    assert betting["awaiting_response_from_team"] == 1
    assert betting["last_raising_team"] is None


def test_unknown_player_returns_invalid_player():
    match = make_match()

    result = match.get_state("unknown")

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_PLAYER
