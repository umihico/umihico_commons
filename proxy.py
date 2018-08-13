from umihico_commons.requests_wrapper import get_with_proxy
import queue
from time import time
from umihico_gist.get_anonymous_proxy.get_anonymous_proxy import get_anonymous_proxy
from umihico_commons.functools import load_from_txt, save_as_txt, PlannedException
import random


class _ProxyQueue():
    def __init__(self, iterable=None):
        self.queue = queue.PriorityQueue()
        iterable = iterable or []
        for proxy in iterable:
            self._put(proxy)

    def add_new_proxy(self, proxy):
        self._put(proxy)

    def _put(self, proxy, score=0):
        if score == 0:
            score = random.random()
        self.queue.put((score, proxy))

    def get(self):
        score, proxy = self.queue.get_nowait()
        return score, proxy

    def put(self, proxy, score):
        self._put(proxy, score)


class ProxyRequests():
    def __init__(self):
        self.proxyqueue = _ProxyQueue()
        self.scrap_new_proxy()
        self.last_proxy_refilled_time = time()

    def scrap_new_proxy(self, old_proxies=None):
        print("scrap_new_proxy...")
        proxies = get_anonymous_proxy()
        old_proxies = old_proxies or []
        new_proxies = list(set(proxies) - set(old_proxies))
        all_proxies = list(set(proxies) + set(old_proxies))
        save_as_txt("proxy.txt", all_proxies)
        self._add_proxies(new_proxies)

    def load_proxy(self):
        proxies = load_from_txt("proxy.txt")
        self._add_proxies(proxies)

    def _add_proxies(self, proxies):
        for proxy in proxies:
            self.proxyqueue.add_new_proxy(proxy)

    def refill_proxy(self):
        old_proxies = load_from_txt("proxy.txt")
        self.scrap_new_proxy(old_proxies=old_proxies)
        self.last_proxy_refilled_time = time()

    def get(self, url, res_test_func):
        if self.last_proxy_refilled_time - time() > 60 * 60:
            self.refill_proxy()
        # print(url)
        success = False
        while not success:
            score, proxy = self.proxyqueue.get()
            # print(score, proxy, url)
            start_time = time()
            try:
                res = get_with_proxy(url, proxy)
                # print("access success", proxy)
            except (Exception, ) as e:
                # print(e)
                # print("access failed", proxy)
                self.proxyqueue.put(proxy, score + 30)
            else:
                if bool(res_test_func(res)):
                    score = start_time - time()
                    success = True
                    # print("test success")
                else:
                    # print("test failed")
                    score += 10
                self.proxyqueue.put(proxy, score)

        # print("success!!!", proxy)
        return res


if __name__ == '__main__':
    proxyrequests = ProxyRequests()
    proxyrequests.load_proxy()
    import itertools
    import requests

    def res_test_func(res): return True
    urls = [
        'https://api.ipify.org',
        'http://checkip.amazonaws.com/',
        'http://icanhazip.com',
        "http://httpbin.org/ip",
        "http://api.aoikujira.com/ip/ini",
    ]
    for url in itertools.cycle(urls):
        print(url)
        # print(requests.get(url).text)
        print(proxyrequests.get(url, res_test_func).text)
