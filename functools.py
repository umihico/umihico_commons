import codecs
from ast import literal_eval
from pprint import pformat
from multiprocessing import Pool, cpu_count, dummy
from tqdm import tqdm
from itertools import zip_longest
import os
import re
import umihico_private
import requests
import re
_jponly = re.compile('[亜-熙ぁ-んァ-ヶ]')


def exact_jp(string):
    return ''.join(_jponly.findall(string))


_letters_only = re.compile('[亜-熙ぁ-んァ-ヶa-zA-Z0-9]')


def exact_letters(string):
    return ''.join(_letters_only.findall(string))


def line_notify_me(message):
    api_key = umihico_private.get_key('line_notify_me')
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer " + api_key
    }
    data = {
        "message": message
    }
    requests.post(url, headers=headers, data=data)


class PlannedException(Exception):
    pass


def isLinux():
    try:
        return bool(os.uname()[0] == 'Linux')
    except (Exception, ) as e:
        return False


def iferror(func, value):
    def new_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (Exception, ) as e:
            return value
    return new_func


def chunks(list_, chunk_len):
    '''
    l = list(range(10))
    print(l)
    print(chunks(l, 3))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    '''
    return list(list_[i:i + chunk_len] for i in range(0, len(list_), chunk_len))


def flatten(list_of_list):
    return [x for list_ in list_of_list for x in list_]


def save_as_txt(filename, data, mode='w'):
    with codecs.open(filename, mode, 'utf-8') as f:
        f.write(pformat(data))


def load_from_txt(filename):
    with codecs.open(filename, 'r', 'utf-8') as f:
        return literal_eval(f.read())


def numberize(string):
    return re.sub(r'\D', '', string)


def map_multiprocessing(func, args_rows=None, kwargs_rows=None, count=-1):
    """return [func(*args,**kwargs) for args,kwargs in zip_longest(args_rows, kwargs_rows)]
    with multiprocessing"""
    return _map(func, args_rows, kwargs_rows, -1, Pool)


def map_multithreading(func, args_rows=None, kwargs_rows=None, count=100):
    """return [func(*args,**kwargs) for args,kwargs in zip_longest(args_rows, kwargs_rows)]
    with multithreading"""
    return _map(func, args_rows, kwargs_rows, count, dummy.Pool)


def _gen_wrapped_func(func):
    def wrapped_func(enumerated_args_kwargs_rows):
        i, args_kwargs_row = enumerated_args_kwargs_rows
        args, kwargs = args_kwargs_row
        return i, func(*args, **kwargs)
    return wrapped_func


def _map(func, args_rows=None, kwargs_rows=None, max_process=-1, pool_func=Pool):
    wrapped_func = _gen_wrapped_func(func)
    if args_rows is None:
        args_rows = []
    if kwargs_rows is None:
        kwargs_rows = []
    args_kwargs_rows = []
    for args, kwargs in zip_longest(args_rows, kwargs_rows):
        args = args or tuple()
        kwargs = kwargs or dict()
        if type(args) is not tuple or type(kwargs) is not dict:
            raise Exception(
                f"'args,kwargs=arg_row' is wrong type. args:{type(args)},kwargs:{type(kwargs)}")
        args_kwargs_rows.append((args, kwargs))
    enumerated_args_kwargs_rows = list(enumerate(args_kwargs_rows))
    if max_process == -1:
        max_process = cpu_count()
    with pool_func(max_process) as p:
        enumerated_results = []
        for i, result in tqdm(p.imap_unordered(wrapped_func, enumerated_args_kwargs_rows), total=len(args_kwargs_rows)):
            enumerated_results.append((i, result))
        enumerated_results.sort(key=lambda x: x[0])
        results = [result for i, result in enumerated_results]
        return results
