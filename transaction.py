from datetime import date, timedelta
from API import API
from ArgParser import ArgParser
import shioaji as sj

def get_close(api, stockId, date):
    ticks = api.ticks(contract=api.Contracts.Stocks[stockId], date=date.strftime("%Y-%m-%d"))
    closes = ticks.close
    if len(closes) == 0:
        print("%s: None" % (date.strftime("%Y-%m-%d")))
        return None

    print("%s: %.2f" % (date.strftime("%Y-%m-%d"), closes[-1]))
    return closes[-1]

def date_range(fromDate, toDate):
    days = (toDate - fromDate).days + 1
    return [fromDate + timedelta(days=i) for i in range(days)]

def get_closes(api, stockId, fromDate, toDate):
    return [get_close(api, stockId, date) for date in date_range(fromDate, toDate)]    

def compute_average_price(prices):
    prices = list(filter(lambda price: price is not None, prices))
    return sum(prices) / len(prices)

def compute_price(api, stockId, date):
    return get_close(api, stockId, date)

def place_order(api, stockId, price, quantity, action):
    contract = getattr(
        api.Contracts.Stocks.TSE,
        "TSE" + stockId
    )

    order = api.Order(
        price=price,
        quantity=quantity,
        action=action,
        price_type=sj.constant.StockPriceType.MKT,
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
        fromDate = toDate - timedelta(days=args.maDays)
        lastDate = toDate - timedelta(days=1)

        # Find today's price
        print("")
        print("Computing today's price")
        todayPrice = compute_price(api, stockId, toDate)
        if todayPrice is None: raise TypeError(todayPrice)

        # Find yesterday's price
        print("")
        print("Computing yesterday's price")
        lastPrice = compute_price(api, stockId, lastDate)
        if lastPrice is None: raise TypeError(lastPrice)

        # Find avarage prices
        print("")
        print("Computing %dma" % (args.maDays))
        closes = get_closes(api, stockId, fromDate, toDate)

        print("")
        print("Computing today's %dma" % (args.maDays))
        todayAvgPrice = compute_average_price(closes[0:-1])
        if todayAvgPrice is None: raise TypeError(todayAvgPrice)

        print("")
        print("Computing yesterday's %dma" % (args.maDays))
        lastAvgPrice = compute_average_price(closes[1:])
        if lastAvgPrice is None: raise TypeError(lastAvgPrice)

        # Print
        print("")
        print("=== Result ===")
        print("Tdy - %dma: %.2f - %.2f" % (args.maDays, todayPrice, todayAvgPrice))
        print("Lst - %dma: %.2f - %.2f" % (args.maDays, lastPrice, lastAvgPrice))
        print("")

        lastDiff = lastPrice - lastAvgPrice
        todayDiff = todayPrice - todayAvgPrice
        if lastDiff * todayDiff <= 0:
            # Trend changes; time to transact

            price = todayPrice
            quantity = args.orderQuantity
            trade = None

            if todayDiff > 0:
                # Buy
                print("Buying %d @ %.2f ..." % (quantity, price))
                print("")

                trade = buy(api, stockId=stockId, price=price, quantity=quantity)

            elif todayDiff <= 0:
                # Sell
                print("Selling %d @ %.2f ..." % (quantity, price))
                print("")

                trade = sell(api, stockId=stockId, price=price, quantity=quantity)

            if trade is not None:
                print(trade)
                print("")
        else:
            print("Not a checkpoint")
            print("")
