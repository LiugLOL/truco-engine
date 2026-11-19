"""Hand lifecycle, trick rotation, and team winner resolution."""

from src.cards.deck import Deck
from src.cards.player_hand import PlayerHand
from src.game import trick
from src.core.error_types import ErrorType
from src.core.result import Failure, InternalError, Result


def _resolve_winner(trick_winners: list[int | None]) -> int | None:
    """Resolve the hand winner from completed trick team results.

    Args:
        trick_winners: Team indexes for each trick; ``None`` represents a tie.

    Returns:
        The winning team index when the hand is decided, otherwise ``None``.
    """
    if len(trick_winners) < 2:
        return None

    first, second = trick_winners[0], trick_winners[1]

    if len(trick_winners) == 2:
        #first tied, who wons the second wons the hand, if tied again keeps None
        if first is None:
            return second
        #first got a winner and second tied, who wons the first takes the point
        if second is None:
            return first
        #both won 1 trick, goes to third
        if first != second:
            return None
        #same team won 2 tricks
        return first

    # if it got here, len(trick_winners) == 3
    third = trick_winners[2]
    if third is not None:
        return third
    # third tied, the team who made first takes it, or 0 if everything tied
    return first


class Hand:
    """Manage four players, their cards, and the tricks in one hand."""

    def __init__(self, players_order: list[str], deck: Deck | None = None):
        """Deal cards and initialize the first trick.

        Args:
            players_order: Ordered player identifiers alternating by team.
            deck: Optional deck implementation used for dealing and the vira.
        """
        self.current_players_order = players_order
        self.deck = deck if deck is not None else Deck()
        self.hands: dict[str, PlayerHand] = {}
        for player_id in players_order:
            hand = PlayerHand()
            for _ in range(3):
                hand.add_card(self.deck.draw())
            self.hands[player_id] = hand

        self.turn_card = self.deck.draw()
        self.trick_winners: list[int | None] = []
        self.winner : int | None = None
        self.current_trick = trick.Trick(self.current_players_order, self.turn_card)
        self.finished: bool = False

    def play_card(self, player_id: str, card_index: int) -> Result[trick.PlayResult]:
        """Play one card and advance the hand state.

        Args:
            player_id: Player attempting to play.
            card_index: Zero-based index of the selected card.

        Returns:
            The play result, or a typed failure for invalid turn, card, or
            finished-hand requests.
        """
        if self.finished:
            return Failure(
                InternalError(
                    code=ErrorType.HAND_ALREADY_FINISHED,
                    message="Cannot play a card in a finished hand.",
                )
            )

        expected_player = self.current_trick.players_order[len(self.current_trick.plays)]
        if player_id != expected_player:
            return Failure(
                InternalError(
                    code=ErrorType.NOT_PLAYER_TURN,
                    message=f"Player {player_id} is not the current turn.",
                )
            )

        card_result = self.hands[player_id].play_card(card_index)
        if isinstance(card_result, Failure):
            return card_result


        play_result = self.current_trick.add_play(card_result.value)
        if isinstance(play_result, Failure):
            return play_result
        trick_result = play_result.value.trick_result
        if trick_result is not None:
            if trick_result.winner_index is None:
                winning_team = None
                next_order = self.current_trick.players_order
            else:
                winner_id = self.current_trick.players_order[trick_result.winner_index]
                winning_team = self.current_players_order.index(winner_id) % 2
                #Rotates the table to start from the winner of the trick
                start_idx = self.current_players_order.index(winner_id)
                next_order = self.current_players_order[start_idx:] + self.current_players_order[:start_idx]

            self.trick_winners.append(winning_team)
            self.winner = _resolve_winner(self.trick_winners)

            if self.winner is not None or len(self.trick_winners) == 3:
                self.finished = True
            else:
                self.current_trick = trick.Trick(next_order, self.turn_card)

        return play_result
