

import json
from os import path
if __name__ == '__main__':
    file_path = path.join(path.dirname(
        path.abspath(__file__)), "result.json")
    with open(file_path, 'r') as f:
        raw_text = '\n'.join(f)
    # print(raw_text)
    d = json.loads(raw_text)
    textAnnotations = d["responses"][0]["textAnnotations"]
    [print(x.keys()) for x in textAnnotations]
    [print(x["description"]) for x in textAnnotations]
    print([d["responses"][0]["textAnnotations"][1], ])
    [{'description': 'Management', 'boundingPoly': {'vertices': [{'x': 547, 'y': 26}, {
        'x': 654, 'y': 26}, {'x': 654, 'y': 43}, {'x': 547, 'y': 43}]}}]

    for key0 in d.keys():
        print(key0)
        for index1, row in enumerate(d[key0]):
            print(key0, index1)
            for key2 in d[key0][index1]:
                print(key0, index1, key2)
                print(type(d[key0][index1][key2]))
