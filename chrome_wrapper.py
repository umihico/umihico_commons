from selenium import webdriver
from lxml import html
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
import shutil
from distutils import dir_util
from traceback import print_exc
from time import sleep
import re
import datetime
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
try:
    from functools import isLinux
except (Exception, ) as e:
    from .functools import isLinux

try:
    import logging
    from selenium.webdriver.remote.remote_connection import LOGGER
    LOGGER.setLevel(logging.WARNING)
except (Exception, ) as e:
    print_exc()
try:
    from requests_common import user_agent as default_userAgent
except (Exception, ) as e:
    from .requests_common import user_agent as default_userAgent


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


def gen_ChromeOptions(userAgent=default_userAgent, cookie_key=None, headless=False):

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("user-agent=" + userAgent)
    if isLinux():
        options.add_argument(
            "download.default_directory=/home/ec2-user/downloads")
    else:
        options.add_argument(
            "download.default_directory=C:/Users/umi/Downloads")
        extenion_path = os.path.join(os.path.dirname(os.path.abspath(
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
                    print_exc()
                    sleep(5)

    return options


default_custom_chrome_options = gen_ChromeOptions()
dirname, filename = os.path.split(os.path.abspath(__file__))
proxy_zip_path = os.path.join(dirname, "proxy.zip")
# print(path)
# default_custom_chrome_options.add_extension(path)
# default_custom_chrome_options.add_argument("--kiosk")


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


def gen_desired_capabilities(userAgent):
    desired_capabilities = DesiredCapabilities().CHROME
    desired_capabilities["pageLoadStrategy"] = "normal"
    # "normal"  # complete
    # "eager"  #  only html
    # "none" # immediately
    desired_capabilities["phantomjs.page.settings.userAgent"] = userAgent
    desired_capabilities['marionette'] = True
    return desired_capabilities


default_custom_desired_capabilities = gen_desired_capabilities(
    userAgent=default_userAgent)


class Chrome(webdriver.Chrome):
    def __init__(self, userAgent=default_userAgent, cookie_key=None, headless=False, desired_capabilities=default_custom_desired_capabilities, chrome_options=default_custom_chrome_options):
        kwargs = {
            'chrome_options': chrome_options,
            'desired_capabilities': desired_capabilities}
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

    def xpath(self, xpath):
        return Chrome_xpath(self, xpath)

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


def _gen_xpath_func(lxml_lambda):
    def _xpath(self, xpath):
        lxml_elements = lxml_lambda(self, xpath)
        pure_elements = self.find_elements_by_xpath(
            xpath) if bool(len(lxml_elements)) else []
        return pure_elements
    return _xpath


Chrome_xpath = _gen_xpath_func(
    lxml_lambda=lambda self, xpath: self.xpath_lxml(xpath))
WebElement_xpath = _gen_xpath_func(lxml_lambda=lambda self, xpath: html.fromstring(
    self.get_attribute('outerHTML')).xpath(xpath))


def _select_by_visible_text(self, text):
    Select(self).select_by_visible_text(text)


def _send_keys_select_all(self):
    self.send_keys(Keys.CONTROL, 'a')


def _scroll_here(self):
    _perform = ActionChains(self.parent).move_to_element(self)
    self.parent.execute_script("arguments[0].scrollIntoView();", self)
    _perform.perform()


def _move_and_click(self):
    try:
        self.origin_click()
    except (Exception, ) as e:
        try:
            self.scroll_here()
            self.origin_click()
        except (Exception, ) as e:
            raise


def edit_WebElement():
    # _move_and_click need "origin_click"
    WebElement.origin_click = WebElement.click
    WebElement.xpath = WebElement_xpath
    WebElement.click = _move_and_click
    WebElement.select_by_visible_text = _select_by_visible_text
    WebElement.send_keys_select_all = _send_keys_select_all
    WebElement.scroll_here = _scroll_here


edit_WebElement()

if __name__ == '__main__':
    c = Chrome()
    c.get("https://ja.wikipedia.org/wiki/%E6%9D%B1%E4%BA%AC%E3%83%89%E3%83%BC%E3%83%A0")
    print(c.all_text)
