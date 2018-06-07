# -*- coding: utf-8 -*-
import requests
import pprint
from passpacker import passwords


def post_in_mychat(msg):
    token = passwords['chatwork_api_key']
    end_point_url = "https://api.chatwork.com/v2"
    chat_id = passwords['chatwork_chatroom_number']
    post_message_url = f'{end_point_url}/rooms/{chat_id}/messages'
    headers = {'X-ChatWorkToken': token}
    params = {'body': msg}
    resp = requests.post(post_message_url, headers=headers, params=params)
    pprint.pprint(resp.content)


if __name__ == '__main__':
    post_in_mychat(msg='hello world3')
