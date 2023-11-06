import configparser

class ArgParser(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
        self.read("env.ini")

        self.sandbox = self["DEFAULT"]["SANDBOX"] == "yes"
        self.apiKey = self["DEFAULT"]["API_KEY"]
        self.secretKey = self["DEFAULT"]["SECRET_KEY"]
        self.caPath = self["DEFAULT"]["CA_PATH"]
        self.caPasswd = self["DEFAULT"]["CA_PASSWD"]
        self.personId = self["DEFAULT"]["PERSON_ID"]
        self.stockId = self["DEFAULT"]["STOCK_ID"]
        self.fromDate = self["DEFAULT"]["FROM"]
        self.toDate = self["DEFAULT"]["TO"]
        self.output = self["DEFAULT"]["OUTPUT"]

