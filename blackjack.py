import os
import random

# Define the deck of cards
suits = ('♥', '♦', '♠', '♣')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True

# Define card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit

# Define deck class
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

# Define player class to manage balance and chips
class Player:
    def __init__(self, balance=1000, bet=0):
        self.balance = balance
        self.bet = bet

    def win_bet(self):
        self.balance += self.bet

    def lose_bet(self):
        self.balance -= self.bet

# Initialize player
player = Player()

# Define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1



def take_bet(player):
    while True:
        try:
            player.bet = int(input("How much would you like to bet? "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if player.bet > player.balance:
            print("Sorry, your bet cannot exceed your balance of", player.balance)
        else:
            break

# Function to take a hit
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# Function to prompt the Player for their hit or stand decision
def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Would you like to Hit or Stand? Enter h or s: ")

        if x[0].lower() == 'h':
            hit(deck, hand)
            os.system('cls')

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False
            os.system('cls')

        else:
            print("Sorry, please try again.")
            continue
        break

# Function to display cards (partial or all)
def show_some(player_hand, dealer_hand):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer_hand.cards[1])
    print("\nPlayer's Hand:", *player_hand.cards, sep='\n ')
    print("Player's Hand =", player_hand.value)

def show_all(player_hand, dealer_hand):
    print("\nDealer's Hand:",*dealer_hand.cards, sep='\n ')
    print("Dealer's Hand =", dealer_hand.value)
    print("\nPlayer's Hand:", *player_hand.cards, sep='\n ')
    print("Player's Hand =", player_hand.value)

# Functions to handle end of game scenarios
def player_busts(player_hand):
    print("Player busts!")

def player_wins(player_hand):
    print("Player wins!")

def dealer_busts(dealer_hand):
    print("Dealer busts!")

def dealer_wins(dealer_hand):
    print("Dealer wins!")

def push(player_hand, dealer_hand):
    print("Dealer and Player tie! It's a push.")

while True:
    # Print an opening statement
    print('Welcome to Blackjack! Your current balance is:', player.balance)

    # Take a bet from the player
    take_bet(player)

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of the loop. The player has busted.

        if player_hand.value > 21:
            player_busts(player_hand)
            player.lose_bet()
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(dealer_hand)
            player.win_bet()

        elif dealer_hand.value > player_hand.value:
            dealer_wins(dealer_hand)
            player.lose_bet()

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand)
            player.win_bet()

        else:
            push(player_hand, dealer_hand)


    # Display player's balance after each round
    print("Your current balance is:", player.balance)

    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n': ")
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break
