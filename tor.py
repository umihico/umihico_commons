from requests import Session
from umihico_commons.functools import isLinux

_port_num = "9050" if isLinux() else "9150"
_tor_session = Session()
_tor_session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0"
_tor_session.proxies = dict(
    http=f'socks5h://127.0.0.1:{_port_num}',
    https=f'socks5h://127.0.0.1:{_port_num}')


def get(url):
    _tor_session.cookies.clear()
    return _tor_session.get(url, timeout=(300, 300))


if __name__ == '__main__':
    import requests
    my_ip = requests.get('http://checkip.amazonaws.com/').text
    tor_ip = get('http://checkip.amazonaws.com/').text
    print(my_ip, tor_ip)
    from lxml import html
    res = get('http://xiwayy2kn32bo3ko.onion')
    res.encoding = 'Shift_JIS'
    lxml = html.fromstring(res.text)
    print(lxml.xpath("//title")[0].text_content())
    print([x.text_content() for x in lxml.xpath("//a")])
    print([x.get('href') for x in lxml.xpath("//a")])
