# Blackjack Simulator

A Monte Carlo simulation of a blackjack strategy where the player hits until a specified amount, tracking wins, loses, and pushes over a certain amount of games.

- Simulates Blackjack using 8 decks
- Player hits until a set value (default: 12)
- Dealer hits until 17, follows soft 17 rules
- Calculates win, push, and loss percentages

## Usage

```bash
python blackjack.py
```

## Configuration

Edit these values in the main() function of `blackjack.py` to customize behavior:

```python
SIMULATE = 1000000 # How many Blackjack games to simulate
PLAYER_HIT_UNTIL = 12 # Player hits while hand value is less than 12
CARDS_REMAINING = 20 # reshuffle threshold (%)
```

