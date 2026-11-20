import pytest

from src.core.error_types import ErrorType
from src.core.result import Failure, RaiseResult, Success
from src.game.betting import Betting


def assert_failure(result, error_type: ErrorType) -> None:
    assert isinstance(result, Failure)
    assert result.error.code is error_type


def test_initial_state_has_one_point_value_and_no_pending_raise():
    betting = Betting()

    assert betting.current_value == 1
    assert betting.value_index == 0
    assert betting.pending_value_index is None
    assert betting.pending is False
    assert betting.requester_team is None
    assert betting.last_raising_team is None


def test_normal_raise_and_accept_progresses_through_all_hand_values():
    betting = Betting()

    for requester, responder, current_value, expected_value in (
        (0, 1, 1, 3),
        (1, 0, 3, 6),
        (0, 1, 6, 9),
        (1, 0, 9, 12),
    ):
        requested = betting.request_raise(requester)
        assert requested == Success(RaiseResult(expected_value, False))
        assert betting.pending is True
        assert betting.current_value == current_value

        accepted = betting.accept_raise(responder)
        assert accepted == Success(expected_value)
        assert betting.current_value == expected_value
        assert betting.pending is False
        assert betting.pending_value_index is None


def test_reraise_chain_keeps_confirmed_value_until_acceptance():
    betting = Betting()

    assert betting.request_raise(0) == Success(RaiseResult(3, False))
    assert betting.current_value == 1
    assert betting.pending_value_index == 1

    assert betting.request_raise(1) == Success(RaiseResult(6, False))
    assert betting.value_index == 1
    assert betting.current_value == 3
    assert betting.pending_value_index == 2
    assert betting.last_raising_team == 0

    assert betting.request_raise(0) == Success(RaiseResult(9, False))
    assert betting.value_index == 2
    assert betting.current_value == 6
    assert betting.pending_value_index == 3
    assert betting.last_raising_team == 1

    assert betting.request_raise(1) == Success(RaiseResult(12, False))
    assert betting.value_index == 3
    assert betting.current_value == 9
    assert betting.pending_value_index == 4
    assert betting.last_raising_team == 0

    assert betting.accept_raise(0) == Success(12)
    assert betting.value_index == 4
    assert betting.current_value == 12
    assert betting.pending is False
    assert betting.last_raising_team == 1


def test_same_team_cannot_raise_again_while_raise_is_pending():
    betting = Betting()

    assert isinstance(betting.request_raise(0), Success)

    assert_failure(betting.request_raise(0), ErrorType.SAME_TEAM_RAISE)


def test_team_that_won_last_accepted_raise_cannot_raise_next():
    betting = Betting()

    assert betting.request_raise(0) == Success(RaiseResult(3, False))
    assert betting.accept_raise(1) == Success(3)

    assert_failure(betting.request_raise(0), ErrorType.SAME_TEAM_RAISE)


def test_raise_past_twelve_fails_while_pending():
    betting = Betting()
    for requester in (0, 1, 0, 1):
        assert isinstance(betting.request_raise(requester), Success)

    assert betting.current_value == 9
    assert betting.pending_value_index == 4
    assert_failure(betting.request_raise(0), ErrorType.OUT_OF_RAISING_INDEX)


def test_raise_past_twelve_fails_after_twelve_is_accepted():
    betting = Betting()
    for requester in (0, 1, 0, 1):
        assert isinstance(betting.request_raise(requester), Success)
    assert betting.accept_raise(0) == Success(12)

    assert_failure(betting.request_raise(0), ErrorType.OUT_OF_RAISING_INDEX)


@pytest.mark.parametrize("operation", ["accept_raise", "fold_raise"])
def test_accept_or_fold_without_pending_raise_fails(operation):
    assert_failure(getattr(Betting(), operation)(1), ErrorType.NO_PENDING_RAISE)


@pytest.mark.parametrize("operation", ["accept_raise", "fold_raise"])
def test_requesting_team_cannot_accept_or_fold_own_raise(operation):
    betting = Betting()
    assert isinstance(betting.request_raise(0), Success)

    assert_failure(getattr(betting, operation)(0), ErrorType.SAME_TEAM_RAISE)


def test_fold_of_three_point_raise_preserves_one_point_value():
    betting = Betting()
    assert betting.request_raise(0) == Success(RaiseResult(3, False))

    result = betting.fold_raise(1)

    assert result == Success(RaiseResult(None, True, 0))
    assert betting.current_value == 1
    assert betting.pending is False
    assert betting.pending_value_index is None


def test_fold_of_six_point_reraise_preserves_three_point_value():
    betting = Betting()
    assert betting.request_raise(0) == Success(RaiseResult(3, False))
    assert betting.request_raise(1) == Success(RaiseResult(6, False))

    result = betting.fold_raise(0)

    assert result == Success(RaiseResult(None, True, 1))
    assert betting.current_value == 3
    assert betting.value_index == 1
    assert betting.pending is False
    assert betting.pending_value_index is None


def test_edge_case_raise_immediately_forfeits_to_other_team():
    betting = Betting(edge_case=True)

    result = betting.request_raise(1)

    assert result == Success(RaiseResult(None, True, 0))
    assert betting.current_value == 1
    assert betting.pending is False
