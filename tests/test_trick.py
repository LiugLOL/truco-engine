from src.game.trick import Trick
from src.cards.card import Card
from src.cards.suits import Suits
from src.core.result import Success, Failure


def players(n):
    return [f"p{i}" for i in range(n)]


def test_play_before_completion_returns_success_and_contains_player_and_card():
    order = players(3)
    turn = Card(Suits.CLUBS, "Q")  # manilha = J
    trick = Trick(order, turn)

    card = Card(Suits.HEARTS, "4")
    res = trick.add_play(card)

    assert isinstance(res, Success)
    play = res.value
    assert play.player_id == order[0]
    assert play.card == card
    assert play.trick_result is None
    assert trick.result is None


def test_unique_highest_normal_card_produces_correct_winner_index():
    order = players(3)
    turn = Card(Suits.SPADES, "Q")
    trick = Trick(order, turn)

    # plays: p0->4, p1->A, p2->2 => winner should be index 2 ("2")
    trick.add_play(Card(Suits.CLUBS, "4"))
    trick.add_play(Card(Suits.CLUBS, "A"))
    final = trick.add_play(Card(Suits.CLUBS, "2"))

    assert isinstance(final, Success)
    assert trick.result is not None
    assert final.value.trick_result is not None
    assert final.value.trick_result.winner_index == 2
    assert not final.value.trick_result.tied


def test_equal_highest_normal_cards_produce_tie():
    order = players(3)
    turn = Card(Suits.HEARTS, "5")
    trick = Trick(order, turn)

    trick.add_play(Card(Suits.CLUBS, "3"))
    trick.add_play(Card(Suits.DIAMONDS, "3"))
    final = trick.add_play(Card(Suits.SPADES, "2"))  # lower than 3

    assert isinstance(final, Success)
    assert final.value.trick_result is not None
    assert final.value.trick_result.winner_index is None
    assert final.value.trick_result.tied


def test_manilha_beats_every_normal_card():
    order = players(3)
    # turn card such that manilha = "5"
    turn = Card(Suits.CLUBS, "4")
    trick = Trick(order, turn)

    trick.add_play(Card(Suits.DIAMONDS, "3"))
    trick.add_play(Card(Suits.DIAMONDS, "6"))
    # manilha play
    final = trick.add_play(Card(Suits.DIAMONDS, "5"))

    assert isinstance(final, Success)
    assert final.value.trick_result is not None
    # manilha should win -> index 2
    assert final.value.trick_result.winner_index == 2


def test_manilha_suit_strength_order():
    order = players(4)
    turn = Card(Suits.HEARTS, "Q")  # manilha = J
    trick = Trick(order, turn)

    # play J of different suits in strength order
    trick.add_play(Card(Suits.DIAMONDS, "J"))  # weakest
    trick.add_play(Card(Suits.SPADES, "J"))
    trick.add_play(Card(Suits.HEARTS, "J"))
    final = trick.add_play(Card(Suits.CLUBS, "J"))  # strongest

    assert isinstance(final, Success)
    assert final.value.trick_result is not None
    assert final.value.trick_result.winner_index == 3


def test_manilha_wraps_after_three():
    order = players(2)
    turn = Card(Suits.SPADES, "3")
    trick = Trick(order, turn)

    assert trick.manilha == "4"


def test_trick_supports_six_players_and_stores_result():
    order = players(6)
    turn = Card(Suits.CLUBS, "7")
    trick = Trick(order, turn)

    # play six cards, final play should set result
    for i in range(5):
        r = trick.add_play(Card(Suits.CLUBS, "4"))
        assert isinstance(r, Success)
        assert r.value.trick_result is None

    final = trick.add_play(Card(Suits.CLUBS, "3"))
    assert isinstance(final, Success)
    assert final.value.trick_result is not None
    assert trick.result is not None


def test_add_play_after_completion_returns_failure_and_does_not_mutate_trick():
    order = players(3)
    turn = Card(Suits.CLUBS, "4")
    trick = Trick(order, turn)

    trick.add_play(Card(Suits.CLUBS, "4"))
    trick.add_play(Card(Suits.CLUBS, "5"))
    final = trick.add_play(Card(Suits.CLUBS, "6"))

    assert isinstance(final, Success)
    old_plays = list(trick.plays)
    old_result = trick.result

    rejected = trick.add_play(Card(Suits.CLUBS, "7"))
    assert isinstance(rejected, Failure)
    # plays not changed
    assert trick.plays == old_plays
    # result not replaced
    assert trick.result == old_result
