from status import status


class historyRecord():
    tradeHistory = []

    def addRecord(self):
        pass

    def writeToCSV(self):
        pass


class record(status):
    coin = 'BTC'
    amount = 0
    price = 0
    orderType = 'Market'  # Market or Limit
    time = 0
    revenueThisTime = 0
    revenueFee = 0
    revenueFunding = 0
    revenuePrice = 0
