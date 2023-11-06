import re
import csv
from datetime import datetime, timedelta
from API import API
from Frame import Frame
from ArgParser import ArgParser

def getFrames(api, stockId, date):
    ticks = api.ticks(contract=api.Contracts.Stocks[stockId], date=date.strftime("%Y-%m-%d"))

    ts = ticks.ts
    prices = ticks.close
    volumes = ticks.volume

    return list(map(lambda t, price, volume: Frame(t, price, volume), ts, prices, volumes))

def putPriceBuckets(frames):
    priceBuckets = {}

    for frame in frames:
        priceBuckets.setdefault(frame.price, 0)
        priceBuckets[frame.price] += frame.volume

    return priceBuckets

def dateRange(fromDate, toDate):
    days = (toDate - fromDate).days + 1
    return [fromDate + timedelta(days=i) for i in range(days)]

def inputDate(msg):
    while True:
        date = input(msg)
        if re.match(r"\d{4}-\d{2}-\d{2}", date):
            return date
        print("Must comply with YYYY-MM-DD")

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

        print("")
        stockId = args.stockId
        fromDate = datetime.strptime(args.fromDate, "%Y-%m-%d")
        toDate = datetime.strptime(args.toDate, "%Y-%m-%d")
        allFrames = []

        for date in dateRange(fromDate, toDate):
            frames = getFrames(api, stockId=stockId, date=date)
            for frame in frames:
                print(frame)
            allFrames += frames

        print("")
        print("==== Price Buckets ====")

        priceBuckets = putPriceBuckets(frames)
        for price, volume in sorted(priceBuckets.items(), reverse=True):
            print("$%f: %d"%(price, volume))

        filename = args.output
        print("")
        print("Writing to %s..."%(filename))

        with open(filename, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Price", "Volume between %s to %s"%(fromDate.strftime("%Y-%m-%d"), toDate.strftime("%Y-%m-%d"))])
            for price, volume in sorted(priceBuckets.items(), reverse=True):
                writer.writerow([price, volume])
