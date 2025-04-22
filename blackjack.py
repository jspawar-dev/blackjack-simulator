import random


def main() -> None:
    # Create a shuffled Blackjack Deck.
    deck: list[str] = create_deck()

    # When to reshuffle the deck
    MAX_DECK_LENGTH: int = len(deck)
    CARDS_REMAINING: int = 20 # reshuffle threshold (%)
    RESHUFFLE: float = MAX_DECK_LENGTH * (CARDS_REMAINING / 100)

    SIMULATE: int = 1000000 # How many Blackjack games to simulate
    PLAYER_HIT_UNTIL: int = 12 # When player stands

    # Scoreboard
    win: int = 0
    push: int = 0
    lose: int = 0

    for _ in range(SIMULATE):
        # Check if deck needs to be reshuffled.
        if len(deck) < RESHUFFLE:
            deck = create_deck()

        result: int = play_blackjack(deck, PLAYER_HIT_UNTIL)

        match result:
            case 1:
                win += 1
            case -1:
                lose += 1
            case 0:
                push += 1

    print(f"Games Played: {SIMULATE:,}")
    print(f"Win: {(win / SIMULATE) * 100:.2f}%")
    print(f"Push: {push / SIMULATE * 100:.2f}%")
    print(f"Lose: {lose / SIMULATE * 100:.2f}%")


def create_deck() -> list[str]:
    """
    This function creates and shuffles a Blackjack deck.

    :return: Returns a shuffled Blackjack deck
    """

    # A standard deck of playing cards consists of 52 cards.
    standard_deck: list[str] = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4

    # A Blackjack deck can be made up of 1-8 standard decks.
    NUM_OF_DECKS: int = 8
    deck: list[str] = standard_deck * NUM_OF_DECKS
    random.shuffle(deck)

    return deck


def draw_card(deck: list[str]) -> str:
    """
    Draws a card from the deck.

    :param deck: The deck to draw from
    :return: Returns the card drawn from the deck
    """

    return deck.pop()


def calculate_hand(cards: list[str]) -> int:
    """
    Calculates the total value of a hand in Blackjack, taking into account the value of Aces.

    :param cards: The cards in the hand
    :return: Returns the total value of the hand
    """

    total = []
    ace_count = 0

    # checks each card in the hand and appends the cards value into a list.
    for card in cards:
        match card:
            case 'J' | 'Q' | 'K':
                total.append(10)
            case 'A':
                # Aces aren't appended as they can be either 11, or 1.
                ace_count += 1
            case _:
                total.append(int(card))

    # Determines whether an ace should be classed as 11, or 1.
    while ace_count != 0:
        # An ace will only be classed as 11, as long as the other cards totals don't exceed 10.
        if sum(total) <= 10:
            total.append(11)
            ace_count -= 1
        else:
            # If the total is 21 or over, and a previous ace has been valued at 11. it will remove the 11, and replace it with a 1.
            if sum(total) >= 21 and 11 in total:
                total.remove(11)
                total.append(1)

            total.append(1)
            ace_count -= 1

    return sum(total)


def play_blackjack(deck: list[str], hit_until: int) -> int:
    """
    This function plays a game of Blackjack.

    :param hit_until: Player will keep hitting till this hand value.
    :param deck: The deck to play with
    :return: Returns the result of the game
    """

    player_hand = []
    dealer_hand = []

    # Start of the game, dealer and player draw 2 cards each.
    for _ in range(2):
        player_hand.append(draw_card(deck))
        dealer_hand.append(draw_card(deck))

    # Player will keep drawing cards while their total is less than 12.
    while calculate_hand(player_hand) < hit_until:
        player_hand.append(draw_card(deck))

    # Dealer will keep drawing cards while their total is less than 17.
    # If the dealer is on a soft 17, they will draw again until they are less than 17.
    while calculate_hand(dealer_hand) <= 17:
        if calculate_hand(dealer_hand) == 17:
            if 'A' in dealer_hand and calculate_hand(dealer_hand) - 11 == 6:
                dealer_hand.append(draw_card(deck))
            else:
                break
        dealer_hand.append(draw_card(deck))

    return compare_hands(player_hand, dealer_hand)


def compare_hands(player_hand: list[str], dealer_hand: list[str]) -> int:
    """
    This function compares the cards of the player and dealer, to determine who wins the blackjack round.

    :param player_hand: Players cards
    :param dealer_hand: Dealers cards
    :return: Win = 1, Push = 0, or Lose = -1
    """

    player_total: int = calculate_hand(player_hand)
    dealer_total: int = calculate_hand(dealer_hand)

    # Checks for Busts
    if player_total > 21 and dealer_total > 21:
        return 0
    elif player_total > 21:
        return -1
    elif dealer_total > 21:
        return 1

    # Compares hands, to determine the winning hand.
    if player_total == dealer_total:
        return 0
    elif player_total > dealer_total:
        return 1
    else:
        return -1


if __name__ == '__main__':
    main()
