import argparse

class ArgParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()

        self.add_argument("--sandbox", action="store_true")
        self.add_argument("--api-key", type=str)
        self.add_argument("--secret-key", type=str)
        self.add_argument("--ca-path", type=str)
        self.add_argument("--ca-passwd", type=str)
        self.add_argument("--person-id", type=str)

        self.add_argument("--stock-id", type=str)
        self.add_argument("--from-date", type=str)
        self.add_argument("--to-date", type=str)
        self.add_argument("--output", type=str)
