import pytest

from src.core.error_types import ErrorType
from src.core.result import Failure, Success
from src.game.match import Match
from tests.test_match import PLAYERS, play_entire_hand, team_zero_deck


def test_play_card_is_blocked_by_pending_raise_and_allowed_after_acceptance():
    match = Match(PLAYERS, lambda: team_zero_deck())

    assert isinstance(match.request_raise("p0"), Success)
    blocked = match.play_card("p0", 0)
    assert isinstance(blocked, Failure)
    assert blocked.error.code is ErrorType.PENDING_RAISE

    assert match.accept_raise("p1") == Success(3)
    assert isinstance(match.play_card("p0", 0), Success)


@pytest.mark.parametrize("raised_value", [3, 6, 9, 12])
def test_winning_hand_awards_confirmed_raise_value(raised_value):
    match = Match(PLAYERS, lambda: team_zero_deck())

    requesters = {
        3: ["p0"],
        6: ["p0", "p1"],
        9: ["p0", "p1", "p0"],
        12: ["p0", "p1", "p0", "p1"],
    }[raised_value]
    for player_id in requesters:
        assert isinstance(match.request_raise(player_id), Success)

    responder = "p1" if requesters[-1] == "p0" else "p0"
    assert match.accept_raise(responder) == Success(raised_value)
    play_entire_hand(match)

    assert match.points == [raised_value, 0]
    assert match.finished is (raised_value == 12)
    if not match.finished:
        assert match.betting.current_value == 1


def test_winning_raised_hand_finishes_match_at_twelve_points():
    match = Match(PLAYERS, lambda: team_zero_deck())
    match.points[0] = 9

    assert isinstance(match.request_raise("p0"), Success)
    assert match.accept_raise("p1") == Success(3)
    play_entire_hand(match)

    assert match.points == [12, 0]
    assert match.finished is True
    assert match.winner == 0


def test_folding_raise_scores_raising_team_rotates_hand_and_resets_betting():
    match = Match(PLAYERS, lambda: team_zero_deck())
    first_hand = match.current_hand

    assert isinstance(match.request_raise("p0"), Success)
    result = match.fold_raise("p1")

    assert isinstance(result, Success)
    assert result.value.forfeited is True
    assert result.value.winner_team == 0
    assert match.points == [1, 0]
    assert match.players_order == ["p1", "p2", "p3", "p0"]
    assert match.current_hand is not first_hand
    assert match.current_hand.current_players_order == match.players_order
    assert match.betting.current_value == 1
    assert match.betting.pending is False


@pytest.mark.parametrize("method_name", ["request_raise", "accept_raise", "fold_raise"])
def test_match_betting_methods_reject_invalid_player(method_name):
    match = Match(PLAYERS, lambda: team_zero_deck())

    result = getattr(match, method_name)("unknown")

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_PLAYER


@pytest.mark.parametrize("method_name", ["request_raise", "accept_raise", "fold_raise"])
def test_match_betting_methods_reject_finished_match(method_name):
    match = Match(PLAYERS, lambda: team_zero_deck())
    match.finished = True

    result = getattr(match, method_name)("p0")

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.MATCH_ALREADY_FINISHED
