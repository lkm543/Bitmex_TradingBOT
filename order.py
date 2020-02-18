from record import historyRecord


class order(historyRecord):
    '''
        order = {
            'price': ,
            'amount:
        }
    '''
    marketFee = 0.00075  # %
    limitFee = -0.00025  # %
    orderBook = []
    print_Order = True

    def cancelOrders(self, price, amount):
        self.orderBook = list(
            filter(lambda order: order != {
                'price': price,
                'amount': amount
            }, self.orderBook))

    def cancelAllOrders(self):
        self.orderBook.clear()

    def putMarketOrder(self, amount, price=0):
        if price == 0:
            price = self.vwap
        '''
        if self.position < 0:
            vwap *= (1 - priceShift)
            revenueThisTime = \
                self.position * (vwap - self.positionPrice) / vwap
            self.revenueTotal += revenueThisTime
            self.revenuePrice += revenueThisTime
            self.revenueHistory.append(self.revenueTotal)
            print(timestamp, "\tRevenue", round(revenueThisTime, 2), "(",
                  round((vwap - self.positionPrice) / vwap * -100, 2),
                  "%)\tTotal Revenue:", round(self.revenueTotal, 2), "FR",
                  round(fundingRate, 4), "Position:", round(self.position,
                                                            2), "\tBuy ",
                  round(amountThisTime, 2), "\tUSD @", round(vwap, 2))
            print("RevenuePrice:", round(self.revenuePrice, 2), "RevenueFee:",
                  round(self.revenueFee, 2), "revenueFunding:",
                  round(self.revenueFunding, 2), "TurnOver:",
                  round(self.turnOver, 2))
        '''
    def putLimitOrder(self, price, amount):
        order = {'price': price, 'amount': amount}
        self.orderBook.add(order)

    def executeLimitOrder(self):
        # o > c
        # o -> h -> l -> c
        if self.open > self.close:
            pass
        # o < c
        # o -> l -> h -> c
        else:
            pass

    def getOrders(self):
        return self.orderBook
