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
