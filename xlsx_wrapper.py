import xlsxwriter
import xlrd


def load_xlsx(filename):
    xl_workbook = xlrd.open_workbook(filename)
    return _load_xlsx(xl_workbook)


def _load_xlsx(xl_workbook):
    xl_sheet = xl_workbook.sheet_by_index(0)
    nrows = xl_sheet.nrows
    ncols = xl_sheet.ncols
    rows = []
    for row_index in range(0, nrows):
        row = []
        for col_index in range(0, ncols):
            cell_value = str(xl_sheet.cell(row_index, col_index).value)
            row.append(cell_value)
        rows.append(row)
    return rows


def to_xlsx(filename, list_of_list):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    for row_index, row in enumerate(list_of_list):
        for col_index, cell in enumerate(row):
            worksheet.write(row_index, col_index, cell)
    workbook.close()


def _gen_fieldnames(ordereddicts):
    fieldnames = []
    for ordereddict in ordereddicts:
        index = 0
        for key in ordereddict.keys():
            if key in fieldnames:
                index = fieldnames.index(key)
            else:
                fieldnames.insert(index + 1, key)
                index = fieldnames.index(key)
    return fieldnames


def dicts_to_xlsx(filename, list_of_dict, fill_string="", add_fieldnames=False):
    fieldnames = _gen_fieldnames(list_of_dict)
    list_of_list = []
    if add_fieldnames:
        list_of_list.append(fieldnames)
    for d in list_of_dict:
        list_of_list.append([d.get(fn, fill_string) for fn in fieldnames])
    to_xlsx(filename, list_of_list)


if __name__ == '__main__':
    from collections import OrderedDict
    d0 = OrderedDict()
    d0["a"] = 1
    d0["b"] = 1
    d0["d"] = 1
    d1 = OrderedDict()
    d1["a"] = 1
    d1["b"] = 1
    d1["c"] = 1
    d1["d"] = 1
    print(_gen_fieldnames(ordereddicts=[d0, d1]))
