from ast import literal_eval
from oauth2client.service_account import ServiceAccountCredentials
from passpacker import passwords
import gspread


def _load_dict_from_passpacker():
    return literal_eval(passwords["spreadsheet_json"])


gc = False


def authorize(jsondict=None):
    jsondict = jsondict or _load_dict_from_passpacker()
    global gc
    if gc:
        return gc
    print('authorizing...')
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        jsondict, scope)
    gc = gspread.authorize(credentials)
    return gc


def _open_spreadsheet(url, jsondict=None):
    gc = authorize(jsondict)
    book = gc.open_by_url(url)
    worksheet = book.get_worksheet(0)
    return worksheet


def load_spreadsheet(url, jsondict=None):
    """return values by list of list"""
    worksheet = _open_spreadsheet(url, jsondict)
    return worksheet.get_all_values()


def update_cell(url, row, col, value, jsondict=None):
    worksheet = _open_spreadsheet(url, jsondict)
    worksheet.update_cell(row + 1, col + 1, value)


def update_cells(url, rows, cols, values, jsondict=None):
    worksheet = _open_spreadsheet(url, jsondict)
    cell_list = []
    for row, col, value in zip(rows, cols, values):
        cell = worksheet.cell(row + 1, col + 1)
        cell.value = value
        cell_list.append(cell)
    worksheet.update_cells(cell_list)


if __name__ == '__main__':
    book_url = "https://docs.google.com/spreadsheets/d/15URyeuU9yUkk5hoj5p69AxOVFtu1e5JRdA0c-G_p2io/edit#gid=0"
    from pprint import pprint
    update_cell(book_url, 7, 7, 'test')
    pprint(load_spreadsheet(book_url))
