from requests import get as requests_get
from requests import Session
import requests
from traceback import print_exc


def get(url):
    session = requests.session()
    session.cookies.clear()
    proxies = dict(
        http='socks5://127.0.0.1:9150',
        https='socks5://127.0.0.1:9150')
    session.proxies = proxies
    session.headers = {}
    session.headers['User-agent'] = 'HotJava/1.1.2 FCS'
    res = session.get(url)
    # res = requests_get(url, proxies=proxies, headers=headers)
    return res


if __name__ == '__main__':
    my_ip = requests_get('http://checkip.amazonaws.com/').text
    tor_ip = get('http://checkip.amazonaws.com/').text
    print(my_ip, tor_ip)
    urls = ['socks5h://xiwayy2kn32bo3ko.onion',
            'socks5h://www.facebookcorewwwi.onion']
    for url in urls:
        try:
            onion_channel = get(url).headers
            print(onion_channel)
        except (Exception, ) as e:
            print_exc()
