import csv_wrapper
import os
import json


def _get_filenames():
    abspath_this = os.path.abspath(__file__)
    dirpath_here = os.path.dirname(abspath_this)
    meta_texts_dir = os.path.join(dirpath_here, 'result')
    return list(map(lambda x: os.path.join(meta_texts_dir, x),  os.listdir(meta_texts_dir)))


def _raw_meta_text_generator():
    filenames = _get_filenames()
    for filename in filenames:
        xlsx = csv_wrapper.xlsx_to_list_of_list(filename)
        yield from _raw_meta_text_generator_xlsx(xlsx)


def _raw_meta_text_generator_xlsx(xlsx):
    for row in xlsx:
        raw_meta_text = row[0]
        yield raw_meta_text


def _extract_urls_generator():
    raw_meta_text_generator = _raw_meta_text_generator()
    for meta_text in raw_meta_text_generator:
        dict_ = json.loads(meta_text)
        image_url, hp_url = _meta_dict_to_urls(dict_)
        yield image_url, hp_url


def _meta_dict_to_urls(dict_):
    image_url = dict_['ou']
    hp_url = dict_['ru']
    return image_url, hp_url


def create_filtered_url():
    hpurl_base_dict = {}
    extract_urls_generator = _extract_urls_generator()
    for urls in extract_urls_generator:
        if 'organization' not in ''.join(urls):
            continue
        image_url, hp_url = urls
        old_image_url = hpurl_base_dict[hp_url] if hp_url in hpurl_base_dict else 'dummy'
        new_image_url = old_image_url if 'organization' in old_image_url else image_url
        hpurl_base_dict[hp_url] = new_image_url
    texts = ['\t'.join([str(i), hp_url, image_url]) for i, (hp_url,
                                                            image_url) in enumerate(hpurl_base_dict.items())]
    combined_text = '\n'.join(texts)
    with open('urls.txt', 'w') as f:
        f.write(combined_text)


if __name__ == '__main__':
    create_filtered_url()
