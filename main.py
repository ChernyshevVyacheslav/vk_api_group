import vk_api

import os

from dotenv import load_dotenv

def post_of_group(url, c, vk):
    group_data=vk.wall.get(domain=url, count=c)
    return group_data

load_dotenv()
Token = os.getenv("TOKEN")
token = vk_api.VkApi(token = Token)
vk = token.get_api()
group_data=post_of_group(someUrl, count, vk)
print(group_data)