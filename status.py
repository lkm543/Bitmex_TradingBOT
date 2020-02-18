class status:
    coin = 'BTC'
    margin = 1
    principal = 1000
    turnOver = 0
    position = 0
    positionPrice = 0
    revenueThisTime = 0
    revenueTotal = 0
    revenueFee = 0
    revenueFunding = 0
    revenuePrice = 0
    volum = 0
    maxLoss = 0
    liquidationPrice = 0
    lastTradeTime = 0

    def __init__(self, coinUsed='BTC', startPrincipal=1000):
        self.coin = coinUsed
        if coinUsed == 'BTC':
            self.margin = 1  # %
        else:
            self.margin = 2  # %
        self.principal = startPrincipal

    def getLiquidationPrice(self):
        print('')
