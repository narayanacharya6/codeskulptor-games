import simpleguitk as simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        hand = ""
        for i in self.hand:
            hand += " " + i.get_suit() + i.get_rank()
        return "Hand contains" + hand

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        contains_aces = False
        for i in self.hand:
            value = value + VALUES[i.get_rank()]
            if i.get_rank() == 'A':
                contains_aces = True
        if contains_aces:
            if value + 10 <= 21:
                value = value + 10
        return value

    def draw(self, canvas, pos):
        global CARD_SIZE
        # draw a hand on the canvas, use the draw method for cards
        for card in self.hand:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0] + 10


# define deck class
class Deck:
    def __init__(self):
        # create a Deck object
        global SUITS, RANKS
        self.DeckCards = []
        for suit in SUITS:
            for rank in RANKS:
                self.DeckCards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck
        # use random.shuffle()
        random.shuffle(self.DeckCards)

    def deal_card(self):
        # deal a card object from the deck
        return self.DeckCards.pop()

    def __str__(self):
        # return a string representing the deck
        deck_str = ""
        for i in self.DeckCards:
            deck_str += " " + i.get_suit() + i.get_rank()
        return "Deck contains" + deck_str


# define event handlers for buttons
def deal():
    global outcome, in_play, deck, score
    if in_play:
        score -= 1
    deck = Deck()
    deck.shuffle()
    global player_hand
    global dealer_hand
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    # print "Player Hand : ",player_hand
    # print "Dealer Hand : ",dealer_hand
    outcome = "HIT or STAND ?"
    in_play = True


def hit():
    global outcome, in_play, player_hand, dealer_hand, deck, score
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            in_play = False
            outcome = "Player busted! NEW DEAL??"
            score -= 1
            # print outcome
            # print "SCORE: ",score
    else:
        pass
    # print "Player Hand : ",player_hand
    # print "Dealer Hand : ",dealer_hand


def stand():
    global outcome, in_play, player_hand, dealer_hand, deck, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "Dealer busted! Player WINS!"
            score += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = "Dealer WINS! NEW DEAL ?"
            score -= 1
        else:
            outcome = "Player WINS! NEW DEAL ?"
            score += 1

        in_play = False
        # print outcome
        # print "Player Hand : ",player_hand
        # print "Dealer Hand : ",dealer_hand
        # print "SCORE: ",score
    else:
        pass


# draw handler
def draw(canvas):
    global outcome, score, player_hand, dealer_hand, in_play, card_back, CARD_BACK_SIZE, CARD_BACK_CENTER, CARD_SIZE
    # test to make sure that card.draw works, replace with your code below
    # card = Card("S", "A")
    # card.draw(canvas, [300, 300])
    canvas.draw_text("BLACKJACK", [180, 40], 50, 'BLACK')
    canvas.draw_text(outcome, [100, 100], 20, "WHITE")
    canvas.draw_text("SCORE : " + str(score), [400, 100], 30, "RED")
    canvas.draw_text("Player's Hand", [100, 200], 40, "WHITE")
    player_hand.draw(canvas, [100, 230])
    if in_play:
        canvas.draw_text("Dealer's Hand", [100, 380], 40, "BLACK")
        dealer_hand.draw(canvas, [100, 410])
        canvas.draw_image(card_back, [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]],
                          [CARD_BACK_SIZE[0], CARD_BACK_SIZE[1]],
                          [100 + CARD_BACK_CENTER[0], 410 + CARD_BACK_CENTER[1]],
                          [CARD_SIZE[0], CARD_SIZE[1]])
    else:
        canvas.draw_text("Dealer's Hand", [100, 380], 40, "BLACK")
        dealer_hand.draw(canvas, [100, 410])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# some important glabal variables
deck = Deck()

# get things rolling
deal()
frame.start()