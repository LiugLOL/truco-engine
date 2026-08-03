from enum import Enum
class ErrorType(Enum):
    #Hand errors
    CARD_NOT_FOUND = "card_not_found"
    INVALID_CARD_INDEX = "invalid_card_index"

    #Trick errors
    INVALID_TRICK_RESULT = "invalid_trick_result"