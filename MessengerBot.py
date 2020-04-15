from fbchat import *
from fbchat.models import *
from Credentials import *
import json
import requests
import re
import os
import time
from multiprocessing import Process
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


def respondFinal(client, text, thread_type, thread_id, author_id, msgType=None):
    if thread_type == thread_type.GROUP:
        if msgType is None:
            client.send(Message(text=text), thread_id=thread_id, thread_type=thread_type)
        elif msgType == "IMAGE":
            client.sendLocalImage(text, thread_id=thread_id, thread_type=thread_type)
    elif thread_type == thread_type.USER:
        if msgType is None:
            client.send(Message(text=text), thread_id=author_id, thread_type=thread_type)
        elif msgType == "IMAGE":
            client.sendLocalImage(text, thread_id=author_id, thread_type=thread_type)


def collectPNG(bot, socket, task):
    def respond(text, msgType=None):
        respondFinal(bot.getClient(), text, thread_type, thread_id, author_id, msgType)

    print("Collection bot initialised...")

    url = task[0]
    thread_type = task[1]
    thread_id = task[2]
    author_id = task[3]

    socket.sendto(url.encode(), ("127.0.0.1", 5000))
    print("Request sent")
    started = time.time()

    while time.time() - started < 20:
        if os.path.exists("./screenshots/" + question_id(url) + ".png"):
            respond("./screenshots/" + question_id(url) + ".png", "IMAGE")
            return
        time.sleep(0.5)
    respond("Your question {} has timed out. Sorry :/".format(question_id(url)))


class CustomClient(Client):
    def onFriendRequest(self, from_id=None, msg=None):
        def respond(text, msgType=None):
            respondFinal(self, text, ThreadType.USER, None, from_id, msgType)

        self.friendConnect(from_id)
        respond("Hello! To use me, type in CHEGG followed by the link of your question. i.e CHEGG <Link>")
    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type, ts, metadata, msg):
        global daily_limit, start_time, socket, bot2, num_processes

        def respond(text, msgType=None):
            respondFinal(self, text, thread_type, thread_id, author_id, msgType)

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
                            daily_limit[author_id] = 5
                        daily_limit[author_id] -= 1

                        for ps_predicted_finish in num_processes:
                            if time.time() > ps_predicted_finish:
                                num_processes.remove(ps_predicted_finish)

                        predicted_time = 15*max(0, len(num_processes)) + 20 * (len(num_processes)+1)
                        num_processes.append(time.time() + predicted_time)

                        respond("You have {} new questions left. Approximate retrieval time: {:.0F} seconds".format(daily_limit[author_id], predicted_time))

                        task = [message, thread_type, thread_id, author_id]
                        p = Process(target=collectPNG, args=(bot2, socket,task))
                        p.start()
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

    def getClient(self):
        return self.client


if __name__ == "__main__":
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    num_processes = []
    daily_limit = {}
    start_time = 0
    bot = MessengerBot()
    bot2 = MessengerBot()
    bot.login(username, passwd)
    bot2.login(username, passwd)
    bot.listen()
