import random

class BlackjackGame:

    # TODO: incorporate a max number of splits 
    # Show a player who splits all their pairs of cards before making him play the game for one of the hands

    # Initializes the data structures needed
    # shoe holds 4 decks worth of the String representation of a card (e.g. "Eight of Spades")
    # cardToNumber is a dictionary that pairs the string card value with the blackjack value (e.g. "Queen" -> 10)
    # totals and hands hold the values and the respective hands of all the players, including the house. The house is always index 0
    def __init__(self, numPlayers):
        print(f"Starting blackjack game with {numPlayers - 1} player{'' if numPlayers == 2 else 's'}...\n")
        self.numPlayers = numPlayers
        self.cards = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
        self.suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        self.shoe = self.newShoe()

        self.shoe.append("Ace of Spades")
        self.shoe.append("Three of Diamonds")
        self.shoe.append("Ace of Hearts")

        self.totals = [[0] for i in range(numPlayers)]
        self.hands = [[[]] for i in range(numPlayers)]
        self.cardToNumber = dict()
        self.gameNumber = 1

        for i in range(2, 10):
            self.cardToNumber[self.cards[i-2]] = i
        for i in range(4):
            self.cardToNumber[self.cards[i+8]] = 10
        self.cardToNumber["Ace"] = 11


    # Main method that runs the game
    def play(self):
        while(1):
            self.hands = [[[]] for i in range(self.numPlayers)]
            self.totals = [[0] for i in range(self.numPlayers)]
            self.playRound()
            playAgain = input("Press enter to continue, or 'end' + enter to stop: ")
            print()
            if playAgain == 'end':
                break
            if len(self.shoe) < 60:
                self.shoe = self.newShoe()
            self.gameNumber += 1
            print(f"Starting round {self.gameNumber}...\n")




    

    # Runs a single round of blackjack - handles user input, etc
    def playRound(self):
        self.deal()
        for playerNum in range(1, self.numPlayers):
            handNum = 0
            while handNum < len(self.hands[playerNum]):
                self.playersTurn(playerNum, handNum, True if handNum > 0 else False)
                print()
                handNum += 1
        self.dealersTurn()
        print()
        dealerTotal = self.totals[0][0]
        if dealerTotal == 21:
            print("Dealer wins with blackjack! Everyone loses")
        else:
            for playerIndex in range(1, len(self.totals)):
                for i, total in enumerate(self.totals[playerIndex]):
                    self.printHands(playerIndex, i, True if len(self.totals[playerIndex]) > 1 else False)
                    if total > 21:
                        print("You busted! You lose")
                    elif total == 21:
                        print("You won with blackjack!")
                    elif dealerTotal > 21:
                        print("Dealer busted! You win by default")
                    else:
                        if total > dealerTotal:
                            print("You won by getting closer than the dealer!")
                        else:
                            print("The dealer got closer than you, so you lose")


        
    # Runs a single player's hand
    def playersTurn(self, playerNum, handNum, split):
        self.printHands(playerNum, handNum, split)
        if self.checkTotal(playerNum, handNum):
            return
        if self.checkSplit(playerNum, handNum):
            hitOrStand = self.splitTurn(playerNum, handNum)
            if hitOrStand == 'split':
                self.playersTurn(playerNum, handNum, True)
                return
        else:
            hitOrStand = input("hit or stand: ").lower()
        while True:
            if hitOrStand == 'stand':
                break
            elif hitOrStand == 'hit':
                self.hit(playerNum, handNum)
                self.printHands(playerNum, handNum, split)
            else:
                print('Please type ', end='')
            if self.checkTotal(playerNum, handNum):
                break
            hitOrStand = input("hit or stand: ").lower()
        
        
        
    # splitTurn is called when it is possible to split. It specifically handles the case when the player decides to split.
    def splitTurn(self, playerNum, handNum):
        while True:
            hitStandOrSplit = input("hit, stand, or split: ").lower()
            if hitStandOrSplit == 'split':
                self.hands[playerNum].insert(handNum + 1, [])
                secondCard = self.hands[playerNum][handNum].pop()
                self.hands[playerNum][handNum + 1].append(secondCard)
                self.totals[playerNum].insert(handNum + 1, self.cardToNumber[secondCard[0 : secondCard.index(' ')]])
                self.totals[playerNum][handNum] = self.cardToNumber[secondCard[0 : secondCard.index(' ')]]
                if self.totals[playerNum][handNum] == 11:
                    self.hands[playerNum][handNum][0] = 'Ace' + secondCard[3:]
                self.hit(playerNum, handNum)
                self.hit(playerNum, handNum + 1)
                break
            elif hitStandOrSplit == 'hit' or hitStandOrSplit == 'stand':
                break
            print("Please enter ", end='')
        return hitStandOrSplit


    # Plays the dealer's turn. Dealer never splits, and hits on a total of 16 or less
    def dealersTurn(self):
        self.printHands(0, 0, False)
        while (self.totals[0][0] < 17):
            print("Hit!")
            self.hit(0, 0)
            self.printHands(0, 0, False)
        if not self.checkTotal(0, 0):
            print("Stand")


    # Returns whether or not the two dealt cards are the same (whether or not you are allowed to split)
    def checkSplit(self, playerNum, handNum):
        card1 = self.hands[playerNum][handNum][0]
        card2 = self.hands[playerNum][handNum][1]
        if card1[0 : card1.index(' ')] == 'Ace(1)':
            return True
        card1Value = self.cardToNumber[card1[0 : card1.index(' ')]]
        card2Value = self.cardToNumber[card2[0 : card2.index(' ')]]
        if len(self.hands[playerNum]) < 4 and card1Value == card2Value:
            return True
        return False



    # deals 2 cards to each player (dealer (index 0) gets dealt last)
    def deal(self):
        for i in range(2):
            for player in range(1, self.numPlayers):
                self.hit(player, 0)
            self.hit(0, 0)
        # print one of the dealer's cards so the players can see
        print("Dealer's card shown:", self.hands[0][0][1], '\n')
            
    


    # adds a card to a player
    # playerNum is the player being served
    def hit(self, playerNum, handNum):
        cardAsString = self.shoe.pop()
        self.hands[playerNum][handNum].append(cardAsString)
        self.totals[playerNum][handNum] += self.cardToNumber[cardAsString[0 : cardAsString.index(' ')]]
        # if total exceeds 21, check if there are aces in hand to switch vale to 1
        if self.totals[playerNum][handNum] > 21:
            sum = 0
            for i, card in enumerate(self.hands[playerNum][handNum]):  
                if card[0 : card.index(' ')] == 'Ace':
                    self.hands[playerNum][handNum][i] = 'Ace(1)' + card[card.index(' '):]
                    self.totals[playerNum][handNum] -= 10
                    break
        



    # Returns True if there is a blackjack or a bust (round is over) and false otherwise
    def checkTotal(self, playerNum, handNum):
        if self.totals[playerNum][handNum] == 21:
            print("Blackjack!")
            return True
        elif self.totals[playerNum][handNum] > 21:
            print("Bust! Total: ", self.totals[playerNum][handNum])
            return True
        return False


    # Prints a player's hand to terminal. If no input is given, prints every players hands
    def printHands(self, playerNum, handNum, isSplit):
        numHandOutput = {1 : " first", 2 : " second", 3 : " third", 4 : " fourth"}
        if playerNum is not None and handNum is not None:
            nameFormat = "Dealer" if playerNum == 0 else "Player " + str(playerNum)
            print(f"{nameFormat}'s{numHandOutput[handNum + 1] if isSplit else ''} hand: ", end='')
            for i, card in enumerate(self.hands[playerNum][handNum]):
                if card[0 : card.index(' ')] == 'Ace(1)':
                    card = card[0 : 3] + card[6:]
                if i == len(self.hands[playerNum][handNum]) - 1:
                    print(card)
                else:
                    print(card, ', ', end='')
        else:
            print(f"Dealer's hand:", end='')
            for i, card in enumerate(self.hands[0][0]):
                if card[0 : card.index(' ')] == 'Ace(1)':
                    card = card[0 : 3] + card[6:]
                if i == len(self.hands[0][0]) - 1:
                    print(card)
                else:
                    print(card, ', ', end='')
            for i in range(1, len(self.hands)):
                for hand in self.hands[i]:
                    print(f"Player {i}'s hand {hand + 1}: ", end='')
                    for j, card in enumerate(self.hands[i][hand]):
                        if j == len(self.hands[i]) - 1:
                            print(card)
                        else: print(card, ', ', end='')
    

    
    # Randomly creates a shoe with 5 decks of cards
    def newShoe(self):
        print("Initializing new shoe with 5 decks...\n")
        shoe = []
        for i in range(5):
            for card in self.cards:
                for suit in self.suits:
                    shoe.append(card + " of " + suit)

        shoe.append('Ace of Hearts')
        shoe.append('Nine of diamonds')
        shoe.append('Ace of spades')

        random.shuffle(shoe)
        return shoe


# Main method that runs when file is run - starts a new blackjack game
def main():
    print("\nWelcome to blackjack!\n")
    numPlayers = input("Enter the number of players: ")
    while True:
        try:
            numPlayersInt = int(numPlayers)
            if numPlayersInt > 8:
                numPlayers = input("Maximum of 8 players allowed: ")
            else:
                break
        except Exception:
            numPlayers = input("Please enter a number: ")
    print()
    game = BlackjackGame(int(numPlayers) + 1)
    game.play()

if __name__ == '__main__':
    main()