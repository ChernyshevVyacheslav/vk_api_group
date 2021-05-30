import vk_api
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import requests

client = MongoClient('mongodb', 27017)
db = client.parser


class Group:
    def __init__(self, domain):
        load_dotenv()
        Token = os.getenv("TOKEN")
        self.token = vk_api.VkApi(token=Token)
        self.vk = self.token.get_api()
        self.domain = domain

    def posts_of_group(self, count):
        group_data = self.vk.wall.get(domain=self.domain, count=count)
        return group_data["items"]

    def save_to_db(self, data):
        db.posts.insert_one({'id': data['id'], 'data': data})

    def check_posts(self, data):
        new_posts = []
        for i in data:
            post = db.posts.find_one({'id': i["id"]})
            if post == None:
                new_posts.append(i)
                self.save_to_db(i)
        return new_posts

    def send_to_chat(self, posts):
        for post in posts:
            text = post["text"]
            data = {
                'message': text,
                'parse_mode': 'HTML'
            }

            requests.post('https://notify.bot.codex.so/u/TOKEN', data=data)
