from kBar import kBar


class status(kBar):
    coin = 'BTC'
    margin = 0.5
    principal = 1000
    turnOver = 0
    position = 0
    positionPrice = 0
    revenueTotal = 0
    volum = 0
    maxLoss = 0
    liquidationPrice = 0
    lastTradeTime = 0

    def __init__(self, coinUsed='BTC', startPrincipal=1000):
        self.coin = coinUsed
        if coinUsed == 'BTC':
            self.margin = 0.5  # %
        else:
            self.margin = 1  # %
        self.principal = startPrincipal

    # Ref:https://kknews.cc/zh-tw/finance/e4ka5ay.html
    # 维持保证金=仓位*开仓价格*2.5%=100000*0.000012*2.5%=0.03
    # 保证金余额=钱包余额-维持保证金=1-0.03=0.97
    # 假设强平价格为X，100000*（0.000012-X）=0.97，X=0.0000023
    def getLiquidationPrice(self):
        maintainMargin = self.principal \
            - self.margin * self.position / 100
        liquidationPrice = self.positionPrice \
            * (1 - maintainMargin / self.position)
        return liquidationPrice

    def unrealisedPNL(self, price):
        uPNL = (price - self.positionPrice) * self.position
        uPNL /= self.positionPrice
        return uPNL

    def calculateFunding(self):
        '''
        if fundingRate != lastFR:
            self.revenueTotal += abs(self.position * lastFR / 100)
            self.revenueFunding += abs(self.position * lastFR / 100)
            amount = (self.principal + self.revenueTotal) * 0.5
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
                self.revenueTotal += self.revenueThisTime
                self.revenuePrice += self.revenueThisTime
                fee = abs(amountThisTime) * 0.00025
                self.revenueTotal += fee
                self.revenueFee += fee
                self.revenueHistory.append(self.revenueTotal)
                self.turnOver += abs(amountThisTime)
                self.position = 0.5 * amount
                print(timestamp, "\tRevenue",
                        round(self.revenueThisTime, 2), "(",
                        round((vwap - self.positionPrice) / vwap * -100,
                            2), "%)\tTotal Revenue:",
                        round(self.revenueTotal, 2), "FR",
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
                self.revenueTotal += self.revenueThisTime
                self.revenuePrice += self.revenueThisTime
                fee = abs(amountThisTime) * 0.00025
                self.revenueTotal += fee
                self.revenueFee += fee
                self.revenueHistory.append(self.revenueTotal)
                self.turnOver += abs(amountThisTime)
                self.position = -0.5 * amount
                print(timestamp, "\tRevenue",
                        round(self.revenueThisTime, 2), "(",
                        round((vwap - self.positionPrice) / vwap * 100,
                            2), "%)\tTotal Revenue:",
                        round(self.revenueTotal, 2), "FR",
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
        '''
        pass

        def checkLiquidation(self, kBar):
            # liquidationPrice = self.getLiquidationPrice()
            pass

        def printStatus(self):
            pass


if __name__ == "__main__":
    Test = status()
    Test.capital = 1000
    Test.position = 10000
    Test.positionPrice = 10000
    print(Test.getLiquidationPrice())
    print(Test.unrealisedPNL(10500))
