import csv
from time import sleep
try:
    from xlsx_wrapper import to_xlsx, load_xlsx
except (Exception, ) as e:
    from .xlsx_wrapper import to_xlsx, load_xlsx


def _open(path, mode):
    return open(path, mode, encoding='UTF-8', newline='')


# def _iter_common(old_rows, func):
#     for row in old_rows:
#         func(row)


def save_csv(path, list_of_list):
    with _open(path, mode='w') as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerows(list_of_list)


def load_csv(path):
    with _open(path, mode='r') as f:
        csv_ = csv.reader(f)
        rows = list(csv_)
    return rows


def xlsx_to_list_of_list(filename):
    print("using csv_wrapper.xlsx_to_list_of_list")
    print("new ver is xlsx_wrapper.load_xlsx")
    return load_xlsx(filename)


def xlsx_from_list_of_list(filename, list_of_list):
    print("using csv_wrapper.xlsx_from_list_of_list")
    print("new ver is xlsx_wrapper.to_xlsx")
    return to_xlsx(filename, list_of_list)


def convert_list_of_dicts_to_list_of_list(list_of_dict, missing_value='__NoValue__'):
    fieldnames = []
    for dict_ in list_of_dict:
        index_ = 0
        for key in dict_.keys():
            if key in fieldnames:
                index_ = fieldnames.index(key)
            else:
                index_ += 1
                fieldnames.insert(index_, key)
    list_of_list = [fieldnames, ]
    for dict_ in list_of_dict:
        row = [dict_.get(key, missing_value) for key in fieldnames]
        list_of_list.append(row)
    return list_of_list


def save_list_of_dict_as_excel(path, list_of_dict):
    list_of_list = convert_list_of_dicts_to_list_of_list(
        list_of_dict, missing_value='')
    save_list_of_list_as_excel(path, list_of_list)


def test_save_csv_list_of_dict():
    dictA = {'a': 0, 'c': 2}
    dictB = {'a': 0, 'b': 1}
    print(save_csv_list_of_dict('path', [dictA, dictB]))


def save_csv_dict(path, list_of_dict):
    fieldnames = set()
    for dict_ in list_of_dict:
        for key in dict_.keys():
            fieldnames.add(key)
    fieldnames = list(fieldnames)
    with _open(path, mode='w') as f:
        w = csv.DictWriter(f, fieldnames, restval="__NoValue__")
        fieldnames = {k: k for k in fieldnames}
        list_of_dict.insert(0, fieldnames)
        w.writerows(list_of_dict)


def load_csv_dict(path):
    with _open(path, mode='r') as f:
        csv_ = csv.DictReader(f)
        rows = []
        for row in csv_:
            row = dict(row)
            row = {k: v for k, v in row.items() if v != "__NoValue__"}
            rows.append(row)
    return rows


if __name__ == '__main__':
    test_save_csv_list_of_dict()
    raise
    test_file_name = 'test_csv.csv'
    list_of_list = [
        ['a', 'b', 'c'],
        ['1', '2', '3'],
    ]
    save_csv(test_file_name, list_of_list)
    print(load_csv(test_file_name))

    list_of_dict = [
        {'a': 'b', 'c': 'd'},
        {1: 2, 3: 4},
    ]
    save_csv_dict(test_file_name, list_of_dict)
    print(load_csv_dict(test_file_name))
