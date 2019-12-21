import math
import pandas as pd
import matplotlib.pyplot as plt


class backTest():
    def __init__(self, filename):
        self.rawData = pd.read_csv(filename, header=0)
        # self.rawData2 = pd.read_csv(filename,header=0)
        # self.rawDataBTC = pd.read_csv("BTC.csv",header=0)
        # self.rawDataBTC.set_index('timestamp',inplace=True)
        self.rawData['timestamp'] = pd.to_datetime(self.rawData['timestamp'])
        # self.rawData.index = self.rawData['timestamp']
        self.principal = 1000
        self.turnOver = 0
        self.position = 0
        self.positionPrice = 0
        self.revenueThisTime = 0
        self.revenue = 0
        self.revenueFee = 0
        self.revenueFunding = 0
        self.revenuePrice = 0
        self.open = 0
        self.close = 0
        self.high = 0
        self.low = 0
        self.vwap = 0
        self.volum = 0
        self.maxLoss = 0
        self.liquidationPrice = 0
        self.lastTradeTime = 0
        self.timestamp = 0
        self.revenueHistory = []
        self.limitOrder = {}

    def isYear(self, year):
        if year % 4 == 0 & year % 100 != 0:
            return True
        elif year % 400 == 0:
            return True
        else:
            return False

    def cancelOrders(self, price, amount):
        print('')

    def cancelAllOrders(self):
        print('')

    def putMarketOrder(self, amount):
        print('')

    def putLimitOrders(self, price, amount):
        print('')

    def printOrders(self):
        print('')

    def printStatus(self):
        print('')

    def printSummary(self):
        self.printStatus()
        # Win Rate
        # mean,sd of win/loss
        print('')

    def writeToCSV(self):
        print('')

    def getLiquidationPrice(self):
        print('')

    def strategy(self, amount):
        print('')

    def start(self):
        lastFR = 0
        shift = 0
        # median = -0.0158
        # shift = -0.0158 # ETH
        # shift = -0.010001 # BTC
        priceShift = 0.00
        for i in range(0, len(self.rawData)):
            fundingRate = self.rawData.loc[i, 'fundingRate'] + shift
            vwap = self.rawData.loc[i, 'vwap']
            # timestamp2 = self.rawData2.loc[i, 'timestamp']
            timestamp = self.rawData.loc[i, 'timestamp']
            '''
            if fundingRate != lastFR:
                counts = 0
            if abs(fundingRate)>0.2 and counts < 5:
                if counts == 0:
                    print('-----------------------------------------')
                print(
                    self.rawData.loc[i-2+480, 'timestamp'],
                    self.rawData.loc[i-2+480, 'vwap'],
                    fundingRate
                )
                counts +=1
            '''
            # fundingRate = self.rawDataBTC.loc[str(timestamp2),'fundingRate']
            if fundingRate != lastFR:
                self.revenue += abs(self.position * lastFR / 100)
                self.revenueFunding += abs(self.position * lastFR / 100)
                amount = (self.principal + self.revenue) * 0.5
                # amount = self.principal
                if fundingRate < 0 and self.position <= 0:
                    vwap *= (1 - priceShift)
                    if self.position < 0:
                        self.revenueThisTime = self.position * (
                            vwap - self.positionPrice) / vwap
                        if math.isnan(self.revenueThisTime):
                            self.revenueThisTime = 0
                        amountThisTime = amount - self.position
                    elif self.position == 0:
                        self.revenueThisTime = 0
                        amountThisTime = amount
                    self.revenue += self.revenueThisTime
                    self.revenuePrice += self.revenueThisTime
                    fee = abs(amountThisTime) * 0.00025
                    self.revenue += fee
                    self.revenueFee += fee
                    self.revenueHistory.append(self.revenue)
                    self.turnOver += abs(amountThisTime)
                    self.position = 0.5 * amount
                    print(timestamp, "\tRevenue",
                          round(self.revenueThisTime, 2), "(",
                          round((vwap - self.positionPrice) / vwap * -100, 2),
                          "%)\tTotal Revenue:", round(self.revenue, 2), "FR",
                          round(fundingRate, 4), "Position:",
                          round(self.position, 2), "\tBuy ",
                          round(amountThisTime, 2), "\tUSD @", round(vwap, 2))
                    print("RevenuePrice:", round(self.revenuePrice,
                                                 2), "RevenueFee:",
                          round(self.revenueFee, 2), "revenueFunding:",
                          round(self.revenueFunding, 2), "TurnOver:",
                          round(self.turnOver, 2))
                    self.positionPrice = vwap
                elif fundingRate > 0 and self.position >= 0:
                    vwap *= (1 + priceShift)
                    if self.position > 0:
                        self.revenueThisTime = self.position * (
                            vwap - self.positionPrice) / vwap
                        if math.isnan(self.revenueThisTime):
                            self.revenueThisTime = 0
                        amountThisTime = -1 * amount - self.position
                    elif self.position == 0:
                        self.revenueThisTime = 0
                        amountThisTime = -1 * amount
                    self.revenue += self.revenueThisTime
                    self.revenuePrice += self.revenueThisTime
                    fee = abs(amountThisTime) * 0.00025
                    self.revenue += fee
                    self.revenueFee += fee
                    self.revenueHistory.append(self.revenue)
                    self.turnOver += abs(amountThisTime)
                    self.position = -0.5 * amount
                    print(timestamp, "\tRevenue",
                          round(self.revenueThisTime, 2), "(",
                          round((vwap - self.positionPrice) / vwap * 100, 2),
                          "%)\tTotal Revenue:", round(self.revenue, 2), "FR",
                          round(fundingRate, 4), "Position:",
                          round(self.position, 2), "\tSell",
                          round(amountThisTime, 2), "\tUSD @", round(vwap, 2))
                    print("RevenuePrice:", round(self.revenuePrice,
                                                 2), "RevenueFee:",
                          round(self.revenueFee, 2), "revenueFunding:",
                          round(self.revenueFunding, 2), "TurnOver:",
                          round(self.turnOver, 2))
                    self.positionPrice = vwap
                lastFR = fundingRate

        if self.position < 0:
            vwap *= (1 - priceShift)
            revenueThisTime = \
                self.position * (vwap - self.positionPrice) / vwap
            self.revenue += revenueThisTime
            self.revenuePrice += revenueThisTime
            self.revenueHistory.append(self.revenue)
            print(timestamp, "\tRevenue", round(revenueThisTime, 2), "(",
                  round((vwap - self.positionPrice) / vwap * -100, 2),
                  "%)\tTotal Revenue:", round(self.revenue, 2), "FR",
                  round(fundingRate, 4), "Position:", round(self.position,
                                                            2), "\tBuy ",
                  round(amountThisTime, 2), "\tUSD @", round(vwap, 2))
            print("RevenuePrice:", round(self.revenuePrice, 2), "RevenueFee:",
                  round(self.revenueFee, 2), "revenueFunding:",
                  round(self.revenueFunding, 2), "TurnOver:",
                  round(self.turnOver, 2))

        elif self.position > 0:
            vwap *= (1 + priceShift)
            revenueThisTime = \
                self.position * (vwap - self.positionPrice) / vwap
            self.revenue += revenueThisTime
            self.revenuePrice += revenueThisTime
            self.revenueHistory.append(self.revenue)
            print(timestamp, "\tRevenue", round(revenueThisTime, 2), "(",
                  round((vwap - self.positionPrice) / vwap * 100, 2),
                  "%)\tTotal Revenue:", round(self.revenue, 2), "FR",
                  round(fundingRate, 4), "Position:", round(self.position,
                                                            2), "\tSell",
                  round(amountThisTime, 2), "\tUSD @", round(vwap, 2))
            print("RevenuePrice:", round(self.revenuePrice, 2), "RevenueFee:",
                  round(self.revenueFee, 2), "revenueFunding:",
                  round(self.revenueFunding, 2), "TurnOver:",
                  round(self.turnOver, 2))

        # print("RevenuePrice:",self.revenuePrice,"RevenueFee:",self.revenueFee,"RevenueFee:",self.revenueFunding,"TurnOver:",self.turnOver)
        plt.plot(self.revenueHistory)
        # plt.axis([0,15000000,0,6000])
        plt.show()


if __name__ == '__main__':
    # TODO: VWAP=NA?
    test = backTest("BTC.csv")
    test.start()
