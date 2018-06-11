# -*- coding: utf-8 -*-
import requests
import pprint
<<<<<<< HEAD
from passpacker import passwords


class ChatworkApi():
    def __init__(self):
        self.api_key = passwords['chatwork_api_key']
        self.chat_id = passwords['chatwork_chatroom_number']

    def post_in_mychat(self, msg):
        end_point_url = "https://api.chatwork.com/v2"
        post_message_url = f'{end_point_url}/rooms/{self.chat_id}/messages'
        headers = {'X-ChatWorkToken': self.api_key}
        params = {'body': msg}
        resp = requests.post(post_message_url, headers=headers, params=params)
        pprint.pprint(resp.content)
=======
from mother import passwords


def post_in_mychat(msg):
    token = passwords['chatwork_api_key_mhk256']
    end_point_url = "https://api.chatwork.com/v2"
    chat_id = "102754923"
    post_message_url = f'{end_point_url}/rooms/{chat_id}/messages'
    headers = {'X-ChatWorkToken': token}
    params = {'body': msg}
    resp = requests.post(post_message_url, headers=headers, params=params)
    pprint.pprint(resp.content)
>>>>>>> 5ae6e267213ab670da0df1bd21214dd159878cb8


if __name__ == '__main__':
    post_in_mychat(msg='hello world3')
