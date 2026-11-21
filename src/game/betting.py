from dataclasses import dataclass
from src.core.error_types import ErrorType
from src.core.result import Failure, InternalError, Result, Success

HAND_VALUES = (1, 3, 6, 9, 12)


class Betting:
    def __init__(self, forfeit_on_raise: bool = False):
        self.value_index = 0
        self.pending_value_index: int | None = None
        self.pending: bool = False
        self.requester_team: int | None = None
        self.last_raising_team: int | None = None
        self.forfeit_on_raise: bool = forfeit_on_raise

    def request_raise(self, requester_team: int) -> Result:
        if self.forfeit_on_raise:
            return Success(RaiseResult(None, True, 1 - requester_team))

        if self.pending:
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
        self.pending = True
        self.pending_value_index = self.value_index + 1
        self.requester_team = requester_team
        return Success(RaiseResult(HAND_VALUES[self.pending_value_index], False))

    def accept_raise(self, responder_team: int) -> Result:
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

    def fold_raise(self, responder_team: int) -> Result:
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


@dataclass(frozen=True)
class RaiseResult:
    pending_value: int | None
    forfeited: bool | None
    winner_team: int | None = None