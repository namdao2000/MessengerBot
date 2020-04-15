# from fbchat import *
# from fbchat.models import *
# from Credentials import *
# import json
# import requests
# import re
# import os
# import time
# from multiprocessing import Process, Value, Manager
# import socket
# import copy
# from MessengerBot import MessengerBot, respondFinal, question_id
#
# socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socket.bind(("127.0.0.1", 5001))
#
# collectBot = MessengerBot()
# collectBot.login(username, passwd)
# print("Collection bot initialised...")
# tasks = []
#
# def processTask(task):
#     global finished
#     url = task[0]
#     thread_type = task[1]
#     thread_id = task[2]
#     author_id = task[3]
#
#     def respond(text, msgType=None):
#         respondFinal(collectBot.getClient(), text, thread_type, thread_id, author_id, msgType)
#
#     socket.sendto(url.encode(), ("127.0.0.1", 5000))
#     started = time.time()
#
#     while time.time() - started < 30:
#         if os.path.exists("./screenshots/" + question_id(url) + ".png"):
#             respond("./screenshots/" + question_id(url) + ".png", "IMAGE")
#             return
#         time.sleep(0.5)
#     respond("Error: Timed out.")
#     finished = True
#
#
# if __name__ == "__main__":
#     while True:
#         task = socket.recv(500).decode("utf-8").split("|||")
#         if len(tasks) > 0:
#         print(tasks)
#         finished = False
#         processTask(tasks.pop())
#         while not finished:
#             time.sleep(0.1)
#         else:
#         time.sleep(0.1)
