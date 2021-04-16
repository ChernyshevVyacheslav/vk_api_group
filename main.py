import vk_api

import os

import json

from dotenv import load_dotenv

import requests

from apscheduler.schedulers.background import BlockingScheduler

def send_to_group(posts):
    for post in posts:

        text=post["text"]
        data = {
            'message': text,
        'parse_mode': 'HTML'
            }

        requests.post('https://notify.bot.codex.so/u/TOKEN', data=data)


def check_post(data):
    json_data = {}
    new_posts=[]
    with open('posts.json', 'r') as j:
        json_data = json.load(j)
    if isinstance(json_data, str):
        json_data = dict(eval(json_data))
    for i in data:
        if str(i["id"]) not in json_data:
            new_posts.append(i)
            save_to_json(i)
    j.close()
    return new_posts



def post_of_group(url, c, vk):
    group_data=vk.wall.get(domain=url, count=c)
    return group_data["items"]

def save_to_json(data):
    json_data = {}
    with open('posts.json', 'r') as j:
        json_data = json.load(j)
    if isinstance(json_data, str):
        json_data = dict(eval(json_data))
    json_data[data["id"]]=data
    with open('posts.json', 'w+') as file:
        json.dump(json_data, file)
    file.close()
    j.close()
def main():
    load_dotenv()
    Token = os.getenv("TOKEN")
    token = vk_api.VkApi(token = Token)
    vk = token.get_api()
    Domain="yourgroup"
    group_data=post_of_group(Domain, 2, vk)
    new_posts=check_post(group_data)
    send_to_group(new_posts)

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', seconds=3)
    try:
        scheduler.start()
    except KeyboardInterrupt:
        pass
scheduler.shutdown()