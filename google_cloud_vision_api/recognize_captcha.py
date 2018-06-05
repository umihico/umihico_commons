import ast
# from mother import passwords
import base64
import json
from requests import post
from passpacker import passwords
from pprint import pprint


def print_texts(texts):
    [print(f"{text[:10]}...{text[len(text)-10:]}".replace('\n', ''))
     for text in texts]


def recognize_captcha(image_path_list):
    images = []
    for path in image_path_list:
        if path.startswith("http"):
            image = {"source": {'imageUri': path}}
        else:
            image = {'content': base64.b64encode(
                open(path, 'rb').read()).decode("UTF-8")}
        images.append(image)
    request_list = [
        {'image': image, 'features': [
            {'type': "TEXT_DETECTION", 'maxResults': 100}]}
        for image in images]
    # request_list = [
    #     {'image': {'content': ef}, 'features': [
    #         {'type': "TEXT_DETECTION", 'maxResults': 100}]}
    # for ef in encode_files]
    json_data = json.dumps({'requests': request_list})
    url = "https://vision.googleapis.com/v1/images:annotate?key="
    api_key = passwords['google_cloud_vision_api']
    headers = {'Content-Type': 'application/json'}

    print("Google Cloud Vision Api...", end='')
    obj_response = post(url + api_key, data=json_data, json=headers)
    print("end request")
    try:
        obj_response.raise_for_status()
        dumped = ast.literal_eval(obj_response.text)
        texts = []
        for response, path in zip(dumped["responses"], image_path_list):
            if response and 'error' not in response:
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
    text = recognize_captcha(
        #     # ["test.jpg", "test2.png", "http://www.tokai-com.co.jp/company/images/soshikizu_img01.gif", "large.jpg", "http://www.flowersinspace.com/img/lean-to-greenhouse/_thumb/mind-santa-barbara-montecito-x-greenhouse-santa-barbara-montecito-x-greenhouse-free-shipping_lean-to-greenhouse_250x250.jpg"])
        ["http://brightcove04.o.brightcove.com/1764166205001/1764166205001_5629748977001_5629752425001-vs.jpg?pubId=1764166205001", ])
    print(text)
    # recognize_captcha("sosiki_tate.png")
    # load_data()
