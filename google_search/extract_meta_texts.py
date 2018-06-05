from chrome_wrapper import Chrome, Keys
import csv_wrapper
import sys
from traceback import format_exc
from time import sleep
import os


def _scroll_google_search_to_the_bottom(c):
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


def _gen_url(i):
    list_of_list = csv_wrapper.xlsx_to_list_of_list("combined_names.xlsx")
    search_words = [x[0] for x in list_of_list]
    if i >= len(search_words):
        return False
    search_word = search_words[i]
    if len(search_word) < 5:
        return False
    url = f"https://www.google.co.jp/search?q={search_word}&tbm=isch"
    print(search_word)
    return url


def get_raw_meta_texts(i):
    print('get_raw_meta_texts', i)
    url = _gen_url(i)
    if not url:
        return
    print('running Chrome...')
    c = Chrome()
    c.get(url)
    _scroll_google_search_to_the_bottom(c)
    print('exacting by xpath...')
    elements = c.xpath_lxml('//*[@class = "rg_meta notranslate"]')
    raw_meta_texts = list(map(lambda x: x.text_content(), elements))
    c.quit()
    _save_as_excel(i, raw_meta_texts)
    with open(f'result_report.txt', 'a') as f:
        text = f'index{i} wrote {len(raw_meta_texts)} meta datas\n'
        f.write(text)
        print(text)


def _save_as_excel(i, raw_meta_texts):
    print('saving as excel...')
    filename = f'result/raw_meta_texts{i}.xlsx'.replace('/', os.sep)
    list_of_list = map(lambda x: [x, ], raw_meta_texts)
    csv_wrapper.xlsx_from_list_of_list(filename, list_of_list)


if __name__ == '__main__':
    args = sys.argv
    this_filename, i = args
    get_raw_meta_texts(int(i))
