from src.cards.card import Card
from src.cards.deck import Deck
from src.cards.suits import Suits


def test_deck_contains_forty_unique_cards():
    deck = Deck()

    assert len(deck.cards) == 40
    assert len(set(deck.cards)) == 40


def test_deck_contains_all_suits_and_ranks():
    deck = Deck()
    ranks = {"4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"}

    assert {card.suit for card in deck.cards} == set(Suits)
    assert {card.number for card in deck.cards} == ranks
    assert all(
        sum(card.suit is suit and card.number == rank for card in deck.cards) == 1
        for suit in Suits
        for rank in ranks
    )


def test_create_deck_repopulates_an_empty_deck():
    deck = Deck()
    deck.cards = []

    deck.create_deck()

    assert len(deck.cards) == 40


def test_draw_removes_and_returns_the_top_card():
    deck = Deck()
    top_card = deck.cards[-1]

    drawn = deck.draw()

    assert drawn is top_card
    assert drawn not in deck.cards
    assert len(deck.cards) == 39


def test_draw_returns_cards_as_card_instances():
    deck = Deck()

    for _ in range(40):
        assert isinstance(deck.draw(), Card)

    assert deck.cards == []
