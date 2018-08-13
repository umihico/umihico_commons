
#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests

get = requests.get('http://httpbin.org/ip',
                   proxies=dict(http='socks5://127.0.0.1:9050',
                                https='socks5://127.0.0.1:9050')).text
print(get)
if __name__ == '__main__':
    pass
