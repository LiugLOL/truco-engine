"""Error categories returned by card, trick, and hand operations."""

from enum import Enum


class ErrorType(Enum):
    """Identify expected domain failures in a machine-readable form."""

    #Card errors
    INVALID_SUIT = "invalid_suit"
    INVALID_NUMBER = "invalid_number"

    #Hand errors
    INVALID_CARD_INDEX = "invalid_card_index"

    #Trick errors
    INVALID_TRICK_RESULT = "invalid_trick_result"
    HAND_ALREADY_FINISHED = "hand_already_finished"

    #Hand errors
    NOT_PLAYER_TURN = "not_player_turn"

    #Match errors
    MATCH_ALREADY_FINISHED = "match_already_finished"
    INVALID_PLAYER = "invalid_player"

    #Betting errors
    INVALID_TEAM = "invalid_team"
    SAME_TEAM_RAISE = "same_team_raise"
    OUT_OF_RAISING_INDEX = "out_of_raising_index"
    NO_PENDING_RAISE = "no_pending_raise"
    PENDING_RAISE = "pending_raise"

