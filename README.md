# Truco Engine

A reusable, transport-independent Truco game engine for card-game applications.

## Overview

**Truco Engine** is a Python library that provides the core rules and state
transitions for a Truco hand without dependencies on networking, user
interfaces, or specific application frameworks. It deals cards, validates
plays, resolves tricks, applies mobile-manilha rules, and determines the hand
winner.

The engine is designed to be:
- **Independent**: Decoupled from networking, UI, and transport layers
- **Modular**: Organized around cards, players, game flow, and shared results
- **Testable**: Deterministic decks can be injected for predictable tests

## Features

- ✅ Complete deck creation and randomized shuffling
- ✅ Three-card hands for four players
- ✅ Vira-based mobile-manilha resolution
- ✅ Trick winner resolution with suit strength
- ✅ Turn validation and card-index validation
- ✅ Trick-order rotation after each winner
- ✅ Tie handling across all three tricks
- ✅ Typed `Success`/`Failure` results with structured error types
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
│   ├── hand.py           # Hand lifecycle and team winner resolution
│   ├── match.py          # Match-level orchestration boundary
│   └── trick.py          # Trick ranking and manilha rules
├── players/              # Player identity models
│   └── player.py         # Player identifier and hand association
tests/                    # Unit tests (20 passing)
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

## Running Tests

Execute the test suite with pytest:

```bash
.\.venv\Scripts\pytest
```

The project currently contains **20 passing unit tests** covering card
ranking, trick resolution, hand flow, validation failures, tie handling, and
mobile manilhas.

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

## Architecture

The engine follows a layered game-flow architecture:

- **Cards**: Define cards, suits, deck operations, and player-held cards
- **Players**: Associate a player identifier with a `PlayerHand`
- **Hand**: Coordinates four players, three tricks, turn validation, and team
  winner resolution
- **Trick**: Compares cards, applies the vira-defined manilha, and resolves
  ties
- **Core Results**: Communicate success or expected domain failures explicitly

The main runtime flow is:

1. `Hand` deals three cards to each player and draws the vira.
2. `Hand.play_card` validates the hand state, player turn, and card index.
3. `Trick` evaluates cards using the standard order and mobile-manilha power.
4. `Hand` records the trick result and rotates the next trick to its winner.
5. After two decisive tricks, or after the third trick, the hand finishes.

## Design Goals

The Truco Engine prioritizes:

- **Rule isolation**: Card ranking and hand scoring remain independent of I/O
- **Explicit state**: Hand, trick, and result objects expose game progress
- **Deterministic testing**: Deck injection removes randomness from scenarios
- **Clear failures**: Invalid actions return structured domain errors
- **Extensibility**: Match orchestration can be added above the hand boundary

## Current Status

The current implementation supports a complete four-player hand lifecycle,
including normal wins, rotations, mobile manilhas, and all required tie
outcomes. Match-level orchestration remains a documented integration boundary;
the active implementation is centered on `Hand` and `Trick`.

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---


