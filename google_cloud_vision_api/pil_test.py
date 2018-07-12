

def get_filesize_without_save():
    from PIL import Image
    from io import BytesIO
    image = Image.open("test.jpg", mode="r")
    format_types = ['jpeg', 'gif', 'png']
    for format_type in format_types:
        with BytesIO() as file_bytes:
            image.save(file_bytes, format=format_type)
            print(format_type, file_bytes.tell())


def send_pilimage_to_googleapi():
    from PIL import Image
    import base64
    import ast
    from traceback import print_exc
    from io import BytesIO
    images = []
    print(bool(type("test0.gif") is str))
    pil_image = Image.open("test0.gif", mode="r")
    print(type(pil_image))
    raise
    file_bytes = BytesIO()
    pil_image.save(file_bytes, format="png")
    image = {'content': base64.b64encode(
        file_bytes.getbuffer()).decode("UTF-8")}
    images.append(image)
    from recognize_captcha import post_request
    raw_response = post_request(images)
    post_request(images)
    raw_response.raise_for_status()
    dumped = ast.literal_eval(raw_response.text)
    try:
        for response in dumped["responses"]:
            print(response["textAnnotations"][0]['description'])
    except (Exception, ) as e:
        print_exc()
        print(raw_response.text)


if __name__ == '__main__':
    # get_filesize_without_save()
    send_pilimage_to_googleapi()
