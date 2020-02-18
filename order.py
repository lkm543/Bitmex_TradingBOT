from status import status
from record import record


class order(status, record):
    '''
        order = {
            'price': ,
            'amount:
        }
    '''
    orderBook = []

    def cancelOrders(self, price, amount):
        self.orderBook = list(
            filter(lambda order: order != {
                'price': price,
                'amount': amount
            }, self.orderBook))

    def cancelAllOrders(self):
        self.orderBook.clear()

    def putMarketOrder(self, amount):
        pass

    def putLimitOrder(self, price, amount):
        order = {'price': price, 'amount': amount}
        self.orderBook.add(order)

    def getOrders(self):
        return self.orderBook
