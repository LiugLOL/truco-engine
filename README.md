# Truco Engine

A reusable, transport-independent Python engine for Truco card games.

> **Project status: under active development.** Core hand and match flows,
> betting, and match-state serialization are implemented. The API may change
> while special hand rules such as Mão de 11 and Mão de Ferro are completed.

## Overview

Truco Engine provides card ranking, deck and hand management, trick resolution,
turn validation, betting escalation, match scoring, and JSON-ready match state.
It does not include networking, UI, or application-framework dependencies.

## Features

- 40-card deck creation and randomized shuffling
- Three-card hands for even player counts
- Vira-based mobile manilhas and suit-strength ranking
- Turn and card-index validation
- Trick winner rotation and tie handling
- Typed `Success` and `Failure` results with structured error types
- 12-point match orchestration
- Betting stakes of 1, 3, 6, 9, or 12 points
- Accept, fold, and re-raise betting actions
- Stable team ownership after table rotations
- Public/private and blind-hand state serialization
- Deterministic deck injection through `deck_factory`
- 72 unit tests

## Project Structure

```text
src/
├── cards/
│   ├── card.py
│   ├── deck.py
│   ├── player_hand.py
│   └── suits.py
├── core/
│   ├── error_types.py
│   └── result.py
└── game/
    ├── betting.py
    ├── hand.py
    ├── match.py
    └── trick.py

tests/
├── test_betting.py
├── test_deck.py
├── test_hand.py
├── test_match.py
├── test_match_betting.py
├── test_player_hand.py
├── test_serialization.py
└── test_trick.py
```

## Installation

```bash
git clone https://github.com/LiugLOL/truco-engine.git
cd truco-engine

python -m venv .venv

# Windows
.\.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Running Tests

```bash
python -m pytest
```

The suite currently contains 72 tests covering cards, deck handling, player
hands, trick ranking, hand flow, betting, match scoring, table rotation,
two-player matches, and state serialization.

## Basic Usage

```python
from src.game.hand import Hand

players = ["p0", "p1", "p2", "p3"]
hand = Hand(players)

result = hand.play_card("p0", 0)
```

`Hand.play_card` returns a typed `Success` or `Failure`. Successful plays contain
a `PlayResult`; failures contain an `InternalError` and an `ErrorType` such as
`NOT_PLAYER_TURN` or `INVALID_CARD_INDEX`.

For deterministic tests, pass a deck instance to `Hand` or a deck factory to
`Match`:

```python
hand = Hand(players, deck=my_deterministic_deck)

match = Match(
    players,
    deck_factory=my_deterministic_deck_factory,
)
```

The match factory must return a fresh `Deck`-compatible instance each time a new
hand starts.

## Match Usage

```python
from src.game.match import Match

players = ["p0", "p1", "p2", "p3"]
match = Match(players)

result = match.play_card("p0", 0)
```

Hands start at 1 point and betting can raise the stake to 3, 6, 9, or 12 points.

After a hand finishes:

- the winning team receives the hand stake;
- tied hands award no points;
- the table rotates one position to the left;
- a new hand starts with 1-point betting;
- the match finishes when a team reaches 12 points.

Use `Match.request_raise`, `Match.accept_raise`, and `Match.fold_raise` to
manage betting. Match constructor validation requires a non-empty, even roster
with unique player IDs.

For multiplayer transports, use `Match.get_state(player_id, blind_hand=False)`:

```python
state = match.get_state("p0")
blind_state = match.get_state("p0", blind_hand=True)
```

The returned `Result` contains JSON-ready data with public match state and only
the requesting player's private cards. In blind mode, the requesting player's
cards are hidden. Other players are represented by ID and card count.

## Architecture

- **Cards**: Card values, suits, deck operations, and cards held by a player
- **Core**: Typed success/failure result and domain error types
- **Trick**: Card comparison, manilha ranking, and trick results
- **Hand**: Three-card hand flow, turn validation, tricks, and team winner resolution
- **Betting**: Stake escalation and accepted, folded, and forfeited raises
- **Match**: 12-point scoring, stable team mapping, table rotation, and completion
- **Serialization**: JSON-ready match snapshots with private-hand isolation

The runtime flow is:

1. `Hand` deals three cards to each player and draws the vira.
2. `Hand.play_card` validates the player turn and card index.
3. `Trick` applies the vira-defined manilhas and resolves the trick.
4. `Hand` records trick winners and rotates the next trick.
5. `Match` applies the current betting stake or advances the table after a tie.
6. `Match` starts a fresh 1-point hand unless a team has reached 12 points.

## Roadmap

- [x] Card, deck, suits, and player-hand models
- [x] Trick ranking and mobile-manilha resolution
- [x] Hand lifecycle, turn validation, rotations, and tie handling
- [x] 12-point match orchestration
- [x] Deterministic match tests with injected decks
- [x] Truco bidding and raise escalation rules
- [x] Public/private match state serialization for multiplayer
- [ ] Mão de 11 and Mão de Ferro
- [ ] Post-MVP table rules ("3 segue" and "pegar pena")
- [ ] Transport/network adapters
- [ ] Package and distribution setup
- [ ] Integration guides and examples

## License

This project is licensed under the [MIT License](LICENSE).
