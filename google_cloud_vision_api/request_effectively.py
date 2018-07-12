try:
    import merge_img
    import parse_merged_text_result
    import recognize_captcha
except (Exception, ) as e:
    from . import merge_img
    from . import parse_merged_text_result
    from . import recognize_captcha
from tqdm import tqdm
import difflib
# #


def send_as_one_responce(pil_image_dict):
    widths = {path: image.size[0] for path, image in pil_image_dict.items()}
    width_sorted_paths = sorted(list(widths.items()), key=lambda x: x[1])
    for path, width in width_sorted_paths:
        merge_img.merge_img(pil_image_dict)
        parse_merged_text_result.parse_image(heightsum_list, textAnnotations)


def recv_detection(paths, try_cnt=0):
    text_dict, match_ratio_dict = get_text_dict_cheaply(paths)
    try_cnt += min([len(paths), 2])
    if max(match_ratio_dict.values()) > 0.6:
        return text_dict

    perfect_path = [path for path,
                    ratio in match_ratio_dict.items() if ratio == 1][0]
    perfect_text = text_dict[perfect_path]
    rest_paths = [path for path in paths if path != perfect_path]
    new_text_dict = {perfect_path: perfect_text, }
    if len(rest_paths) <= 2:
        new_text_dict.update(get_text_dict(rest_paths))
        try_cnt += len(rest_paths)
    else:
        rest_paths_half0 = rest_paths[:len(rest_paths) // 2]
        rest_paths_half1 = rest_paths[len(rest_paths) // 2:]
        new_text_dict.update(recv_detection(rest_paths_half0))
        try_cnt += min([len(paths), 2])
        new_text_dict.update(recv_detection(rest_paths_half1))
        try_cnt += min([len(paths), 2])
    return new_text_dict


def get_text_dict(paths):
    text_dict = {}
    json_result = recognize_captcha.get_json_result([paths, ])
    for response, path in zip(json_result["responses"], paths):
        if response and 'error' not in response.keys():
            text_dict[path] = response["textAnnotations"][0]['description']
        else:
            if 'error' not in response.keys():
                pprint(response)
            text_dict[path] = "__empty__"
    return text_dict


def check_ratio(path0, text0):
    check_text = get_text_dict(paths=[path0, ])[0]
    ratio = get_match_ratio(string0=text0, string1=check_text)
    return ratio


# if len(paths) <= 2:
#     texts = recognize_captcha.get_text_result(paths)
#     return {p: t for p, t in zip(paths, texts)}
#
# # print(img_dict)
def get_text_dict_cheaply(paths):
    if len(paths) <= 2:
        text_dict = get_text_dict(paths)
        match_ratio = 1
        match_ratio_dict = {path: 1 for path in paths}
        return text_dict, match_ratio_dict

    img_dict = merge_img.gen_img_dict(paths)
    merged_image = merge_img.merge_img(img_dict)
    # merged_image.save("merged_image.png", format="PNG")
    heightsum_list = merge_img.gen_heightsum_list(img_dict)
    json_ = recognize_captcha.get_json_result([merged_image, ])
    textAnnotations = json_["responses"][0]["textAnnotations"]
    text_dict = parse_merged_text_result.parse_image(
        heightsum_list, textAnnotations)
    most_long_text_path, most_long_text = sorted([(path, len(
        text)) for path, text in text_dict.items()], key=lambda x: x[1], reverse=True)[0]
    most_long_text_accurate = get_text_dict(paths=[most_long_text_path, ])[
        most_long_text_path]
    match_ratio = get_match_ratio(most_long_text, most_long_text_accurate)
    match_ratio_dict = {most_long_text_path: match_ratio}
    return text_dict, match_ratio_dict


def get_match_ratio(string0, string1):
    return difflib.SequenceMatcher(None, string0, string1).ratio()


if __name__ == '__main__':
    paths = ["test.jpg", "test1.gif",   "test0.gif",  "test2.png", ]
    text_dict = get_text_dict_cheaply(paths)
    print(text_dict)
