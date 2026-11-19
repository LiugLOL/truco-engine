"""Match-level orchestration boundary for hands and tricks.

The intended control flow is match -> hand -> trick: a match coordinates
hands, while each hand coordinates its tricks.
"""
from collections.abc import Callable
from src.cards.deck import Deck
from src.core.error_types import ErrorType
from src.core.result import Failure, InternalError, Result, Success
from src.game import hand, trick

def _turn_table(players_order) -> list[str]:
    return players_order[1:]+ players_order[:1]

class Match:
    def __init__(self, players_order: list[str], deck_factory: Callable[[], Deck] = Deck):
        self.deck_factory = deck_factory
        self.players_order = list(players_order) # I'M TRUSTING THAT AN EVEN NUMBER OF PLAYERS ARE ON THE GAME!!
        self.team_by_player = {player: i % 2 for i, player in enumerate(players_order)}
        self.current_hand = hand.Hand(self.players_order, self.deck_factory())
        self.points:list[int] = [0,0]
        self.finished: bool = False
        self.winner: int | None = None

    def play_card(self, player_id: str, card_index: int) -> Result[trick.PlayResult]:
        if self.finished:
            return Failure(
                InternalError(
                    code=ErrorType.MATCH_ALREADY_FINISHED,
                    message="Cannot play a card in a finished match.",
                )
            )
        hand_result = self.current_hand.play_card(player_id, card_index)
        if isinstance(hand_result, Failure):
            return hand_result
        if self.current_hand.finished:
            if self.current_hand.winner is not None:
                winner_player = self.current_hand.current_players_order[self.current_hand.winner]
                winning_team = self.team_by_player[winner_player]
                self.points[winning_team] += 1
                if self.points[winning_team] >= 12:
                    self.finished = True
                    self.winner = winning_team
            if not self.finished:
                self.players_order = _turn_table(self.players_order)
                self.current_hand = hand.Hand(self.players_order, self.deck_factory())
        return Success(hand_result.value)



