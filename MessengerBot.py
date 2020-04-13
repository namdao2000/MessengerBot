from fbchat import *
from fbchat.models import *
from Credentials import *
import json
import requests
import re
import os
import time
from multiprocessing import Process, Value, Manager
import socket


def finalVerification(url):
    if re.search("homework-help", url):
        return True
    return False


def question_id(url):
    try:
        ID = ""
        i = len(url) - 1
        while i > 0:
            if url[i] != "q":
                ID = url[i] + ID
            else:
                return "q" + ID
            i -= 1
    except Exception:
        return "QUESTION ID ERROR"


def verifyURL(url):
    try:
        response = requests.head(url)
        print(response.status_code)
        if response.status_code == 404:
            print("Bad website.")
            return False
        return True
    except Exception:
        print("Bad website")
        return False


def isAnswered(url):
    id = question_id(url)
    for root, dirs, files in os.walk("./screenshots"):
        for name in files:
            if name == id + ".png":
                return True
        return False


class CustomClient(Client):

    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type, ts, metadata, msg):
        global daily_limit, start_time

        def respond(text, msgType=None):
            if thread_type == thread_type.GROUP:
                if msgType is None:
                    self.send(Message(text=text), thread_id=thread_id, thread_type=thread_type)
                elif msgType == "IMAGE":
                    self.sendLocalImage(text, thread_id=thread_id, thread_type=thread_type)
            elif thread_type == thread_type.USER:
                if msgType is None:
                    self.send(Message(text=text), thread_id=author_id, thread_type=thread_type)
                elif msgType == "IMAGE":
                    self.sendLocalImage(text, thread_id=author_id, thread_type=thread_type)

        def collectPNG():
            global que_position, socket, recent_call
            que_position += 1
            print("Started a thread to collect {}".format(question_id(message)))
            respond("You have {} new questions left. Approximate retrieval time: {:.0F} seconds".format(daily_limit[author_id], que_position*25 + 1*max(0, 25-(time.time()-recent_call)) + (que_position-1)*25))

            while que_position-1 != 0 or time.time() - recent_call < 25:
                time.sleep(0.1)

            socket.sendto(message.encode(), ("127.0.0.1", 5000))
            recent_call = time.time()
            print("Request sent to AnswerMe")
            started = time.time()
            while time.time() - started < 25:
                if os.path.exists("./screenshots/" + question_id(message) + ".png"):
                    respond("./screenshots/" + question_id(message) + ".png", "IMAGE")
                    que_position -= 1
                    return
                os.sleep(0.5)
            respond("Error: Timed out.")

        if time.time() - start_time > 86400:
            start_time = time.time()
            daily_limit = {}
        if author_id != self.uid:
            if re.search("CHEGG", message):
                message = message.replace("CHEGG", "").strip()
                if verifyURL(message) and finalVerification(message):
                    respond("Your question {} is being processed.".format(question_id(message)))
                    if isAnswered(message):
                        respond("The question has been identified in Steve's data base.")
                        respond("./screenshots/" + question_id(message) + ".png", "IMAGE")
                    elif author_id in daily_limit and daily_limit[author_id] > 0 or author_id not in daily_limit:
                        if author_id not in daily_limit:
                            daily_limit[author_id] = 4
                        daily_limit[author_id] -= 1
                        Thread(target=collectPNG).start()
                    else:
                        respond(
                            "You have asked too many questions today. Please wait {:.2f} minute(s) to ask more questions!".format(
                                (86400 - (time.time() - start_time)) / 60))
                else:
                    respond("Invalid URL. Please type in a correct link.")


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

            self.client = CustomClient(username, password, session_cookies=cookies)
            print("Is logged in? {}".format(self.client.isLoggedIn()))

            if cookies is None:
                with open("session.json", "w") as file:
                    json.dump(self.client.getSession(), file)

    def listen(self):
        print("Listening")
        self.client.listen()


if __name__ == "__main__":
    while True:
        try:
            socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            que_position = 0
            start_time = time.time()
            recent_call = 0
            daily_limit = {}
            bot = MessengerBot()
            bot.login(username, passwd)
            bot.listen()
        except Exception:
            continue
