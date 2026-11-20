"""Match-level orchestration boundary for hands and tricks.

The intended control flow is match -> hand -> trick: a match coordinates
hands, while each hand coordinates its tricks.
"""
from collections.abc import Callable
from src.cards.deck import Deck
from src.core.error_types import ErrorType
from src.core.result import Failure, InternalError, Result, Success
from src.game import hand, trick, betting

def _turn_table(players_order) -> list[str]:
    return players_order[1:]+ players_order[:1]

class Match:
    def __init__(self, players_order: list[str], deck_factory: Callable[[], Deck] = Deck):
        self.deck_factory = deck_factory
        self.players_order = list(players_order) # I'M TRUSTING THAT AN EVEN NUMBER OF PLAYERS ARE ON THE GAME!!
        self.team_by_player = {player: i % 2 for i, player in enumerate(players_order)}
        self.current_hand = hand.Hand(self.players_order, self.deck_factory())
        self.betting = betting.Betting()
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
        if self.betting.pending:
            return Failure(
                InternalError(
                    code=ErrorType.PENDING_RAISE,
                    message="Cannot play a card while a raise is pending.",
                )
            )
        hand_result = self.current_hand.play_card(player_id, card_index)
        if isinstance(hand_result, Failure):
            return hand_result
        if self.current_hand.finished:
            winning_team = None
            if self.current_hand.winner is not None:
                winner_player = self.current_hand.current_players_order[self.current_hand.winner]
                winning_team = self.team_by_player[winner_player]
            self._finish_hand(winning_team)
        return Success(hand_result.value)


    def _finish_hand(self, winning_team: int | None = None):
        points = self.betting.current_value
        if winning_team is not None:
            self.points[winning_team] += points
            if self.points[winning_team] >= 12:
                self.finished = True
                self.winner = winning_team
                return
        self.players_order = _turn_table(self.players_order)
        self.current_hand = hand.Hand(self.players_order, self.deck_factory())
        self.betting = betting.Betting()

    def request_raise(self, player_id: str) -> Result:
        if player_id not in self.team_by_player:
            return Failure(
                InternalError(
                    code=ErrorType.INVALID_PLAYER,
                    message=f"Player {player_id} is not on the game.",
                )
            )
        if self.finished:
            return Failure(
                InternalError(
                    code=ErrorType.MATCH_ALREADY_FINISHED,
                    message="Cannot request a raise in a finished match.",
                )
            )
        team = self.team_by_player[player_id]
        result = self.betting.request_raise(team)
        if isinstance(result, Success) and result.value.forfeited:
            self._finish_hand(result.value.winner_team)
        return result

    def accept_raise(self, player_id: str) -> Result:
        if player_id not in self.team_by_player:
            return Failure(
                InternalError(
                    code=ErrorType.INVALID_PLAYER,
                    message=f"Player {player_id} is not on the game.",
                )
            )
        if self.finished:
            return Failure(
                InternalError(
                    code=ErrorType.MATCH_ALREADY_FINISHED,
                    message="Cannot accept a raise in a finished match.",
                )
            )
        team = self.team_by_player[player_id]
        return self.betting.accept_raise(team)

    def fold_raise(self, player_id: str) -> Result:
        if player_id not in self.team_by_player:
            return Failure(
                InternalError(
                    code=ErrorType.INVALID_PLAYER,
                    message=f"Player {player_id} is not on the game.",
                )
            )
        if self.finished:
            return Failure(
                InternalError(
                    code=ErrorType.MATCH_ALREADY_FINISHED,
                    message="Cannot fold a raise in a finished match.",
                )
            )
        team = self.team_by_player[player_id]
        result = self.betting.fold_raise(team)
        if isinstance(result, Success):
            self._finish_hand(result.value.winner_team)
        return result

    def get_state(self, player_id: str, blind_hand: bool = False) -> Result[dict]:
        if player_id not in self.team_by_player:
            return Failure(
                InternalError(
                    code=ErrorType.INVALID_PLAYER,
                    message=f"Player {player_id} is not on the game.",
                )
            )

        return Success(
            {
                "points": list(self.points),
                "teams": dict(self.team_by_player),
                "finished": self.finished,
                "winner": self.winner,
                "betting": self.betting.to_dict(),
                "hand": self.current_hand.to_dict(player_id, blind_hand=blind_hand),
            }
        )