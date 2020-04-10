from fbchat import *
from Credentials import *
import json


class MessengerBot:
    def __init__(self):
        self.client = None

    def login(self, username, password):
        if self.client is None:
            self.client = Client(username, password)
            print(self.client.isLoggedIn())

if __name__ == "__main__":
    bot = MessengerBot()
    bot.login(username, passwd)
    print("done")