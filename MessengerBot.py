from fbchat import *
from Credentials import *
import json


class MessengerBot:
    def __init__(self):
        self.client = None

    def login(self, username, password):
        if self.client is None:
            cookies = None
            try:
                with open("session.json") as file:
                    cookies = json.load(file)
                    print("Loading session cookies...")

            except FileNotFoundError:
                print("First time logging in...")

            self.client = Client(username, password, session_cookies=cookies)
            print(self.client.isLoggedIn())

            if cookies is None:
                with open("session.json", "w") as file:
                    json.dump(self.client.getSession(), file)


if __name__ == "__main__":
    bot = MessengerBot()
    bot.login(username, passwd)
    print("done")
