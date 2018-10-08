from umihico_commons.requests_wrapper import get_with_proxy
import queue
from time import time
from umihico_gist.get_anonymous_proxy.get_anonymous_proxy import get_anonymous_proxy
from umihico_commons.functools import load_from_txt, save_as_txt, PlannedException
import random
import os
from collections import namedtuple
from threading import Lock
EmptyResponse = namedtuple('EmptyResponse', ('text', 'json', ))
emptyresponse = EmptyResponse(text="", json=dict(),)
refill_proxy_frequency_sec = 60 * 60 * 2
import itertools
from tinydb import TinyDB


class TooManyGetFailedException(Exception):
    pass


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
    def __init__(self, failed_count_limit):
        self.proxy_errors = TinyDB('proxy_errors.json')
        self.proxy_errors.purge()
        self.failed_count_limit = failed_count_limit
        # self.process_index = process_index
        # self.process_max_num = process_max_num
        self.scrap_new_proxy_lock = Lock()
        self.proxyqueue = _ProxyQueue()
        if os.path.isfile("proxy.txt"):
            self.load_proxy()
            if time() - self.last_proxy_refilled_time < refill_proxy_frequency_sec:
                return
        self.scrap_new_proxy()

    def set_response_test_func(self, response_test_func):
        self.response_test_func = response_test_func

    def scrap_new_proxy(self, old_proxies=None):
        if not self.scrap_new_proxy_lock.acquire(False):
            return
        print("scrap_new_proxy...")
        proxies = get_anonymous_proxy()
        old_proxies = old_proxies or ['dummy', []]
        old_proxies = old_proxies[1]
        new_proxies = list(set(proxies) - set(old_proxies))
        all_proxies = list(set([*proxies, *old_proxies]))
        self.last_proxy_refilled_time = time()
        self.seve_proxy(proxies)
        self._add_proxies(new_proxies)
        self.scrap_new_proxy_lock.release()

    def seve_proxy(self, proxies):
        save_as_txt("proxy.txt", [self.last_proxy_refilled_time, proxies])

    def load_proxy(self):
        time_, proxies = load_from_txt("proxy.txt")
        self.last_proxy_refilled_time = time_
        self._add_proxies(proxies)

    def _add_proxies(self, proxies):
        # added_some = False
        # print(self.process_index, self.process_max_num)
        # if self.process_index and self.process_max_num:
        #     for proxy, index in zip(proxies, itertools.cycle(range(1, self.process_max_num + 1))):
        #         self.proxyqueue.add_new_proxy(proxy)
        #         # if self.process_index == index:
        #         #     # added_some = True
        #         #     self.proxyqueue.add_new_proxy(proxy)
        #     # if not added_some:
        #     #     for proxy, index in zip(proxies, itertools.cycle(range(1, self.process_max_num + 1))):
        #     #         print(proxy, index)
        #     #     print(process_index, self.process_index, self.process_max_num)
        #     #     raise
        #     # print('added_some', added_some)
        # else:
        for proxy in proxies:
            self.proxyqueue.add_new_proxy(proxy)

        #

    def refill_proxy(self):
        old_proxies = load_from_txt("proxy.txt")
        self.scrap_new_proxy(old_proxies=old_proxies)

    def get(self, url, res_test_func=None):
        res_test_func = res_test_func or self.response_test_func
        if time() - self.last_proxy_refilled_time > refill_proxy_frequency_sec:
            self.refill_proxy()
        # print(url)
        success = False
        failed_count = -1
        while not success:
            failed_count += 1
            if failed_count > self.failed_count_limit:
                print(f'ProxyRequests.get error:{url}')
                try:
                    self.proxy_errors.insert(
                        {'url': res.url, 'src': res.text, 'proxy': res.proxy})
                except Exception as e:
                    print(e)
                return url
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
                    res.proxy = proxy
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
