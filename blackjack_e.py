import random

suits= ['♦', '♥', '♣', '♠']#♥♦♣♠
ranking = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
value = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,'J':10,'Q':10,'K':10, 'A':11}
chips_standard = 1000

chips = chips_standard

class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
        if self.rank == 'A':
            self.ass = True
        else:
            self.ass = False
    def __str__(self):
        return self.suit + self.rank
    def print_card(self):
        print(self.suit + self.rank)
        return
    

class Deck:
    def __init__(self):
        self.deck_list =[]
        for rank in ranking:
            for suit in suits:
                self.deck_list.append(Card(rank, suit))
        self.deck_list = self.deck_list * 4
    def __str__(self):
        list = ''
        for card in self.deck_list:
            list += '\n'+ card.rank + card.suit
        return list
    def shuffle(self):
        random.shuffle(self.deck_list)
    def hand_out(self):
        upper_card = self.deck_list.pop()
        return upper_card


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
    def add_card(self, card):
        self.cards.append(card)
        self.value += value[card.rank]
        if card.ass == True and self.value >21:
            self.value -= 10   
    def print_hand(self):
        number_cards = len(self.cards)
        for i in range(0,number_cards):
            self.cards[i].print_card()
    def print_wert(self):
        print('Wert der Karten: %i'%self.value)

def start_round():
    global chips
    bet = 0
    print('\n \n \nEine neue Runde ist gestartet! ')
    while bet not in range(1,(chips+1)):
        bet = (eval(input('Sie haben noch %i Chips. Wieviel möchten Sie setzen? ' %chips)))
    print('Sie haben %i Chips gesetzt!' %bet)
    hand_out_cards(bet)

def hand_out_cards(bet):
    stapel = Deck()    
    stapel.shuffle()
    hand_player = Hand()
    hand_casino = Hand()
    hand_player.add_card(stapel.hand_out())
    hand_casino.add_card(stapel.hand_out())
    hand_player.add_card(stapel.hand_out())
    print('Deine Karten:')
    hand_player.print_hand()
    hand_player.print_wert()
    if hand_player.value == 21:
        blackjack(bet)
        return
    print('Karten des Groupiers:')
    hand_casino.print_hand()
    decide(bet, hand_player, hand_casino, stapel)

def decide(bet, hand_player, hand_casino, stapel):
    decision = ''
    while decision.lower() not in ['h', 's']:
        decision = str(input('Drücken Sie "h" für eine weitere Card oder "s" für Stehen!'))
    if decision == 'h':
        hand_player.add_card(stapel.hand_out())
        hand_player.print_hand()
        hand_player.print_wert()
        if hand_player.value == 21:
            stay(bet, hand_player, hand_casino, stapel)
        elif hand_player.value > 21:
            lose(bet)
        elif hand_player.value < 21:
            decide(bet, hand_player, hand_casino, stapel)
    elif decision == 's':
        stay(bet, hand_player, hand_casino, stapel)

def stay(bet, hand_player, hand_casino, stapel):
    hand_casino.add_card(stapel.hand_out())
    hand_casino.print_hand()
    while hand_casino.value <= 16:
        hand_casino.add_card(stapel.hand_out())
        print('Karten des Groupiers: ')
        hand_casino.print_hand()
        hand_casino.print_wert()
        if hand_casino.value > 21:
            win(bet)
    evaluation(bet, hand_player, hand_casino)

def evaluation(bet, hand_player, hand_casino):
    if hand_player.value > hand_casino.value:
        win(bet)
    elif hand_player.value == hand_casino.value:
        draw(bet)
    elif hand_player.value < hand_casino.value:
        lose(bet)

def lose(bet):
    global chips
    print('Sie haben leider verloren!')
    chips = chips - bet
    end_round()

def draw(bet):
    global chips
    print('Die Runde endet draw!')
    end_round()

def win(bet):
    global chips
    print('Glückunsch Sie haben gewonnen! Ihr Gewinn: %i Chips' %bet)
    chips = chips + bet
    end_round()

def blackjack(bet):
    global chips
    chips_won = (bet * 1.5)
    chips = chips + chips_won
    print('Gratuliere, Sie haben mit einem BlackJack gewonnen! Ihr Gewinn: %i Chips' %chips_won)
    end_round()

def end_round():
    global chips
    if chips == 0:
        print('Sie haben leider ihr Guthaben verspielt.')
        end()
        return
    action = ""
    while action not in ['w', 'e']:
            action = str(input('"w" zum Weiterspielen oder "e" zum aussteigen!'))
    if action == 'w':
        start_round()
    elif action == 'e':
        print('Glückwunsch, Sie steigen mit %i Chips aus' %chips)
        return
def intro():
    print('Herzlich Willkommen bei BlackJack! Ziel ist es mit den Karten 21 zu erreichen. Der Dealer zieht Karten bis 16, und bleibt stehen ab 17. \n Sie starten mit 1000 Chips. Viel Glück!')

def end():
    print('Danke für das Spielen von Blackjack! Bis zum nächsten Mal!')
intro()
start_round()

