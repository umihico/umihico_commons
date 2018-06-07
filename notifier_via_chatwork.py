# -*- coding: utf-8 -*-
import requests
import pprint
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


if __name__ == '__main__':
    post_in_mychat(msg='hello world3')
