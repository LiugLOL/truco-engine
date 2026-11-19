"""Error categories returned by card, trick, and hand operations."""

from enum import Enum


class ErrorType(Enum):
    """Identify expected domain failures in a machine-readable form."""

    #Hand errors
    CARD_NOT_FOUND = "card_not_found"
    INVALID_CARD_INDEX = "invalid_card_index"

    #Trick errors
    INVALID_TRICK_RESULT = "invalid_trick_result"
    HAND_ALREADY_FINISHED = "hand_already_finished"

    #Hand errors
    NOT_PLAYER_TURN = "not_player_turn"
    INVALID_PLAY_INDEX = "invalid_play_index"
