import random


class EasyBlackjack:
    """Generate a Single-Deck Blackjack hand or calculate a Blackjack hand value."""

    def __init__(self):
        """Initialize the valid values, the suits and the points list."""
        self._values = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
        self._suits = ('C', 'D', 'H', 'S')
        self._points = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'J': 10,
            'Q': 10,
            'K': 10,
            'A': 11
        }

    @property
    def values(self) -> tuple:
        """Read-only access to all the valid values."""

        return self._values

    @property
    def suits(self) -> tuple:
        """Read-only access to all the suits."""

        return self._suits

    @property
    def points(self) -> dict:
        """Read-only access to the points list."""
        
        return self._points

    def generate_cards(self, calculate_points: bool = True) -> dict:
        """Generate two random cards with their value.

        The cards are returned as a dictionary with three items:

            * `card_one`, `card_two`: dictionaries with two items each (`value` and `suit`)
            * `points`: an integer value

        If `calculate_points` is not True, the hand value represented by the `points`
        item, is not returned.
        """

        card_one_value = self._values[random.randint(0, len(self._values) - 1)]
        card_one_suit = self._suits[random.randint(0, len(self._suits) - 1)]

        # Generates the second card until it's different from the first.
        while True:
            card_two_value = self._values[random.randint(0, len(self._values) - 1)]
            card_two_suit = self._suits[random.randint(0, len(self._suits) - 1)]
            if card_one_value + card_one_suit != card_two_value + card_two_suit:
                break

        cards = {
            'card_one': {
                'value': card_one_value,
                'suit': card_one_suit
            },
            'card_two': {
                'value': card_two_value,
                'suit': card_two_suit
            }
        }

        if calculate_points is True:
            points = {
                'points': self.calculate_points([card_one_value, card_two_value])
            }
            cards.update(points)

        return cards

    def calculate_points(self, cards: list) -> int:
        """Calculate the value of a given list of cards.

        The only supported way to pass the cards is by passing them in a list
        in which each single card is represented by its respective value:

            * Ace: 'A'
            * King: 'K'
            * Queen: 'Q'
            * Jack: 'J'
            * Ten: '1'`
            * Nine: '9'
            * Eight: '8'
            * Seven: '7'
            * Six: '6'
            * Five: '5'
            * Four: '4'
            * Three: '3'
            * Two: '2'

        The valid values are also available in the `values` property.
        """

        if not isinstance(cards, list):
            raise TypeError("the 'cards' argument must be a list")

        aces = 0
        points = 0
        for card in cards:
            if str(card).upper() not in self._points:
                raise ValueError (f"'{card}' is not a valid card")
                
            if (str(card).upper() == 'A'):
                aces += 1
            points += self._points[str(card).upper()]

        while points > 21 and aces > 0:
            points -= 10
            aces -= 1

        if points > 21:
            points = 0
            
        return points