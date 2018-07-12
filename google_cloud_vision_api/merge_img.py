from PIL import Image
import requests
from io import BytesIO


def _url_to_pil(url):
    img = Image.open(BytesIO(requests.get(url).content))
    return img


def _path_to_pil(path):
    img = Image.open(path)
    return img


def gen_img(url_or_path):
    if url_or_path.startswith('http'):
        img = _url_to_pil(url=url_or_path)
    else:
        img = _path_to_pil(path=url_or_path)
    return img


def gen_img_dict(paths):
    img_dict = {}
    for path in paths:
        try:
            img_dict[path] = gen_img(path)
        except (Exception, ) as e:
            print(path)
            print(e)
    return img_dict


def gen_height_dict(img_dict):
    height_dict = {}
    print(img_dict)
    for path, img in img_dict.items():
        width, height = img.size
        height_dict[path] = height
    return height_dict


def gen_heightsum_list(img_dict):
    height_dict = gen_height_dict(img_dict)
    height_list = list(height_dict.items())
    height_list.sort(key=lambda x: x[1], reverse=False)
    heightsum_list = []
    sum_ = 0
    for path, height in height_dict.items():
        sum_ += height
        heightsum_list.append((path, sum_))
    return heightsum_list


def _gen_plain_background(img_dict):
    background_width = max(
        [w for w, h in [img.size for img in img_dict.values()]])
    heightsum_list = gen_heightsum_list(img_dict)
    background_height = heightsum_list[-1][1]
    background = Image.new('RGB', (background_width, background_height))
    return background


def merge_img(img_dict):
    plain_background = _gen_plain_background(img_dict)
    height_dict = gen_height_dict(img_dict)
    heightsum_list = gen_heightsum_list(img_dict)
    for path, heightsum in heightsum_list:
        img = img_dict[path]
        paste_end_height = heightsum
        paste_start_height = paste_end_height - height_dict[path]
        plain_background.paste(img, (0, paste_start_height))
    merged_image = plain_background
    return merged_image


if __name__ == '__main__':
    paths = ["test.jpg", "test2.png", ]
    img_dict = gen_img_dict(paths)
    merged_image = merge_img(img_dict)
    merged_image.save("merged_image.png", format="PNG")
