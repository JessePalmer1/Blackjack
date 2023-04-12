import random

class BlackjackGame:
    
    # Initializes the data structures needed
    # shoe holds 4 decks worth of the String representation of a card (e.g. "Eight of Spades")
    # cardToNumber is a dictionary that pairs the string card value with the blackjack value (e.g. "Queen" -> 10)
    # totals and hands hold the values and the respective hands of all the players, including the house. The house is always index 0
    # totals and hands are multi-dimensional arrays that are as follows: [player number][hand number (in case of splits)][hand/total]
    def __init__(self, numPlayers, startingMoney):
        print(f"Starting blackjack game with {numPlayers - 1} player{'' if numPlayers == 2 else 's'}...\n")
        self.numPlayers = numPlayers
        self.cards = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
        self.suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        self.shoe = self.newShoe()
        self.totals = [[0] for i in range(numPlayers)]
        self.hands = [[[]] for i in range(numPlayers)]
        self.playersMoney = [startingMoney for i in range(numPlayers - 1)]
        self.roundBets = [[] for i in range(numPlayers - 1)]
        self.cardToNumber = dict()
        self.gameNumber = 1

        # self.shoe.append("Ace of Spades")
        # self.shoe.append("King of Diamonds")
        # self.shoe.append("King of hearts")
        # self.shoe.append("Ace of Hearts")

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
        self.collectBets()
        dealerWon = self.deal()
        if dealerWon:
            self.printHands(0, 0, False)
            for i in range(self.numPlayers - 1):
                self.printHands(i + 1, 0, False)
                if self.totals[i + 1][0] == 21:
                    print("Player ", i + 1, "also has blackjack. You keep your bet")
                    self.playersMoney[i] += self.roundBets[i][0]
            print()
            return
        for playerNum in range(1, self.numPlayers):
            handNum = 0
            while handNum < len(self.hands[playerNum]):
                self.playersTurn(playerNum, handNum, True if handNum > 0 else False)
                print()
                handNum += 1
        self.dealersTurn()
        print()
        dealerTotal = self.totals[0][0]
        for playerIndex in range(1, len(self.totals)):
            for i, total in enumerate(self.totals[playerIndex]):
                self.printHands(playerIndex, i, True if len(self.totals[playerIndex]) > 1 else False)
                if total > 21:
                    print("You busted! You lose")
                elif total == 21 and len(self.hands[playerIndex][i]) == 2:
                    print("You won with natural blackjack! Payout:", int(self.roundBets[playerIndex - 1][i] * 2.5))
                    self.playersMoney[playerIndex - 1] += int(self.roundBets[playerIndex - 1][i] * 1.5)
                elif dealerTotal > 21:
                    print("Dealer busted! You win. Payout:", self.roundBets[playerIndex - 1][i])
                    self.playersMoney[playerIndex - 1] += 2 * self.roundBets[playerIndex - 1][i]
                else:
                    if total > dealerTotal:
                        print("You won by getting closer than the dealer! Payout:", self.roundBets[playerIndex - 1][i])
                        self.playersMoney[playerIndex - 1] += 2 * self.roundBets[playerIndex - 1][i]
                    elif dealerTotal > total:
                        print("The dealer got closer than you, so you lose")
                    else:
                        print("You tied the dealer, so you keep your bet")
                        self.playersMoney[playerIndex - 1] += self.roundBets[playerIndex - 1][i]
        for i in range(self.numPlayers - 1):
            self.roundBets[i].clear()


        
    # Runs a single player's hand
    def playersTurn(self, playerNum, handNum, split):
        self.printHands(playerNum, handNum, split)
        if self.checkTotal(playerNum, handNum):
            return
        if self.checkSplit(playerNum, handNum):
            hitOrStand = self.splitTurn(playerNum, handNum)
            if hitOrStand == 'dd':
                return
            if hitOrStand == 'split':
                self.playersTurn(playerNum, handNum, True)
                return
        # Provides the option to double down when applicable
        elif len(self.hands[playerNum][handNum]) == 2:
            while True:
                hitOrStand = input("hit, stand, or double down (dd): ").lower()
                if hitOrStand == 'dd':
                    if self.roundBets[playerNum - 1][handNum] > self.playersMoney[playerNum - 1]:
                        print("You cannot double down because you have insufficient funds")
                    else:
                        self.doubleDown(playerNum, handNum)
                        return
                elif hitOrStand != 'stand' and hitOrStand != 'hit':
                    print('Please type ', end='')
                else:
                    break
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
    


    def collectBets(self):
        for i in range(self.numPlayers - 1):
            if self.playersMoney[i] < 10:
                print(f"Player {i + 1} does not have sufficient funds to bet\n")
                self.roundBets[i] = 0
                continue
            self.collectBet(i + 1)



    def collectBet(self, playerNum):
        inputBet = ''
        inputBet = input(f"Player {playerNum} place your bet (total funds: {self.playersMoney[playerNum - 1]}): ")
        while True:
            try:
                bet = int(inputBet)
                if bet < 10:
                    inputBet = input("You must bet at least $10: ")
                elif bet > self.playersMoney[playerNum - 1]:
                    inputBet = input(f"You only have {self.playersMoney[playerNum - 1]} dollars: ")
                else:
                    break
            except Exception:
                inputBet = input("Please enter a digit: ")
        self.roundBets[playerNum - 1].append(bet)
        self.playersMoney[playerNum - 1] -= bet
        print()
        

    # Performs the double down operation on a hand (adds exactly one card and doubles the bet)
    def doubleDown(self, playerNum, handNum):
        self.playersMoney[playerNum - 1] -= self.roundBets[playerNum - 1][handNum]
        self.roundBets[playerNum - 1][handNum] *= 2
        print("Giving you one more card and doubling your bet")
        self.hit(playerNum, handNum)
        self.printHands(playerNum, handNum, True if handNum > 0 else False)
        if not self.checkTotal(playerNum, handNum):
            print("Total:", self.totals[playerNum][handNum])
        
        
        
    # splitTurn is called when it is possible to split. It specifically handles the case when the player decides to split.
    def splitTurn(self, playerNum, handNum):
        while True:
            hitStandOrSplit = input("hit, stand, split, or double down (dd): ").lower()
            if hitStandOrSplit == 'dd':
                if (self.roundBets[playerNum - 1][handNum] > self.playersMoney[playerNum - 1]):
                    print("You cannot split or double down because you have insufficient funds")
                    return 'illegal'
                self.doubleDown(playerNum, handNum)
                break
            if hitStandOrSplit == 'split':
                if self.roundBets[playerNum - 1][handNum] > self.playersMoney[playerNum - 1]:
                    print("You cannot split or double down because you have insufficient funds")
                    return 'illegal'
                self.roundBets[playerNum - 1].append(self.roundBets[playerNum - 1][0])
                self.playersMoney[playerNum - 1] -= self.roundBets[playerNum - 1][0]
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
        # Print one of the dealer's cards so the players can see
        print("Dealer's up card:", self.hands[0][0][1], '\n')
        # If the dealer has a natural blackjack, no one plays their turn
        if self.totals[0][0] == 21:
            print("Dealer wins with blackjack\n")
            return True
        return False
    


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
            print("Bust! Total card values: ", self.totals[playerNum][handNum])
            return True
        return False



    # Prints a player's hand to terminal. If no input is given, prints every players hands
    def printHands(self, playerNum, handNum, isSplit):
        numHandOutput = {1 : "first", 2 : "second", 3 : "third", 4 : "fourth"}
        if playerNum is not None and handNum is not None:
            nameFormat = "Dealer" if playerNum == 0 else "Player " + str(playerNum)
            print(f"{nameFormat}'s {numHandOutput[handNum + 1] if isSplit else ''} hand: ", end='')
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
    startingMoney = input("Enter the starting amount of money you wish to have: ")
    while True:
        try:
            startingMoneyInt = int(startingMoney)
            if startingMoneyInt < 100:
                startingMoney = input("You must start with at least $100: ")
            else:
                break
        except Exception:
            startingMoney = input("Please enter a digit: ")
    print()
    game = BlackjackGame(numPlayersInt + 1, startingMoneyInt)
    game.play()

if __name__ == '__main__':
    main()