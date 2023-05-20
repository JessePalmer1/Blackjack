# This class automates the playing process

from collections import Counter
import blackjackBE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class agent:

    def __init__(self):
        self.winLoseOrTieLS = []
        self.startingFunds = 1000000
        self.netFunds = 0
        self.gameNum = 1
        self.numGames = 1000000
        self.splitInfo = []
        self.ddInfo = []
        self.countHistory = []
        self.winLoseOrTieToStr = dict()
        self.winLoseOrTieToStr[0] = 'loss'
        self.winLoseOrTieToStr[1] = 'win'
        self.winLoseOrTieToStr[2] = 'tie'
        self.fundsOverTime = []


    def hitOrStand(self, hand, total, dealersCard):
        # print("My hand at the moment is: ", hand)
        if total >= 17:
            return 'stand'
        elif total == 16 or total == 15 or total == 14 or total == 13:
            return 'stand' if dealersCard <= 6 else 'hit'
        elif total == 12 or total == 11:
            return 'stand' if dealersCard >= 4 and dealersCard <= 6 else 'hit'
        else:
            return 'hit'
        
        
    def hitStandSplitOrDD(self, hand, total, dealersCard):
        # print("My hand at the moment is: ", hand)
        if hand[0][0 : hand[0].index(' ')] == 'Ace' or total == 16:
            self.splitInfo.append(self.gameNum)
            return 'split'
        elif total == 18:
            return 'split' if dealersCard <= 9 and dealersCard != 7 else 'stand'
        elif total == 14 or total == 6 or total == 4:
            return 'split' if dealersCard <= 7 else 'hit'
        elif total == 12:
            return 'split' if dealersCard <= 6 else 'hit'
        elif total == 10:
            return 'split' if dealersCard <= 9 else 'hit'
        elif total == 4:
            return 'split' if dealersCard == 5 or dealersCard == 6 else 'hit'
        else:
            return self.hitStandOrDD(hand, total, dealersCard)
        

    def hitStandOrDD(self, hand, total, dealersCard):
        # print("My hand at the moment is: ", hand)
        if total == 11:
            self.ddInfo.append(self.gameNum)
            return 'dd'
        elif total == 10:
            return 'dd' if dealersCard <= 9 else 'hit'
        elif total == 9:
            return 'dd' if dealersCard <= 6 and dealersCard >= 3 else 'hit'
        else:
            return self.hitOrStand(hand, total, dealersCard)
        

    def playAgain(self, gameNumber, winLoseOrTie, funds):
        self.netFunds = funds
        if gameNumber % 1000 == 0:
            self.fundsOverTime.append(self.netFunds)
        if gameNumber % 100000 == 0:
            print("Game number " , gameNumber)
        self.gameNum += 1
        for num in winLoseOrTie:
            # print(self.winLoseOrTieToStr[num])
            self.winLoseOrTieLS.append(num)
        return 'end' if gameNumber >= self.numGames else 'continue'

        
    def collectBet(self, funds, trueCount):
        # print("My total funds is ", funds, ". Betting 10")
        # print(int(trueCount))
        self.countHistory.append(int(trueCount))
        count = int(trueCount)
        if count < 5:
            return 1
        else:
            return int((count ** 3))


def main():
    gerald = agent()
    game = blackjackBE.BlackjackGame(2, gerald.startingFunds, gerald)
    game.play()
    numWins = gerald.winLoseOrTieLS.count(1)
    numLosses = gerald.winLoseOrTieLS.count(0)
    numTies = gerald.winLoseOrTieLS.count(2)
    print("Games played: ", gerald.numGames)
    print(f"\n\nTotal wins: {numWins}. Total Losses: {numLosses}. Total Ties: {numTies}. Total funds: {gerald.netFunds}\n")
    print(f"Win percentage: {round(numWins / gerald.numGames * 100, 3)}%. \
            Profit percentage: {round((gerald.netFunds - gerald.startingFunds) / gerald.startingFunds * 100, 3)}%\n")
    print("\nnumber of splits: ", len(gerald.splitInfo), "\n")
    print("\nnumber of double downs: ", len(gerald.ddInfo), "\n")
    print()
    payoutHistory = game.getPayoutHistory()
    print("Len of payout history: ", len(payoutHistory), "\n")
    payHistAsDict = Counter(payoutHistory)
    sortedPayHistAsDict = dict(sorted(payHistAsDict.items()))
    print("Payout History:\n", sortedPayHistAsDict)
    print()
    cntHistory = gerald.countHistory
    print("Len of count history: ", len(cntHistory))
    cntHistAsDict = Counter(cntHistory)
    sortedCntHistAsDict = dict(sorted(cntHistAsDict.items()))
    print("Count history: \n", sortedCntHistAsDict)

    

    # Convert dictionary to pandas DataFrame
    # df = pd.DataFrame(list(sortedPayHistAsDict.items()), columns=['Key', 'Value'])
    # dfCount = pd.DataFrame(list(sortedCntHistAsDict.items()), columns=['Key', 'Value'])
    fundsLinePlot = pd.Series(gerald.fundsOverTime)

    # Plot the DataFrame
    # df.plot(x='Key', y='Value', kind='bar')
    # dfCount.plot(x='Key', y='Value', kind='bar')
    fundsLinePlot.plot(kind='line')


    # Show the plot
    plt.show()

    # # Visualize the count and the payout history
    # series = pd.Series(payoutHistory)
    # plt.hist(series.values, bins=np.arange(min(series.values), max(series.values) + 1.5) - 0.5, edgecolor='black')
    # plt.xlabel('Values')
    # plt.ylabel('Frequency')
    # plt.title('Histogram')
    # plt.show()

    # plt.hist(payoutHistory, bins=np.arange(min(payoutHistory), max(payoutHistory) + 1.5) - 0.5, edgecolor='black')
    # plt.xlabel('Values')
    # plt.ylabel('Frequency')

    # plt.hist(cntHistory, bins=np.arange(min(cntHistory), max(cntHistory) + 1.5) - 0.5, edgecolor='black')
    # plt.xlabel('Values')
    # plt.ylabel('Frequency')
    
    # print("Showing plot:")
    # plt.show()  





if __name__ == '__main__':
    main()

