from truco_engine.cards.card import Card
from truco_engine.cards.deck import Deck
from truco_engine.cards.suits import Suits
from truco_engine.core.error_types import ErrorType
from truco_engine.core.result import Failure, Success
from truco_engine.game.hand import Hand


PLAYERS = ["p0", "p1", "p2", "p3"]


class DeterministicDeck(Deck):
    def __init__(self, cards: list[Card]):
        self.cards = list(reversed(cards))

    def draw(self) -> Card:
        return self.cards.pop()


def card(number: str, suit: Suits = Suits.CLUBS) -> Card:
    return Card(suit, number)


def make_deck(cards_by_player: dict[str, list[Card]], turn_card: Card) -> DeterministicDeck:
    cards = [card for player in PLAYERS for card in cards_by_player[player]]
    cards.append(turn_card)
    return DeterministicDeck(cards)


def play_trick(hand: Hand, cards: list[tuple[str, int]]) -> None:
    for player_id, card_index in cards:
        result = hand.play_card(player_id, card_index)
        assert isinstance(result, Success)


def test_initialization_deals_three_cards_and_sets_turn_card():
    cards_by_player = {
        player: [card(str(index + 4)) for index in range(3)]
        for player in PLAYERS
    }
    turn_card = card("A", Suits.HEARTS)
    hand = Hand(PLAYERS, make_deck(cards_by_player, turn_card))

    assert {player: player_hand.cards for player, player_hand in hand.hands.items()} == cards_by_player
    assert hand.turn_card == turn_card
    assert all(hand.turn_card not in player_hand.cards for player_hand in hand.hands.values())
    assert hand.finished is False
    assert hand.winner is None


def test_playing_out_of_turn_returns_not_player_turn():
    cards = {player: [card("6"), card("7"), card("A")] for player in PLAYERS}
    hand = Hand(PLAYERS, make_deck(cards, card("4")))

    result = hand.play_card("p1", 0)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.NOT_PLAYER_TURN


def test_invalid_card_index_returns_invalid_card_index():
    cards = {player: [card("6"), card("7"), card("A")] for player in PLAYERS}
    hand = Hand(PLAYERS, make_deck(cards, card("4")))

    result = hand.play_card("p0", 3)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.INVALID_CARD_INDEX


def test_playing_after_hand_finishes_returns_hand_already_finished():
    cards = {
        "p0": [card("7"), card("7"), card("4")],
        "p1": [card("6"), card("6"), card("4")],
        "p2": [card("5"), card("5"), card("4")],
        "p3": [card("4"), card("4"), card("4")],
    }
    hand = Hand(PLAYERS, make_deck(cards, card("A")))
    play_trick(hand, [(player, 0) for player in PLAYERS])
    play_trick(hand, [(player, 0) for player in PLAYERS])

    result = hand.play_card("p0", 0)

    assert isinstance(result, Failure)
    assert result.error.code is ErrorType.HAND_ALREADY_FINISHED


def test_team_zero_wins_two_tricks_and_hand_finishes_immediately():
    cards = {
        "p0": [card("7"), card("7"), card("4")],
        "p1": [card("6"), card("6"), card("4")],
        "p2": [card("5"), card("5"), card("4")],
        "p3": [card("4"), card("4"), card("4")],
    }
    hand = Hand(PLAYERS, make_deck(cards, card("A")))
    play_trick(hand, [(player, 0) for player in PLAYERS])
    play_trick(hand, [(player, 0) for player in PLAYERS])

    assert hand.finished is True
    assert hand.winner == 0
    assert len(hand.trick_winners) == 2


def test_next_trick_starts_with_trick_winner():
    cards = {
        "p0": [card("4"), card("4"), card("4")],
        "p1": [card("5"), card("4"), card("4")],
        "p2": [card("7"), card("4"), card("4")],
        "p3": [card("6"), card("4"), card("4")],
    }
    hand = Hand(PLAYERS, make_deck(cards, card("A")))
    play_trick(hand, [(player, 0) for player in PLAYERS])

    assert hand.current_trick.players_order == ["p2", "p3", "p0", "p1"]


def test_team_one_wins_after_three_tricks_with_a_turnaround():
    cards = {
        "p0": [card("7"), card("4"), card("4")],
        "p1": [card("6"), card("7"), card("7")],
        "p2": [card("5"), card("6"), card("6")],
        "p3": [card("4"), card("5"), card("5")],
    }
    hand = Hand(PLAYERS, make_deck(cards, card("A")))
    play_trick(hand, [(player, 0) for player in PLAYERS])
    play_trick(hand, [("p0", 0), ("p1", 0), ("p2", 0), ("p3", 0)])
    play_trick(hand, [("p1", 0), ("p2", 0), ("p3", 0), ("p0", 0)])

    assert hand.finished is True
    assert hand.winner == 1


def test_tied_first_trick_then_team_one_wins_second():
    cards = {
        "p0": [card("7"), card("4"), card("4")],
        "p1": [card("7"), card("7"), card("4")],
        "p2": [card("7"), card("6"), card("4")],
        "p3": [card("7"), card("5"), card("4")],
    }
    hand = Hand(PLAYERS, make_deck(cards, card("A")))
    play_trick(hand, [(player, 0) for player in PLAYERS])
    play_trick(hand, [(player, 0) for player in PLAYERS])

    assert hand.finished is True
    assert hand.winner == 1


def test_team_zero_wins_first_trick_and_ties_second():
    cards = {
        "p0": [card("7"), card("6"), card("4")],
        "p1": [card("6"), card("6"), card("4")],
        "p2": [card("5"), card("6"), card("4")],
        "p3": [card("4"), card("6"), card("4")],
    }
    hand = Hand(PLAYERS, make_deck(cards, card("A")))
    play_trick(hand, [(player, 0) for player in PLAYERS])
    play_trick(hand, [(player, 0) for player in PLAYERS])

    assert hand.finished is True
    assert hand.winner == 0


def test_one_trick_each_then_tied_third_trick_goes_to_first_winner():
    cards = {
        "p0": [card("7"), card("4"), card("6")],
        "p1": [card("6"), card("7"), card("6")],
        "p2": [card("5"), card("6"), card("6")],
        "p3": [card("4"), card("5"), card("6")],
    }
    hand = Hand(PLAYERS, make_deck(cards, card("A")))
    play_trick(hand, [(player, 0) for player in PLAYERS])
    play_trick(hand, [("p0", 0), ("p1", 0), ("p2", 0), ("p3", 0)])
    play_trick(hand, [("p1", 0), ("p2", 0), ("p3", 0), ("p0", 0)])

    assert hand.finished is True
    assert hand.winner == 0


def test_three_tied_tricks_finish_without_a_winner():
    cards = {player: [card("6"), card("6"), card("6")] for player in PLAYERS}
    hand = Hand(PLAYERS, make_deck(cards, card("A")))
    for _ in range(3):
        play_trick(hand, [(player, 0) for player in hand.current_trick.players_order])

    assert hand.finished is True
    assert hand.winner is None


def test_turn_card_manilha_beats_a_three_in_hand():
    cards = {
        "p0": [card("3"), card("4"), card("4")],
        "p1": [card("5", Suits.DIAMONDS), card("4"), card("4")],
        "p2": [card("6"), card("4"), card("4")],
        "p3": [card("7"), card("4"), card("4")],
    }
    hand = Hand(PLAYERS, make_deck(cards, card("4", Suits.HEARTS)))
    play_trick(hand, [(player, 0) for player in PLAYERS])

    assert hand.current_trick.players_order == ["p1", "p2", "p3", "p0"]
    assert hand.trick_winners == [1]
