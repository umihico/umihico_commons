from umihico_commons.chrome_wrapper import Chrome, Keys
from umihico_commons import csv_wrapper
import sys
from traceback import format_exc
from time import sleep
import os


def get_raw_meta_texts(url):
    print('running Chrome...')
    c = Chrome()
    c.get(url)
    _scroll_to_the_bottom_google_image_search(c)
    print('exacting by xpath...')
    elements = c.xpath_lxml('//*[@class = "rg_meta notranslate"]')
    raw_meta_texts = list(map(lambda x: x.text_content(), elements))
    c.quit()
    return raw_meta_texts


def _scroll_to_the_bottom_google_image_search(c):
    last_height = 0
    scrolling_cnt = 0
    while True:
        c.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        new_height = c.execute_script("return document.body.scrollHeight")
        scrolling_cnt += 1
        print('scrolling...', scrolling_cnt)
        show_more_result_buttons = c.xpath("//input[@id='smb']")
        if new_height == last_height:
            if len(show_more_result_buttons) > 0:
                try:
                    show_more_result_buttons[0].click()
                    sleep(1)
                except (Exception, ) as e:
                    break
            else:
                break
        last_height = new_height


def _meta_dict_to_urls(dict_):
    image_url = dict_['ou']
    hp_url = dict_['ru']
    return image_url, hp_url


if __name__ == '__main__':
    search_word = "社是"
    url = f"https://www.google.co.jp/search?q={search_word}&tbm=isch"
    pprint(get_raw_meta_texts(url))
