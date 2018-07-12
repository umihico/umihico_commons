import ast
# from mother import passwords
import base64
import json
from requests import post
from passpacker import passwords
from pprint import pprint
from io import BytesIO


def print_texts(texts):
    [print(f"{text[:10]}...{text[len(text)-10:]}".replace('\n', ''))
     for text in texts]


def post_request(images):
    request_list = [
        {'image': image, 'features': [
            {'type': "TEXT_DETECTION", 'maxResults': 1000}]}
        for image in images]
    json_data = json.dumps({'requests': request_list})
    url = "https://vision.googleapis.com/v1/images:annotate?key="
    api_key = passwords['google_cloud_vision_api']
    headers = {'Content-Type': 'application/json'}
    raw_response = post(url + api_key, data=json_data, json=headers)
    raw_response.raise_for_status()
    return raw_response


def _encode_image(image):
    return {'content': base64.b64encode(image).decode("UTF-8")}


def _to_image(data):
    if bool(type(data) is str):
        if data.startswith("http"):
            image = {"source": {'imageUri': data}}  # url
        else:
            image = _encode_image(open(data, 'rb').read())  # local path
    else:
        f = BytesIO()
        data.save(f, format="png")  # data was pil_image
        content = f.getbuffer()
        # f.close()
        image = _encode_image(content)
    return image


def get_json_result(datas):
    images = [_to_image(data) for data in datas]
    raw_response = post_request(images)
    dumped = ast.literal_eval(raw_response.text)
    return dumped


def get_text_result(datas):
    dumped = get_json_result(datas)
    try:
        texts = []
        for response, path in zip(dumped["responses"], datas):
            if response and 'error' not in response.keys():
                texts.append(response["textAnnotations"][0]['description'])
            else:
                if 'error' in response:
                    print(path)
                    pprint(response)
                texts.append("empty")
        return True, texts
    except (Exception, ) as e:
        # print(obj_response.text)
        raise
        return False, obj_response.text
        # return obj_response.text


def gen_ocr_pair_on_new_xlsx(urls_xlsx_path, save_filename):
    from umihico_commons.csv_wrapper import xlsx_from_list_of_list, xlsx_to_list_of_list
    from tqdm import tqdm
    list_of_list = xlsx_to_list_of_list(urls_xlsx_path)
    urls = [list_[0] for list_ in list_of_list]
    del list_of_list
    url_chunk = []
    output_list_of_list = []
    for url in tqdm(urls):
        url_chunk.append(url)
        if len(url_chunk) == 16 or url == urls[-1]:
            success_bool, texts = recognize_captcha(url_chunk)
            if success_bool:
                print_texts(texts)
                output_list_of_list.extend(list(zip(url_chunk, texts)))
                xlsx_from_list_of_list(save_filename, output_list_of_list)
                url_chunk.clear()
            else:
                for url0 in url_chunk:
                    success_bool, texts = recognize_captcha([url0, ])
                    if success_bool:
                        print_texts(texts)
                        output_list_of_list.append((url0, texts[0]))
                    else:
                        """this was the bad one. keep rest in chunk"""
                        index_ = url_chunk.index(url0)
                        url_chunk = url_chunk[index_ + 1:]
                        if url != urls[-1]:
                            break


if __name__ == '__main__':
    text = get_text_result(
        ["test1.gif",   "test0.gif",  "test2.png", ])
    # ["http://brightcove04.o.brightcove.com/1764166205001/1764166205001_5629748977001_5629752425001-vs.jpg?pubId=1764166205001", ])
    print(text)
    # recognize_captcha("sosiki_tate.png")
    # load_data()
