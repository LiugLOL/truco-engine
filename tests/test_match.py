from src.cards.card import Card
from src.cards.deck import Deck
from src.cards.suits import Suits
from src.core.error_types import ErrorType
from src.core.result import Failure, Success
from src.game.hand import Hand
from src.game.match import Match


PLAYERS = ["p0", "p1", "p2", "p3"]


class DeterministicDeck(Deck):
    def __init__(self, cards: list[Card]):
        self.cards = list(reversed(cards))

    def draw(self) -> Card:
        return self.cards.pop()


def card(number: str, suit: Suits = Suits.CLUBS) -> Card:
    return Card(suit, number)


def make_deck(
    cards_by_player: dict[str, list[Card]],
    turn_card: Card,
    players: list[str] = PLAYERS,
) -> DeterministicDeck:
    cards = [card for player in players for card in cards_by_player[player]]
    cards.append(turn_card)
    return DeterministicDeck(cards)


def team_zero_deck(players: list[str] = PLAYERS) -> DeterministicDeck:
    cards_by_player = {
        "p0": [card("7"), card("7"), card("4")],
        "p1": [card("6"), card("6"), card("4")],
        "p2": [card("5"), card("5"), card("4")],
        "p3": [card("4"), card("4"), card("4")],
    }
    return make_deck(cards_by_player, card("A"), players)


def team_one_deck(players: list[str] = PLAYERS) -> DeterministicDeck:
    cards_by_player = {
        "p0": [card("4"), card("4"), card("4")],
        "p1": [card("7"), card("7"), card("4")],
        "p2": [card("6"), card("6"), card("4")],
        "p3": [card("5"), card("5"), card("4")],
    }
    return make_deck(cards_by_player, card("A"), players)


def rotating_orders(count: int, players: list[str] = PLAYERS) -> list[list[str]]:
    orders = []
    for _ in range(count):
        orders.append(list(players))
        players = players[1:] + players[:1]
    return orders


def tied_deck(players: list[str] = PLAYERS) -> DeterministicDeck:
    cards_by_player = {
        player: [card("6"), card("6"), card("6")]
        for player in players
    }
    return make_deck(cards_by_player, card("A"), players)


def play_entire_hand(match: Match) -> None:
    hand = match.current_hand
    while not hand.finished:
        order = list(hand.current_trick.current_players_order)
        for player_id in order:
            result = match.play_card(player_id, 0)
            assert isinstance(result, Success)


def test_initialization_starts_match_with_initial_hand():
    deck = team_zero_deck()

    match = Match(PLAYERS, lambda: deck)

    assert match.points == [0, 0]
    assert match.finished is False
    assert match.winner is None
    assert isinstance(match.current_hand, Hand)
    assert match.current_hand.current_players_order == PLAYERS


def test_team_zero_win_scores_rotates_table_and_starts_new_hand():
    orders = rotating_orders(2)
    decks = [team_zero_deck(orders[0]), team_zero_deck(orders[1])]

    match = Match(PLAYERS, lambda: decks.pop(0))
    first_hand = match.current_hand

    play_entire_hand(match)

    assert first_hand.finished is True
    assert match.points == [1, 0]
    assert match.players_order == ["p1", "p2", "p3", "p0"]
    assert isinstance(match.current_hand, Hand)
    assert match.current_hand is not first_hand
    assert match.current_hand.current_players_order == match.players_order


def test_team_one_wins_on_second_hand_after_table_rotation():
    decks = [
        team_zero_deck(),
        team_one_deck(["p1", "p2", "p3", "p0"]),
        team_zero_deck(),
    ]

    match = Match(PLAYERS, lambda: decks.pop(0))
    play_entire_hand(match)

    assert match.points == [1, 0]
    assert match.players_order == ["p1", "p2", "p3", "p0"]

    second_hand = match.current_hand
    play_entire_hand(match)

    assert second_hand.finished is True
    assert match.points == [1, 1]
    assert match.players_order == ["p2", "p3", "p0", "p1"]
    assert match.team_by_player["p1"] == 1
    assert match.team_by_player["p3"] == 1


def test_fully_tied_hand_scores_nothing_but_rotates_table():
    decks = [tied_deck(), team_zero_deck()]

    match = Match(PLAYERS, lambda: decks.pop(0))
    first_hand = match.current_hand

    play_entire_hand(match)

    assert first_hand.finished is True
    assert first_hand.winner is None
    assert match.points == [0, 0]
    assert match.players_order == ["p1", "p2", "p3", "p0"]
    assert isinstance(match.current_hand, Hand)
    assert match.current_hand is not first_hand


def test_playing_out_of_turn_does_not_change_match_state():
    match = Match(PLAYERS, lambda: team_zero_deck())
    original_hand = match.current_hand

    result = match.play_card("p1", 0)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.NOT_PLAYER_TURN
    assert match.points == [0, 0]
    assert match.current_hand is original_hand
    assert match.players_order == PLAYERS


def test_invalid_card_index_does_not_change_match_state():
    match = Match(PLAYERS, lambda: team_zero_deck())
    original_hand = match.current_hand

    result = match.play_card("p0", 3)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_CARD_INDEX
    assert match.points == [0, 0]
    assert match.current_hand is original_hand
    assert match.players_order == PLAYERS


def test_team_zero_reaches_twelve_points_finishes_match_and_blocks_play():
    orders = rotating_orders(12)
    decks = [team_zero_deck(order) for order in orders]

    match = Match(PLAYERS, lambda: decks.pop(0))

    for _ in range(12):
        play_entire_hand(match)

    assert match.points == [12, 0]
    assert match.finished is True
    assert match.winner == 0
    assert match.current_hand.finished is True

    result = match.play_card("p0", 0)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.MATCH_ALREADY_FINISHED
    assert match.points == [12, 0]
    assert len(decks) == 0


def test_team_one_reaches_twelve_points_and_wins_match():
    orders = rotating_orders(12)
    decks = [team_one_deck(order) for order in orders]

    match = Match(PLAYERS, lambda: decks.pop(0))

    for _ in range(12):
        play_entire_hand(match)

    assert match.points == [0, 12]
    assert match.finished is True
    assert match.winner == 1


def test_two_player_match_supports_mano_a_mano_play():
    players = ["p0", "p1"]
    cards_by_player = {
        "p0": [card("7"), card("7"), card("4")],
        "p1": [card("6"), card("6"), card("4")],
    }
    decks = [
        make_deck(cards_by_player, card("A"), players),
        make_deck(cards_by_player, card("A"), players),
    ]

    match = Match(players, lambda: decks.pop(0))

    play_entire_hand(match)

    assert match.points == [1, 0]
    assert match.winner is None
    assert match.finished is False
    assert match.players_order == ["p1", "p0"]
