from dataclasses import dataclass
from src.core.error_types import ErrorType
from src.core.result import Failure, InternalError, Result, Success

HAND_VALUES = (1, 3, 6, 9, 12)


@dataclass(frozen=True)
class RaiseResult:
    pending_value: int | None
    forfeited: bool | None
    winner_team: int | None = None



class Betting:
    def __init__(self, forfeit_on_raise: bool = False):
        self.value_index = 0
        self.pending_value_index: int | None = None
        self.pending: bool = False
        self.requester_team: int | None = None
        self.last_raising_team: int | None = None
        self.forfeit_on_raise: bool = forfeit_on_raise

    @property
    def has_pending_raise(self) -> bool:
        return self.pending

    def _initiate_raise(self, requester_team: int) -> Result[RaiseResult]:
        if self.last_raising_team == requester_team:
            return Failure(
                InternalError(
                    code=ErrorType.SAME_TEAM_RAISE,
                    message="You cannot raise twice.",
                )
            )
        if self.value_index >= len(HAND_VALUES) - 1:
            return Failure(
                InternalError(
                    code=ErrorType.OUT_OF_RAISING_INDEX,
                    message="You cannot raise more than 12 points.",
                )
            )
        next_index = self.value_index + 1
        self.pending = True
        self.pending_value_index = next_index
        self.requester_team = requester_team
        return Success(RaiseResult(HAND_VALUES[next_index], False))

    def _escalate_pending_raise(self, requester_team: int) -> Result[RaiseResult]:
        if self.requester_team == requester_team:
            return Failure(
                InternalError(
                    code=ErrorType.SAME_TEAM_RAISE,
                    message="You cannot raise twice.",
                )
            )
        if self.pending_value_index is None or self.pending_value_index >= len(HAND_VALUES) - 1:
            return Failure(
                InternalError(
                    code=ErrorType.OUT_OF_RAISING_INDEX,
                    message="You cannot raise more than 12 points.",
                )
            )
        self.value_index = self.pending_value_index
        self.pending_value_index += 1
        self.last_raising_team = self.requester_team
        self.requester_team = requester_team
        return Success(RaiseResult(HAND_VALUES[self.pending_value_index], False))

    def request_raise(self, requester_team: int) -> Result[RaiseResult]:
        invalid = _validate_team(requester_team)
        if invalid is not None:
            return invalid

        if self.forfeit_on_raise:
            return Success(RaiseResult(None, True, 1 - requester_team))

        if self.pending:
            return self._escalate_pending_raise(requester_team)

        return self._initiate_raise(requester_team)

    def accept_raise(self, responder_team: int) -> Result[int]:
        invalid = _validate_team(responder_team)
        if invalid is not None:
            return invalid

        if not self.pending or self.pending_value_index is None:
            return Failure(
                InternalError(
                    code=ErrorType.NO_PENDING_RAISE,
                    message="There is no pending raise to accept.",
                )
            )
        if responder_team == self.requester_team:
            return Failure(
                InternalError(
                    code=ErrorType.SAME_TEAM_RAISE,
                    message="You cannot accept your own raise.",
                )
            )
        self.value_index = self.pending_value_index
        self.pending_value_index = None
        self.last_raising_team = self.requester_team
        self.requester_team = None
        self.pending = False
        return Success(HAND_VALUES[self.value_index])

    def fold_raise(self, responder_team: int) -> Result[RaiseResult]:
        invalid = _validate_team(responder_team)
        if invalid is not None:
            return invalid

        if not self.pending:
            return Failure(
                InternalError(
                    code=ErrorType.NO_PENDING_RAISE,
                    message="There is no pending raise to fold.",
                )
            )
        if self.requester_team == responder_team:
            return Failure(
                InternalError(
                    code=ErrorType.SAME_TEAM_RAISE,
                    message="You cannot fold your own raise.",
                )
            )
        winner_team = self.requester_team
        self.pending = False
        self.pending_value_index = None
        self.requester_team = None
        return Success(RaiseResult(None, True, winner_team))

    @property
    def current_value(self) -> int:
        return HAND_VALUES[self.value_index]

    def to_dict(self) -> dict:
        return {
            "current_value": self.current_value,
            "pending": self.pending,
            "pending_value": (
                HAND_VALUES[self.pending_value_index]
                if self.pending_value_index is not None
                else None
            ),
            "requester_team": self.requester_team,
            "awaiting_response_from_team": (
                1 - self.requester_team
                if self.requester_team is not None
                else None
            ),
            "last_raising_team": self.last_raising_team,
        }




def _validate_team(team: int) -> Failure | None:
    if not isinstance(team, int) or isinstance(team, bool) or team not in (0, 1):
        return Failure(
            InternalError(
                code=ErrorType.INVALID_TEAM,
                message=f"Invalid team: {team!r}. Expected 0 or 1.",
            )
        )
    return None