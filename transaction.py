from datetime import date, timedelta
from API import API
from ArgParser import ArgParser
import shioaji as sj

def getClose(api, stockId, date):
    ticks = api.ticks(contract=api.Contracts.Stocks[stockId], date=date.strftime("%Y-%m-%d"))
    if len(ticks.close) == 0:
        print("%s: None" % (date.strftime("%Y-%m-%d")))
        return None

    print("%s: %.1f" % (date.strftime("%Y-%m-%d"), ticks.close[-1]))
    return ticks.close[-1]

def dateRange(fromDate, toDate):
    days = (toDate - fromDate).days + 1
    return [fromDate + timedelta(days=i) for i in range(days)]

def compute_average_price(api, stockId, fromDate, toDate):
    closes = [getClose(api, stockId, date) for date in dateRange(fromDate, toDate)]
    closes = list(filter(lambda close: close is not None, closes))
    return sum(closes) / len(closes)

def compute_price(api, stockId, date):
    return getClose(api, stockId, date)

def place_order(api, stockId, price, quantity, action):
    contract = getattr(
        api.Contracts.Stocks.TSE,
        "TSE" + stockId
    )

    order = api.Order(
        price=price,
        quantity=quantity,
        action=action,
        price_type=sj.constant.StockPriceType.LMT,
        order_type=sj.constant.OrderType.ROD,
        order_lot=sj.constant.StockOrderLot.Common,
        daytrade_short=False,
        account=api.stock_account
    )

    trade = api.place_order(contract, order)
    return trade

def buy(api, stockId, price, quantity):
    place_order(api, stockId, price, quantity, sj.constant.Action.Buy)

def sell(api, stockId, price, quantity):
    place_order(api, stockId, price, quantity, sj.constant.Action.Sell)

if __name__ == "__main__":
    args = ArgParser()

    with API(
        simulation=args.sandbox,
        apiKey=args.apiKey,
        secretKey=args.secretKey,
        caPath=args.caPath,
        caPasswd=args.caPasswd,
        personId=args.personId
    ) as api:

        stockId = args.stockId
        toDate = date.today() - timedelta(days=1) # TODO: Should be today?
        fromDate = toDate - timedelta(days=args.maDays - 1)
        lastDate = toDate - timedelta(days=1)

        # Find today's price
        todayPrice = compute_price(api, stockId, toDate)
        if todayPrice is None: raise TypeError(todayPrice)
        print("Tdy: %.1f" % (todayPrice))
        print("")

        # Find yesterday's price
        lastPrice = compute_price(api, stockId, lastDate)
        if lastPrice is None: raise TypeError(lastPrice)
        print("Lst: %.1f" % (lastPrice))
        print("")

        # Find average price
        averagePrice = compute_average_price(api, stockId, fromDate, toDate)
        if averagePrice is None: raise TypeError(averagePrice)
        print("Avg: %.1f" % (averagePrice))
        print("")

        if (lastPrice - averagePrice) * (todayPrice - averagePrice) < 0:
            # Trend changes; time to transact

            if (todayPrice - averagePrice) > 0:
                # Buy
                price = todayPrice - averagePrice
                quantity = args.orderPrice / price
                print("Buying %d @ %.1f ..." % (quantity, price))
                print("")

                trade = buy(api, stockId=stockId, price=price, quantity=quantity)

            elif (todayPrice - averagePrice) < 0:
                # Sell
                price = averagePrice - todayPrice
                quantity = args.orderPrice / price
                print("Selling %d @ %.1f ..." % (quantity, price))
                print("")

                trade = sell(api, stockId=stockId, price=price, quantity=quantity)

            if trade is not None:
                print(trade)
                print("")
