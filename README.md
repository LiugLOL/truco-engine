# Truco Engine

A reusable, transport-independent Truco game engine for card-game applications.

> **Project status: under active development.** This repository is public for
> collaboration and early testing. Core hand and match flows are implemented,
> but the API may change as special hand rules (Mão de 11 / Mão de Ferro) and
> multiplayer serialization are completed.

## Overview

**Truco Engine** is a Python library that provides the core rules and state
transitions for a Truco hand without dependencies on networking, user
interfaces, or specific application frameworks. It deals cards, validates
plays, resolves tricks, applies mobile-manilha rules, and determines the hand
winner. It now also coordinates complete matches to 12 points, keeping team
ownership stable while rotating the table between hands.

The engine is designed to be:
- **Independent**: Decoupled from networking, UI, and transport layers
- **Modular**: Organized around cards, players, game flow, and shared results
- **Testable**: Deterministic decks can be injected for predictable tests

## Features

- ✅ Complete deck creation and randomized shuffling
- ✅ Three-card hands for even players(e.g., 2 or 4 players)
- ✅ Vira-based mobile-manilha resolution
- ✅ Trick winner resolution with suit strength
- ✅ Turn validation and card-index validation
- ✅ Trick-order rotation after each winner
- ✅ Tie handling across all three tricks
- ✅ Typed `Success`/`Failure` results with structured error types
- ✅ Basic 12-point match orchestration
- ✅ Truco betting escalation (1 -> 3 -> 6 -> 9 -> 12) with accept, fold, and re-raise handling
- ✅ Dynamic hand scoring (1, 3, 6, 9, or 12 points)
- ✅ Hand scoring and table rotation
- ✅ Stable team assignment for players after table rotations
- ✅ Match completion and `MATCH_ALREADY_FINISHED` protection
- ✅ Support for even player counts, including 2-player matches
- ✅ Deterministic deck injection through `deck_factory`
- ✅ Comprehensive unit test coverage

## Project Structure

```
src/
├── cards/                # Card and deck models
│   ├── card.py           # Immutable Card value object
│   ├── deck.py           # Deck creation, shuffle, and draw operations
│   ├── player_hand.py    # Cards held by one player
│   └── suits.py          # Card suit definitions
├── core/                 # Shared result and error types
│   ├── error_types.py    # Domain error categories
│   └── result.py         # Success, Failure, and InternalError wrappers
├── game/                 # Hand and trick orchestration
│   ├── betting.py        # Truco bidding and raise escalation
│   ├── hand.py           # Hand lifecycle and team winner resolution
│   ├── match.py          # Match-level orchestration boundary
│   └── trick.py          # Trick ranking and manilha rules
├── players/              # Player identity models
│   └── player.py         # Player identifier and hand association
tests/                    # Unit tests (66 passing)
```

## Installation

### Clone the repository

```bash
git clone https://github.com/LiugLOL/truco-engine.git
cd truco-engine
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.\.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Running Tests

Execute the test suite with pytest:

```bash
python -m pytest
```

The project currently contains **66 passing unit tests** covering card
ranking, trick resolution, hand flow, match scoring, table rotation, validation
failures, tie handling, mobile manilhas, match completion, and 2-player matches.

## Basic Usage

The engine accepts a deck through dependency injection, which makes game setup
and tests predictable:

```python
from src.cards.card import Card
from src.cards.deck import Deck
from src.cards.suits import Suits
from src.game.hand import Hand


class DeterministicDeck(Deck):
    def __init__(self, cards):
        self.cards = list(reversed(cards))

    def draw(self):
        return self.cards.pop()


players = ["p0", "p1", "p2", "p3"]
cards = [
    Card(Suits.CLUBS, "4"),
    # Add the remaining dealt cards and the vira in draw order.
]

hand = Hand(players, DeterministicDeck(cards))
result = hand.play_card("p0", 0)
```

`Hand.play_card` returns a typed result. Successful plays contain a
`PlayResult`; rejected operations contain an `InternalError` with an
`ErrorType` such as `NOT_PLAYER_TURN` or `INVALID_CARD_INDEX`.

## Match Usage

`Match` coordinates hands and uses `Betting` to apply the stake of each hand.
Hands start at 1 point and can escalate to 3, 6, 9, or 12 points:

```python
from src.game.match import Match

players = ["p0", "p1", "p2", "p3"]
match = Match(players)

result = match.play_card("p0", 0)
```

After a hand finishes:

- the winning team receives the hand stake set by `Betting`;
- tied hands do not award points;
- the table rotates one position to the left;
- a new `Hand` starts with the rotated player order;
- the match finishes when a team reaches 12 points.

Raise requests can be accepted or folded through `Match.request_raise`,
`Match.accept_raise`, and `Match.fold_raise`.

For deterministic tests and controlled games, provide a `deck_factory`:

```python
match = Match(players, deck_factory=my_deterministic_deck_factory)
```

The factory must return a fresh `Deck` each time a new hand is created.
Matches also support an even number of players, including mano-a-mano play
with two players.

## Architecture

The engine follows a layered game-flow architecture:

- **Cards**: Define cards, suits, deck operations, and player-held cards
- **Players**: Associate a player identifier with a `PlayerHand`
- **Hand**: Coordinates players, three tricks, turn validation, and team
  winner resolution
- **Trick**: Compares cards, applies the vira-defined manilha, and resolves
  ties
- **Betting**: Escalates hand stakes through 1, 3, 6, 9, and 12 points, and
  handles accepted raises, folds, re-raises, and edge-case forfeits
- **Match**: Scores hands to 12 points, rotates the table, and blocks play after
  match completion
- **Core Results**: Communicate success or expected domain failures explicitly

The main runtime flow is:

1. `Hand` deals three cards to each player and draws the vira.
2. `Hand.play_card` validates the hand state, player turn, and card index.
3. `Trick` evaluates cards using the standard order and mobile-manilha power.
4. `Hand` records the trick result and rotates the next trick to its winner.
5. After two decisive tricks, or after the third trick, the hand finishes.
6. `Match` applies the `Betting` stake to the winning team or rotates the table
   after a tie.
7. `Match` starts a fresh hand with 1-point stakes unless a team has reached
   12 points.

## Design Goals

The Truco Engine prioritizes:

- **Rule isolation**: Card ranking and hand scoring remain independent of I/O
- **Explicit state**: Hand, trick, and result objects expose game progress
- **Deterministic testing**: Deck injection removes randomness from scenarios
- **Clear failures**: Invalid actions return structured domain errors
- **Extensibility**: Match orchestration remains isolated from transport and UI

## Current Status

The engine currently supports complete hand and basic match lifecycles for
even player counts. The implemented match flow is:

- `points` begins at `[0, 0]`;
- each hand winner awards the dynamic stake of 1, 3, 6, 9, or 12 points;
- ties award no points;
- the table rotates after every completed hand;
- team ownership remains stable after rotation;
- 12 points finishes the match and prevents further card plays.

Issue [#4 - Implement basic 12-point Match orchestration](https://github.com/LiugLOL/truco-engine/issues/4)
and Issue [#2 - Implement Truco betting and raise escalation](https://github.com/LiugLOL/truco-engine/issues/2)
are closed. Dynamic Match scoring through `Betting` and 12-point match completion
are therefore implemented and covered by unit tests.

## Roadmap

- [x] Card, deck, suits, and player-hand models
- [x] Trick ranking and mobile-manilha resolution
- [x] Hand lifecycle, turn validation, rotations, and tie handling
- [x] Basic 12-point match orchestration (#4)
- [x] Deterministic match tests with injected decks
- [x] Truco bidding and raise escalation rules
- [ ] Hand of 11 and Hand of Iron (Mão de 11 / Mão de Ferro)
- [ ] Public/private match state serialization for multiplayer
- [ ] Post-MVP table rules ("3 segue" verification and "pegar pena" cut)
- [ ] Transport/network adapters outside the core engine
- [ ] Package and distribution setup
- [ ] Documentation, examples, and integration guides

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---
