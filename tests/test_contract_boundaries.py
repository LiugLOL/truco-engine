import copy
from dataclasses import FrozenInstanceError

import pytest

from truco_engine.cards.card import Card
from truco_engine.cards.deck import Deck
from truco_engine.cards.player_hand import PlayerHand
from truco_engine.cards.suits import Suits
from truco_engine.core.error_types import ErrorType
from truco_engine.core.result import Failure, Success
from truco_engine.game.betting import Betting
from truco_engine.game.hand import Hand, _resolve_winner
from truco_engine.game.match import Match
from truco_engine.game.trick import Trick, TrickResult
from tests.test_match import PLAYERS, team_zero_deck


def make_hand() -> Hand:
    deck = Deck()
    deck.cards = [
        Card(Suits.CLUBS, "6"),
        Card(Suits.CLUBS, "7"),
        Card(Suits.CLUBS, "A"),
        Card(Suits.DIAMONDS, "6"),
        Card(Suits.DIAMONDS, "7"),
        Card(Suits.DIAMONDS, "A"),
        Card(Suits.SPADES, "4"),
    ]
    return Hand(["p0", "p1"], deck)


def oracle(values: list[int | None]) -> int | None:
    if len(values) < 2:
        return None
    first, second = values[0], values[1]
    if len(values) == 2:
        if first is None:
            return second
        if second is None:
            return first
        if first != second:
            return None
        return first

    third = values[2]
    if first is None and second is None and third is None:
        return None
    win_counts = {
        team: sum(winner == team for winner in values)
        for team in (0, 1)
    }
    for team, count in win_counts.items():
        if count >= 2:
            return team
    if first is None:
        return second if second is not None else third
    if second is None:
        return first
    if third is None:
        return first
    return third


@pytest.mark.parametrize(
    "trick_winners",
    [(a, b, c) for a in (0, 1, None) for b in (0, 1, None) for c in (0, 1, None)],
)
def test_resolve_winner_all_cartesian_combinations(trick_winners):
    assert _resolve_winner(list(trick_winners)) == oracle(list(trick_winners))


@pytest.mark.parametrize(
    ("trick_winners", "expected"),
    [
        ([0], None),
        ([1], None),
        ([None], None),
        ([0, 1], None),
        ([1, 0], None),
        ([None, None], None),
        ([0, 0], 0),
        ([1, 1], 1),
        ([None, 0], 0),
        ([0, None], 0),
    ],
)
def test_resolve_winner_intermediate_states(trick_winners, expected):
    assert _resolve_winner(trick_winners) == expected


@pytest.mark.parametrize("suit", ["CLUBS", None, 0, True, object()])
def test_card_rejects_invalid_suit_types(suit):
    with pytest.raises(ValueError):
        Card(suit, "4")


@pytest.mark.parametrize(
    "rank",
    ["10", "8", "9", "1", "", None, 4, "a", "q", "j", "k"],
)
def test_card_rejects_invalid_ranks(rank):
    with pytest.raises(ValueError):
        Card(Suits.CLUBS, rank)


def test_card_is_immutable():
    card = Card(Suits.CLUBS, "4")
    with pytest.raises(FrozenInstanceError):
        card.number = "5"


@pytest.mark.parametrize("invalid_card", [None, "4c", 0, True])
def test_trick_rejects_non_card_inputs_without_mutation(invalid_card):
    turn_card = Card(Suits.CLUBS, "4")
    trick = Trick(["p0", "p1"], turn_card)
    before = list(trick.plays)

    result = trick.add_play(invalid_card)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_CARD
    assert trick.plays == before


@pytest.mark.parametrize("players", [[], [ "p0" ], [ "p0", "p1", "p2" ]])
def test_hand_rejects_empty_or_odd_player_lists(players):
    with pytest.raises(ValueError):
        Hand(players)


def test_hand_rejects_more_than_twelve_players():
    with pytest.raises(ValueError):
        Hand([f"p{i}" for i in range(14)])


def test_hand_rejects_duplicate_player_ids():
    with pytest.raises(ValueError):
        Hand(["p0", "p0"])


@pytest.mark.parametrize("team", [-1, 2, True, False, "0", None])
def test_hand_rejects_invalid_team_values(team):
    with pytest.raises(ValueError):
        Hand(["p0", "p1"], team_by_player={"p0": team, "p1": 1})


@pytest.mark.parametrize(
    "team_by_player",
    [
        {"p0": 0},
        {"p0": 0, "p1": 1, "p2": 0},
        {},
        {"p0": 0, "ghost": 1},
    ],
)
def test_hand_rejects_team_mapping_with_missing_or_extra_keys(team_by_player):
    with pytest.raises(ValueError):
        Hand(["p0", "p1"], team_by_player=team_by_player)


@pytest.mark.parametrize(
    "team_by_player",
    [
        {"p0": 0, "p1": 0},
        {"p0": 1, "p1": 1},
    ],
)
def test_hand_rejects_team_mapping_without_both_teams(team_by_player):
    with pytest.raises(
        ValueError,
        match="team_by_player must include both team 0 and team 1",
    ):
        Hand(["p0", "p1"], team_by_player=team_by_player)


def test_hand_rejects_insufficient_deck_size():
    deck = Deck()
    deck.cards = deck.cards[:6]
    with pytest.raises(ValueError):
        Hand(["p0", "p1"], deck)


@pytest.mark.parametrize("players", [[], ["p0"], ["p0", "p1", "p2"]])
def test_match_rejects_empty_or_odd_player_lists(players):
    with pytest.raises(ValueError):
        Match(players)


def test_match_rejects_more_than_twelve_players():
    with pytest.raises(ValueError):
        Match([f"p{i}" for i in range(14)])


def test_match_rejects_duplicate_player_ids():
    with pytest.raises(ValueError):
        Match(["p0", "p0"])


INVALID_INDICES = [True, False, 0.0, 1.5, "0", "abc", None, -1, 3, 99]


@pytest.mark.parametrize("index", INVALID_INDICES)
def test_player_hand_rejects_adversarial_card_indices_without_mutation(index):
    cards = [Card(Suits.CLUBS, "4"), Card(Suits.DIAMONDS, "5"), Card(Suits.SPADES, "3")]
    hand = PlayerHand(cards)
    before = list(hand.cards)

    result = hand.play_card(index)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_CARD_INDEX
    assert hand.cards == before


@pytest.mark.parametrize("index", INVALID_INDICES)
def test_hand_rejects_adversarial_card_indices_without_mutation(index):
    hand = make_hand()
    before = {pid: list(player.cards) for pid, player in hand.hands.items()}

    result = hand.play_card("p0", index)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_CARD_INDEX
    assert {pid: list(player.cards) for pid, player in hand.hands.items()} == before


@pytest.mark.parametrize("index", INVALID_INDICES)
def test_match_rejects_adversarial_card_indices_without_mutation(index):
    match = Match(PLAYERS, lambda: team_zero_deck())
    before = {pid: list(player.cards) for pid, player in match.current_hand.hands.items()}

    result = match.play_card("p0", index)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_CARD_INDEX
    assert {pid: list(player.cards) for pid, player in match.current_hand.hands.items()} == before


@pytest.mark.parametrize("team", [True, False, -1, 2, 99, 0.0, "0", None])
@pytest.mark.parametrize("operation", ["request_raise", "accept_raise", "fold_raise"])
def test_betting_rejects_invalid_team_types(operation, team):
    betting = Betting()
    before = copy.deepcopy(betting.__dict__)

    result = getattr(betting, operation)(team)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_TEAM
    assert betting.__dict__ == before


@pytest.mark.parametrize("operation", ["accept_raise", "fold_raise"])
def test_betting_accept_or_fold_without_pending_raise(operation):
    betting = Betting()
    before = copy.deepcopy(betting.__dict__)
    result = getattr(betting, operation)(1)
    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.NO_PENDING_RAISE
    assert betting.__dict__ == before


@pytest.mark.parametrize("operation", ["accept_raise", "fold_raise"])
def test_betting_requester_cannot_accept_or_fold(operation):
    betting = Betting()
    assert isinstance(betting.request_raise(0), Success)
    before = copy.deepcopy(betting.__dict__)
    result = getattr(betting, operation)(0)
    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.SAME_TEAM_RAISE
    assert betting.__dict__ == before


def test_betting_same_team_cannot_raise_consecutively():
    betting = Betting()
    assert isinstance(betting.request_raise(0), Success)
    before = copy.deepcopy(betting.__dict__)
    result = betting.request_raise(0)
    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.SAME_TEAM_RAISE
    assert betting.__dict__ == before


def test_betting_cannot_raise_past_twelve():
    betting = Betting()
    for team in (0, 1, 0, 1):
        assert isinstance(betting.request_raise(team), Success)
    before = copy.deepcopy(betting.__dict__)
    result = betting.request_raise(0)
    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.OUT_OF_RAISING_INDEX
    assert betting.__dict__ == before


@pytest.mark.parametrize("player_id", ["ghost", "", None])
def test_hand_to_dict_rejects_unknown_player(player_id):
    hand = make_hand()
    result = hand.to_dict(player_id)
    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_PLAYER


@pytest.mark.parametrize("player_id", ["ghost", "", None])
def test_match_get_state_rejects_unknown_player(player_id):
    match = Match(PLAYERS, lambda: team_zero_deck())
    result = match.get_state(player_id)
    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_PLAYER


def test_match_play_is_blocked_by_pending_raise_without_mutation():
    match = Match(PLAYERS, lambda: team_zero_deck())
    before_cards = {pid: list(p.cards) for pid, p in match.current_hand.hands.items()}
    assert isinstance(match.request_raise("p0"), Success)
    before_state = copy.deepcopy(match.__dict__)
    before_state["current_hand"] = match.current_hand

    result = match.play_card("p0", 0)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.PENDING_RAISE
    assert match.points == [0, 0]
    assert match.betting.pending is True
    assert {pid: list(p.cards) for pid, p in match.current_hand.hands.items()} == before_cards


def test_hand_play_is_blocked_on_finished_trick_without_mutation():
    hand = make_hand()
    hand.current_trick.result = TrickResult(None)
    hand.current_trick.plays = [
        hand.hands["p0"].cards[0],
        hand.hands["p1"].cards[0],
    ]
    before_cards = {pid: list(p.cards) for pid, p in hand.hands.items()}
    before_plays = list(hand.current_trick.plays)

    result = hand.play_card("p0", 0)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_TRICK_RESULT
    assert {pid: list(p.cards) for pid, p in hand.hands.items()} == before_cards
    assert hand.current_trick.plays == before_plays


def test_match_play_is_blocked_on_finished_trick_without_mutation():
    match = Match(PLAYERS, lambda: team_zero_deck())
    match.current_hand.current_trick.result = TrickResult(None)
    match.current_hand.current_trick.plays = [
        match.current_hand.hands[player_id].cards[0]
        for player_id in match.current_hand.current_trick.players_order
    ]
    before_cards = {pid: list(p.cards) for pid, p in match.current_hand.hands.items()}
    before_plays = list(match.current_hand.current_trick.plays)

    result = match.play_card("p0", 0)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_TRICK_RESULT
    assert {pid: list(p.cards) for pid, p in match.current_hand.hands.items()} == before_cards
    assert match.current_hand.current_trick.plays == before_plays


@pytest.mark.parametrize("owner", ["hand", "match"])
def test_play_is_blocked_on_finished_hand_or_match_without_mutation(owner):
    if owner == "hand":
        hand = make_hand()
        hand.finished = True
        before_cards = {pid: list(p.cards) for pid, p in hand.hands.items()}
        result = hand.play_card("p0", 0)
        assert isinstance(result, Failure)
        assert result.error.code is ErrorType.HAND_ALREADY_FINISHED
        assert {pid: list(p.cards) for pid, p in hand.hands.items()} == before_cards
    else:
        match = Match(PLAYERS, lambda: team_zero_deck())
        match.finished = True
        before_cards = {pid: list(p.cards) for pid, p in match.current_hand.hands.items()}
        before_points = list(match.points)
        result = match.play_card("p0", 0)
        assert isinstance(result, Failure)
        assert result.error.code is ErrorType.MATCH_ALREADY_FINISHED
        assert match.points == before_points
        assert {pid: list(p.cards) for pid, p in match.current_hand.hands.items()} == before_cards
