try:
    from requests_common import headers_dict_user_agent, user_agent
except (Exception, ) as e:
    from .requests_common import headers_dict_user_agent, user_agent
from requests import Session as requests_Session
from requests import get as requests_get
from lxml import html


def save_img(response, filename):
    img = Image.open(BytesIO(response.content))
    img.convert('RGB').save(filename)


def save_img_response_test_func(response):
    try:
        img = Image.open(BytesIO(response.content))
        img.convert('RGB')
        return True
    except Exception as e:
        return False


def get_with_proxy(url, proxy):
    s = Session(Proxy=proxy)
    res = s.get(url)
    return res


def get(url):
    return requests_get(url, headers=headers_dict_user_agent)


def url_to_lxml(url):
    return html.fromstring(get(url).text)


class Session(requests_Session):
    def __init__(self, Proxy=None):
        super().__init__()
        self.headers['User-Agent'] = user_agent
        if not Proxy is None:
            self.proxies = {
                'http': 'http://' + Proxy,
                'https': 'https://' + Proxy, }

    def get(self, url, connet_timeout=10, read_time=30):
        # connect timeoutを10秒, read timeoutを30秒に設定
        res = super().get(url, timeout=(connet_timeout, read_time))
        res.raise_for_status()
        return res


if __name__ == '__main__':
    from umihico_commons.functools import load_from_txt
    from threading import Thread, Semaphore
    proxies = load_from_txt("result.txt")
    sem = Semaphore(value=100)
    from lxml import html

    def res_func(res):
        print(html.fromstring(res.text).xpath("//title")[0].text_content())

    def test_proxy_func(test_proxy, sem):
        with sem:
            try:
                res = get_with_proxy(
                    'https://textream.yahoo.co.jp/message/1001925/bgoba5oa5a6a599a96h', test_proxy)
            except (Exception, ) as e:
                print("failed")
                return
            try:
                res_func(res)
            except (Exception, ) as e:
                print(e)
    for proxy in proxies:
        Thread(target=test_proxy_func,  args=(proxy, sem,)).start()
