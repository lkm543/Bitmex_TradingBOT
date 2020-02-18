import pandas as pd
from order import order
from crawlData import histData
from kBar import kBar


class backTest(order, kBar):
    liquidation = 0
    timestamp = ""
    fundingRate = 0

    def __init__(self, filename):
        self.rawData = pd.read_csv(filename, header=0)
        self.rawData['timestamp'] = pd.to_datetime(self.rawData['timestamp'])

    def strategy(self):
        if self.position < 0:
            self.putMarketOrder(self.vwap, self.capital * 2)
        else:
            self.putMarketOrder(self.vwap, self.capital * -2)

    def start(self):
        for i in range(0, len(self.rawData)):
            # Step 0: Get k bar this minute
            self.fundingRate = self.rawData.loc[i, 'fundingRate']
            self.open = self.rawData.loc[i, 'open']
            self.close = self.rawData.loc[i, 'close']
            self.high = self.rawData.loc[i, 'high']
            self.low = self.rawData.loc[i, 'low']
            self.vwap = self.rawData.loc[i, 'vwap']
            self.volume = self.rawData.loc[i, 'volume']
            self.timestamp = self.rawData.loc[i, 'timestamp']

            # Step 1: Calculate funding
            if False:
                self.calculateFunding()

            # Step 2: Check liquidation or not
            self.liquidation = self.checkLiquidation()
            if self.liquidation:
                break

            # Step 2: Execute limit order
            self.executeLimitOrder()

            # Step 4: Execute trading strategy
            self.strategy()
        if self.liquidation:
            print("Your strategy was liquidated.")
            print("The result of your strategy is:")
            self.printStatus()


if __name__ == '__main__':
    # TODO: VWAP=NA?
    history = histData()
    history.complement("BTC", "BTC.csv")
    # history.complement("ETH", "ETH.csv")

    test = backTest("BTC.csv")
    test.start()
