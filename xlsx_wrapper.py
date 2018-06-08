import xlsxwriter
import xlrd


def load_xlsx(filename):
    xl_workbook = xlrd.open_workbook(filename)
    xl_sheet = xl_workbook.sheet_by_index(0)
    row = xl_sheet.row(0)  # 1st row
    nrows = xl_sheet.nrows
    ncols = xl_sheet.ncols
    list_of_list = []
    for row_index in range(0, nrows):
        list_ = []
        for col_index in range(0, ncols):
            cell_str = str(xl_sheet.cell(row_index, col_index).value)
            list_.append(cell_str)
        list_of_list.append(list_)
    return list_of_list


def to_xlsx(filename, list_of_list):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    for row_index, row in enumerate(list_of_list):
        for col_index, cell in enumerate(row):
            worksheet.write(row_index, col_index, cell)
