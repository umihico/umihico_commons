from requests import get
from io import BytesIO
from PIL import Image


def _url_to_image(url):
    img = Image.open(BytesIO(get(url).content))
    return img


def _path_to_image(path):
    img = Image.open(path)
    return img


def to_image(path):
    return _url_to_image(path) if path.startswith('http') else _path_to_image(path)
