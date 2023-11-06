from datetime import datetime

class Frame:
    def __init__(self, t, price, volume):
        self.date = datetime.fromtimestamp(t/1_000_000_000)
        self.price = price
        self.volume = volume

    def __str__(self) -> str:
        return "[%s] %d @ $%f"%(self.date.strftime("%Y-%m-%d %H:%M:%S"), self.volume, self.price)
