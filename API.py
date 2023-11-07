import shioaji as sj
import traceback

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

    def __exit__(self, exc_type, exc_value, tb):
        if not exc_type:
            print("Disconnecting API...")
            self.logout()
        else:
            print("Exception type:", exc_type)
            print("Exception value:", exc_value)
            traceback.print_tb(tb)
            exit(1)
