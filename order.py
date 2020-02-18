from record import historyRecord


class order(historyRecord):
    '''
        orderBook = {
            'price': amount:
        }
    '''
    marketFee = 0.00075
    limitFee = -0.00025
    orderBook = dict()
    print_Order = True

    def removeOrder(self, price):
        self.orderBook.pop(price, None)

    def cancelAllOrders(self):
        self.orderBook = dict()

    def putMarketOrder(self, amount, price=0):
        if price == 0:
            price = self.vwap
        if self.print_Order:
            self.calculteExecution(price, amount, 'Market')
            print(f"{self.timestamp}:Market executed @{price} for ${amount}"
                  f", Capital: {self.capital}")

    def putLimitOrder(self, price, amount):
        self.orderBook[price] = amount

    def executeLimitOrder(self):
        # o > c
        # o -> h -> l -> c
        if self.open > self.close:
            self.executeRangeLimit(self.open, self.high)
            self.executeRangeLimit(self.high, self.low)
            self.executeRangeLimit(self.low, self.close)
        # o < c
        # o -> l -> h -> c
        else:
            self.executeRangeLimit(self.open, self.low)
            self.executeRangeLimit(self.low, self.high)
            self.executeRangeLimit(self.high, self.close)

    def executeRangeLimit(self, fromPrice, toPrice):
        orderPrices = self.orderBook.keys()
        for orderPrice in orderPrices:
            if fromPrice < orderPrice < toPrice:
                executeAmount = self.orderBook[orderPrice]
                self.calculteExecution(orderPrice, executeAmount, 'Limit')
                print(f"Limit executed @{orderPrice} for ${executeAmount}"
                      f", Capital: {self.capital}")
                self.removeOrder(orderPrice)

    def calculteExecution(self, price, amount, orderType):
        if orderType == 'Market':
            self.revenueFee += -1 * amount * self.marketFee
        elif orderType == 'Limit':
            self.revenueFee += -1 * amount * self.limitFee

        if amount == 0:
            self.revenuePrice = 0
        # 第一次開倉
        elif self.position == 0:
            self.position = amount
            self.positionPrice = price
            self.revenuePrice = 0
        # 加倉
        elif amount * self.position > 0:
            self.revenuePrice = 0
            self.positionPrice = \
                (price * amount + self.positionPrice * self.position) \
                / (amount + self.position)
            self.position += amount
        elif amount * self.position < 0:
            # 反倉
            if abs(amount) > abs(self.position):
                self.revenuePrice = \
                    self.position * (price - self.positionPrice) \
                    / self.positionPrice
                self.positionPrice = price
            # 減倉
            else:
                self.revenuePrice = \
                    amount * (price - self.positionPrice) / self.positionPrice
            self.position += amount

        self.revenueFunding = 0
        self.revenueThisTime = self.revenuePrice + self.revenueFee
        self.revenueTotal += self.revenueThisTime
        self.capital += self.revenueThisTime
        self.amount = amount
        self.price = price
        self.orderType = orderType
        self.turnOver += abs(amount)
        self.lastTradeTime = self.timestamp

    def getOrders(self):
        return self.orderBook
