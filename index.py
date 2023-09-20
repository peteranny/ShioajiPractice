import argparse
import re
import csv
from datetime import datetime, timedelta
import shioaji as sj

class API:
    def __init__(self, simulation, apiKey, secretKey, caPath, caPasswd, personId) -> None:
        self.simulation = simulation
        self.apiKey = apiKey
        self.secretKey = secretKey
        self.caPath = caPath
        self.caPasswd = caPasswd
        self.personId = personId

    def login(self):
        self.api = sj.Shioaji(simulation=self.simulation)
        self.api.login(self.apiKey, self.secretKey)
        self.api.activate_ca(
            ca_path=self.caPath,
            ca_passwd=self.caPasswd,
            person_id=self.personId
        )
        return self.api

    def logout(self):
        self.api.logout()

    def __enter__(self):
        print("Connecting API...")
        return self.login()

    def __exit__(self, exc_type, exc_value, traceback):
        if not exc_type:
            print("Disconnecting API...")
            self.logout()
        else:
            print("Exception type:", exc_type)
            print("Exception value:", exc_value)
            print("Traceback:", traceback)
            exit(1)

class Frame:
    def __init__(self, t, price, volume):
        self.date = datetime.fromtimestamp(t/1_000_000_000)
        self.price = price
        self.volume = volume

    def __str__(self) -> str:
        return "[%s] %d @ $%f"%(self.date.strftime("%Y-%m-%d %H:%M:%S"), self.volume, self.price)

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

def getArgsParser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--sandbox", action="store_true")
    parser.add_argument("--api-key", type=str)
    parser.add_argument("--secret-key", type=str)
    parser.add_argument("--ca-path", type=str)
    parser.add_argument("--ca-passwd", type=str)
    parser.add_argument("--person-id", type=str)

    parser.add_argument("--stock-id", type=str)
    parser.add_argument("--from-date", type=str)
    parser.add_argument("--to-date", type=str)
    parser.add_argument("--output", type=str)

    return parser

if __name__ == "__main__":
    argsParser = getArgsParser()
    args = argsParser.parse_args()

    with API(
        simulation=args.sandbox,
        apiKey=args.api_key,
        secretKey=args.secret_key,
        caPath=args.ca_path,
        caPasswd=args.ca_passwd,
        personId=args.person_id
    ) as api:

        print("")
        stockId = args.stock_id
        fromDate = datetime.strptime(args.from_date, "%Y-%m-%d")
        toDate = datetime.strptime(args.to_date, "%Y-%m-%d")
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
