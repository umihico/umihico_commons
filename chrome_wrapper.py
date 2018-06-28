from selenium import webdriver
from lxml import html
import os
import sys
import inspect
from selenium.webdriver.common.keys import Keys
import shutil
from distutils import dir_util
from traceback import format_exc
from time import sleep
import re
import datetime
try:
    import logging
    from selenium.webdriver.remote.remote_connection import LOGGER
    LOGGER.setLevel(logging.WARNING)
except (Exception, ) as e:
    print(e)


def rename_method(pure_elements):
    for pure_element in pure_elements:
        pure_element.xpath = pure_element.find_elements_by_xpath


def _clean_unused_cookies(cookies_base_path):
    """if you can rename, delete it."""
    folder_names = os.listdir(cookies_base_path)
    dummy_path = os.path.join(
        cookies_base_path, 'dummy_folder')
    other_cookie_folders = [os.path.join(
        cookies_base_path, folder_name) for folder_name in folder_names]
    for other_cookie_path in other_cookie_folders:
        _del_dir(other_cookie_path)
        continue
        # try:
        #     os.rename(other_cookie_path, dummy_path)
        # except PermissionError:
        #     continue
        # else:
        #     _del_dir(dummy_path)


def _del_dir(path):
    shutil.rmtree(path=path, ignore_errors=True)


def _robocopy(from_path, to_path):
    if os.path.isdir(from_path):
        try:
            dir_util.copy_tree(from_path, to_path, preserve_mode=0)
        except (Exception, ) as e:
            print(e)
    else:
        try:
            makedirs(to_path, exist_ok=True)
        except (Exception, ) as e:
            pass
        shutil.copy2(from_path, to_path)


def _gen_executable_path():
    import __main__
    dirname, filename = os.path.split(os.path.abspath(__main__.__file__))
    path = os.path.join(dirname, "chromedriver")
    return path


def _gen_ChromeOptions(userAgent, cookie_key, headless):

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("user-agent=" + userAgent)
    try:
        if os.uname()[0] == 'Linux':
            options.add_argument(
                "download.default_directory=/home/ec2-user/downloads")
        else:
            raise Exception("not linux")
    except (Exception, ) as e:
        options.add_argument(
            "download.default_directory=C:/Users/umi/Downloads")
        from os import path
        extenion_path = path.join(path.dirname(path.abspath(
            __file__)), "chrome_extension_xpath_helper.crx")
        options.add_extension(extenion_path)
    try:
        if os.uname()[0] == 'Linux' or headless:
            options.add_argument("--headless")
        if os.uname()[0] == 'Linux':
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1280,1024')
            options.add_argument("--headless")
    except (Exception, ) as e:
        pass

    if cookie_key is not None:
        set_cookie(options, cookie_key)
        try:
            set_cookie(options, cookie_key)
        except (Exception, ) as e:
            while True:
                try:
                    set_cookie(options, cookie_key='copy')
                except (Exception, ) as e:
                    print(format_exc())
                    sleep(5)

    return options


def _gen_cookie_folder_name(name='no_name'):
    pattern = r'([0-9]*)'
    return '_'.join(re.findall(pattern, str(datetime.datetime.today()))).replace('__', '_') + name
    # '2018_04_13_17_30_15_913448_no_name'


def set_cookie(options, cookie_key):
    if cookie_key is None:
        return

    cookie_path_original = "C:\\Users\\umi\\AppData\\Local\\Google\\Chrome\\User Data"

    if cookie_key == 'original':
        options.add_argument("user-data-dir=" + cookie_path_original)
        return

    if cookie_key == 'copy':
        copy_cookie_path = cookie_path_original

    else:
        copy_cookie_path = os.path.join(
            'C:\\Users\\umi\\data\\saved_cookie', cookie_key)

    cookie_path_original_default = os.path.join(
        cookie_path_original, 'Default')
    cookies_base_path = 'C:\\Users\\umi\\data\\cookie'
    this_cookie_path = os.path.join(
        cookies_base_path, _gen_cookie_folder_name(name=cookie_key))
    # C:\Users\umi\data\cookie\2018_04_13_17_34_10_708525_no_name
    this_cookie_path_default = os.path.join(this_cookie_path, 'Default')
    # C:\Users\umi\data\cookie\2018_04_13_17_34_10_708525_no_name\Default

    copy_cookie_path_default = os.path.join(copy_cookie_path, 'Default')
    _clean_unused_cookies(cookies_base_path)

    os.makedirs(os.path.join(this_cookie_path, 'Default'), exist_ok=True)

    for filename in ['Cookies', 'Secure Preferences', 'Local Storage']:
        from_path = os.path.join(copy_cookie_path_default, filename)
        to_path = os.path.join(this_cookie_path_default, filename)
        _robocopy(from_path, to_path)

    options.add_argument("user-data-dir=" + this_cookie_path)


def _gen_desired_capabilities(userAgent):
    headers = {
        "phantomjs.page.settings.userAgent": userAgent,
        'marionette': True}
    return headers


class Chrome(webdriver.Chrome):
    def __init__(self, cookie_key=None, headless=False):
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        kwargs = {
            'chrome_options': _gen_ChromeOptions(userAgent, cookie_key, headless),
            'desired_capabilities': _gen_desired_capabilities(userAgent)}
        try:
            super().__init__(**kwargs)
        except (Exception, ) as e:
            if bool("executable needs to be in PATH" in str(e)):
                kwargs['executable_path'] = _gen_executable_path()
                super().__init__(**kwargs)
            else:
                raise
        self.maximize_window()
        self.backup_executor_url = self.command_executor._url
        self.backup_session_id = self.session_id

    def get(self, url):
        try:
            super().get(url)
        except (Exception, ) as e:
            print(url)
            raise

    def xpath_lxml(self, path, make_links_absolute=False):
        try:
            page_source = self.page_source
        except (Exception, ) as e:
            # executor_url, session_id = self.backup_executor_url, self.backup_session_id
            # self = webdriver.Remote(
            #     command_executor=executor_url, desired_capabilities={})
            # self.session_id = session_id
            raise

        doc = html.fromstring(page_source)
        if make_links_absolute:
            html.make_links_absolute(doc, base_url=self.current_url)
        elements = doc.xpath(path)
        return elements

    def xpath(self, path, IndexError_msg=None):
        lxml_elements = self.xpath_lxml(path)
        pure_elements = self.find_elements_by_xpath(
            path) if bool(len(lxml_elements)) else []
        rename_method(pure_elements)
        wrapped_elements = WebElementsWrapper(
            pure_elements, IndexError_msg, path)
        return wrapped_elements

    @property
    def all_text(self):
        body_element = self.find_element_by_tag_name('body')
        return body_element.text

    def copy_tab(self):
        self.find_element_by_tag_name(
            'body').send_keys(Keys.ALT, 'D', Keys.ENTER)

    def close_tab(self):
        self.close()
        # self.find_element_by_tag_name(
        #     'body').send_keys(Keys.CONTROL + 'w') dosen't work

    def switch_tab(self, index=0):
        self.switch_to.window(self.window_handles[index])

    def new_tab(self):
        self.execute_script('''window.open("","_blank");''')


class WebElementsWrapper(list):
    """to be able to prevent IndexError by Chrome.xpath(path)[0]"""
    """to set useful properties like .texts"""

    def __init__(self, webelements, IndexError_msg, xpath):
        self.IndexError_msg = IndexError_msg
        self.xpath = xpath
        super().__init__(webelements)

    def __getitem__(self, key):
        if len(self) <= key and not self.IndexError_msg is None:
            return WebElementPretender(self.IndexError_msg)
        else:
            try:
                return super().__getitem__(key)
            except (Exception, ) as e:
                print(e)
                print(f'key:{key}')
                print(f'xpath:{self.xpath}')
                print(f'len:{len(self)}')
                raise

    def __getattr__(self, key):
        if key.endswith('s'):  # hrefs, srcs, texts
            keys = key
            key = keys[:len(keys) - 1]
            try:
                return_ = [getattr(x, key) for x in self]  # text
            except (Exception, ) as e:
                try:
                    return_ = [x.get_attribute(key) for x in self]  # href
                except (Exception, ) as e:
                    pass
            return return_
        else:
            raise Exception(f'__getattr__ got unknown key:{key}')


class WebElementPretender():
    """to prevent AttributeError by Chrome.xpath(path)[0].text"""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.msg

    def get_attribute(self, key):
        return self.msg

    def __getattr__(self, key):
        return self.msg


if __name__ == '__main__':
    c = Chrome()
    c.get("https://ja.wikipedia.org/wiki/%E6%9D%B1%E4%BA%AC%E3%83%89%E3%83%BC%E3%83%A0")
    print(c.all_text)
