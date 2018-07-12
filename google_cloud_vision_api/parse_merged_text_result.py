try:
    import merge_img
except (Exception, ) as e:
    from . import merge_img
import bisect
# paths
# merged_file_path


def _parse_annotations(textAnnotations):
    full_text = textAnnotations[0]['description']
    each_words_heigths = []
    for textAnnotation in textAnnotations[1:]:
        text = textAnnotation["description"]
        pos_dicts = textAnnotation["boundingPoly"]["vertices"]
        end_heigths = max([pos_dict['y'] for pos_dict in pos_dicts])
        each_words_heigths.append((text, end_heigths))
    return full_text, each_words_heigths
    # print([d["responses"][0]["textAnnotations"][1], ])
    # [{'description': 'Management', 'boundingPoly': {'vertices': [{'x': 547, 'y': 26}, {'x': 654, 'y': 26}, {'x': 654, 'y': 43}, {'x': 547, 'y': 43}]}}]


def to_sentence(full_text, each_words_heigths):
    each_texts_heigths = []
    full_text_list = full_text.split('\n')
    for sentence in full_text_list:
        if not sentence:
            continue
        # else:
        #     print(sentence, True)
        copy_sentence = sentence
        heigths = []
        for i, (word, heigth) in enumerate(each_words_heigths):
            if word in copy_sentence:
                heigths.append(heigth)
                copy_sentence = copy_sentence.replace(word, "", 1)
            else:
                each_words_heigths = each_words_heigths[i:]
                break
        # print([sentence, ])
        # print(each_words_heigths)
        ave_heigth = sum(heigths) / len(heigths)
        each_texts_heigths.append((sentence, ave_heigth))
    return each_texts_heigths


def parse_image(heightsum_list, textAnnotations):
    full_text, each_words_heigths = _parse_annotations(textAnnotations)
    print(full_text)
    each_texts_heigths = to_sentence(full_text, each_words_heigths)
    textlist_dict = {path: [] for path, h in heightsum_list}
    heightsums = [h for w, h in heightsum_list]
    for text, height in each_texts_heigths:
        idx = bisect.bisect_left(heightsums, height)
        path = heightsum_list[idx][0]
        textlist_dict[path].append(text)
    text_dict = {path: '\n'.join(text_list)
                 for path, text_list in textlist_dict.items()}
    return text_dict


if __name__ == '__main__':
    from PIL import Image
    img = Image.open("test.jpg")
    w, h = img.size
    dummy_heightsum_list = [("filename0", int(h / 2)), ("filename1", h)]
    from os import path as os_path
    import json
    file_path = os_path.join(os_path.dirname(
        os_path.abspath(__file__)), "result.json")
    raw_text = '\n'.join(open(file_path, 'r'))
    textAnnotations = json.loads(raw_text)["responses"][0]["textAnnotations"]
    print(parse_image(dummy_heightsum_list, textAnnotations))
