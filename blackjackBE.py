import random
import agent
# This class will interact with agent.py to automate the playing process.
# Everything will be run through methods called back and forth between this and 
# the agent. Anything output to the terminal would be to track progress/debug, etc.

class BlackjackGame:

    
    # Initializes the data structures needed
    # shoe holds 4 decks worth of the String representation of a card (e.g. "Eight of Spades")
    # cardToNumber is a dictionary that pairs the string card value with the blackjack value (e.g. "Queen" -> 10)
    # totals and hands hold the values and the respective hands of all the players, including the house. The house is always index 0
    # totals and hands are multi-dimensional arrays that are as follows: [player number][hand number (in case of splits)][hand/total]
    # winLoseOrTie holds 0 for a loss, 1 for a win, and 2 for a tie for each hand to pass to the agent. It is cleared after each round
    def __init__(self, numPlayers, startingMoney, agentInstance):
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
        self.dealersCardValue = 2
        self.count = 0
        self.winLoseOrTie = []
        self.getCountOfCard = {2 : 1, 3 : 1, 4 : 1, 5 : 1, 6 : 1, 7 : 0, 8 : 0, 9 : 0, 10 : -1, 11 : -1}
        self.gerald = agentInstance
        self.payoutHistory = []

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
            # print("\n\nwinLoseOrTie: ", self.winLoseOrTie, "\n\n")
            playAgain = self.gerald.playAgain(self.gameNumber, self.winLoseOrTie, self.playersMoney[0])
            self.winLoseOrTie.clear()
            # print()
            if playAgain == 'end':
                break
            if len(self.shoe) < 10:
                self.shoe = self.newShoe()
            self.gameNumber += 1
            # print(f"Starting round {self.gameNumber}...\n")

    

    # Runs a single round of blackjack - handles user input, etc
    def playRound(self):
        self.collectBets()
        dealerWon = self.deal()
        if dealerWon:
            hasBlackjack = False
            self.winLoseOrTie.append(0)
            # self.printHands(0, 0, False)
            for i in range(self.numPlayers - 1):
                # self.printHands(i + 1, 0, False)
                if self.totals[i + 1][0] == 21:
                    hasBlackjack = True
                    # print("Player ", i + 1, "also has blackjack. You keep your bet")
                    self.winLoseOrTie.append(2)
                    self.playersMoney[i] += self.roundBets[i][0]
            # print()
            if hasBlackjack:
                # print("Payout: -", self.roundBets[0][0])
                self.payoutHistory.append(-self.roundBets[0][0])
            return
        for playerNum in range(1, self.numPlayers):
            handNum = 0
            while handNum < len(self.hands[playerNum]):
                self.playersTurn(playerNum, handNum, True if handNum > 0 else False)
                # print()
                handNum += 1
        self.dealersTurn()
        # print()
        dealerTotal = self.totals[0][0]
        for playerIndex in range(1, len(self.totals)):
            for i, total in enumerate(self.totals[playerIndex]):
                # self.printHands(playerIndex, i, True if len(self.totals[playerIndex]) > 1 else False)
                if total > 21:
                    # print("You busted! You lose")
                    # print("Payout: -", self.roundBets[playerIndex - 1][i])
                    self.payoutHistory.append(-self.roundBets[playerIndex - 1][i])
                    self.winLoseOrTie.append(0)
                elif total == 21 and len(self.hands[playerIndex][i]) == 2:
                    # print("You won with natural blackjack! Payout:", int(self.roundBets[playerIndex - 1][i] * 2.5))
                    # print("Payout: ", int(self.roundBets[playerIndex - 1][i] * 2.5))
                    self.payoutHistory.append(int(self.roundBets[playerIndex - 1][i] * 2.5))
                    self.winLoseOrTie.append(1)
                    self.playersMoney[playerIndex - 1] += int(self.roundBets[playerIndex - 1][i] * 1.5)
                elif dealerTotal > 21:
                    # print("Dealer busted! You win. Payout:", self.roundBets[playerIndex - 1][i])
                    # print("Payout: ", self.roundBets[playerIndex - 1][i])
                    self.payoutHistory.append(self.roundBets[playerIndex - 1][i])
                    self.winLoseOrTie.append(1)
                    self.playersMoney[playerIndex - 1] += 2 * self.roundBets[playerIndex - 1][i]
                else:
                    if total > dealerTotal:
                        # print("You won by getting closer than the dealer! Payout:", self.roundBets[playerIndex - 1][i])
                        # print("Payout: ", self.roundBets[playerIndex - 1][i])
                        self.payoutHistory.append(self.roundBets[playerIndex - 1][i])
                        self.winLoseOrTie.append(1)
                        self.playersMoney[playerIndex - 1] += 2 * self.roundBets[playerIndex - 1][i]
                    elif dealerTotal > total:
                        # print("The dealer got closer than you, so you lose")
                        # print("Payout: -", self.roundBets[playerIndex - 1][i])
                        self.payoutHistory.append(-self.roundBets[playerIndex - 1][i])
                        self.winLoseOrTie.append(0)
                    else:
                        # print("You tied the dealer, so you keep your bet")
                        self.winLoseOrTie.append(2)
                        self.playersMoney[playerIndex - 1] += self.roundBets[playerIndex - 1][i]
        for i in range(self.numPlayers - 1):
            self.roundBets[i].clear()


        
    # Runs a single player's hand
    def playersTurn(self, playerNum, handNum, split):
        # self.printHands(playerNum, handNum, split)
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
                hitOrStand = self.gerald.hitStandOrDD(self.hands[playerNum][handNum], self.totals[playerNum][handNum], self.dealersCardValue)
                if hitOrStand == 'dd':
                    if self.roundBets[playerNum - 1][handNum] > self.playersMoney[playerNum - 1]:
                        raise Exception("Insufficient funds to double down")
                    else:
                        self.doubleDown(playerNum, handNum)
                        return
                elif hitOrStand != 'stand' and hitOrStand != 'hit':
                    raise Exception("Did not return a valid string")
                else:
                    break
        else:
            hitOrStand = self.gerald.hitOrStand(self.hands[playerNum][handNum], self.totals[playerNum][handNum], self.dealersCardValue)
        while True:
            if hitOrStand == 'stand':
                break
            elif hitOrStand == 'hit':
                self.hit(playerNum, handNum)
                # self.printHands(playerNum, handNum, split)
            else:
                print('Please type ', end='')
            if self.checkTotal(playerNum, handNum):
                break
            hitOrStand = self.gerald.hitOrStand(self.hands[playerNum][handNum], self.totals[playerNum][handNum], self.dealersCardValue)
    


    def collectBets(self):
        if self.playersMoney[0] < 10:
            raise Exception("Agent ran out of funds :(")
        self.collectBet(1)



    def collectBet(self, playerNum):
        bet = self.gerald.collectBet(self.playersMoney[0], self.getTrueCount())
        # while True:
        #     try:
        #         bet = int(inputBet)
        #         if bet < 10:
        #             inputBet = ("You must bet at least $10: ")
        #         elif bet > self.playersMoney[playerNum - 1]:
        #             inputBet = input(f"You only have {self.playersMoney[playerNum - 1]} dollars: ")
        #         else:
        #             break
        #     except Exception:
        #         inputBet = input("Please enter a digit: ")
        self.roundBets[playerNum - 1].append(bet)
        self.playersMoney[playerNum - 1] -= bet
        # print()
        

    # Performs the double down operation on a hand (adds exactly one card and doubles the bet)
    def doubleDown(self, playerNum, handNum):
        self.playersMoney[playerNum - 1] -= self.roundBets[playerNum - 1][handNum]
        self.roundBets[playerNum - 1][handNum] *= 2
        # print("Giving you one more card and doubling your bet")
        self.hit(playerNum, handNum)
        # self.printHands(playerNum, handNum, True if handNum > 0 else False)
        if not self.checkTotal(playerNum, handNum):
            # print("Total:", self.totals[playerNum][handNum])
            pass
        
        
        
    # splitTurn is called when it is possible to split. It specifically handles the case when the player decides to split.
    def splitTurn(self, playerNum, handNum):
        while True:
            hitStandSplitOrDD = self.gerald.hitStandSplitOrDD(self.hands[playerNum][handNum], self.totals[playerNum][handNum], self.dealersCardValue)
            if hitStandSplitOrDD == 'dd':
                if (self.roundBets[playerNum - 1][handNum] > self.playersMoney[playerNum - 1]):
                    raise Exception("You cannot split or double down because you have insufficient funds")
                    # print("You cannot split or double down because you have insufficient funds")
                    # return 'illegal'
                self.doubleDown(playerNum, handNum)
                break
            if hitStandSplitOrDD == 'split':
                if self.roundBets[playerNum - 1][handNum] > self.playersMoney[playerNum - 1]:
                    raise Exception("You cannot split or double down because you have insufficient funds")
                    # print("You cannot split or double down because you have insufficient funds")
                    # return 'illegal'
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
            elif hitStandSplitOrDD == 'hit' or hitStandSplitOrDD == 'stand':
                break
            raise Exception("Did not return a valid string: 'split', 'dd', 'hit', or 'stand'")
            # print("Please enter ", end='')
        return hitStandSplitOrDD



    # Plays the dealer's turn. Dealer never splits, and hits on a total of 16 or less
    def dealersTurn(self):
        # self.printHands(0, 0, False)
        while (self.totals[0][0] < 17):
            # print("Hit!")
            self.hit(0, 0)
            # self.printHands(0, 0, False)
        if not self.checkTotal(0, 0):
            pass
            # print("Stand")



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
        self.dealersCardValue = self.cardToNumber[self.hands[0][0][1][0 : self.hands[0][0][1].index(' ')]]
        # print("Dealer's up card:", self.hands[0][0][1], '\n')
        # If the dealer has a natural blackjack, no one plays their turn
        if self.totals[0][0] == 21:
            # print("Dealer wins with blackjack\n")
            return True
        return False
    


    # adds a card to a player
    # playerNum is the player being served
    def hit(self, playerNum, handNum):
        if len(self.shoe) < 10:
            self.shoe = self.newShoe()
        try:
            cardAsString = self.shoe.pop()
        except IndexError:
            print("Caught index error")
            self.shoe = self.newShoe()
            cardAsString = self.shoe.pop()
        self.hands[playerNum][handNum].append(cardAsString)
        cardNum = self.cardToNumber[cardAsString[0 : cardAsString.index(' ')]]
        self.totals[playerNum][handNum] += cardNum
        self.count += self.getCountOfCard[cardNum]
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
            # print("Blackjack!")
            return True
        elif self.totals[playerNum][handNum] > 21:
            # print("Bust! Total card values: ", self.totals[playerNum][handNum])
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
        # print("Initializing new shoe with 5 decks...\n")
        self.count = 0
        shoe = []
        for i in range(5):
            for card in self.cards:
                for suit in self.suits:
                    shoe.append(card + " of " + suit)
        random.shuffle(shoe)
        return shoe
    

    # Returns the true count of the game
    def getTrueCount(self):
        return self.count / (len(self.shoe) / 52)
    
    
    def getPayoutHistory(self):
        return self.payoutHistory