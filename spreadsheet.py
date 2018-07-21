from ast import literal_eval
from oauth2client.service_account import ServiceAccountCredentials
from passpacker import passwords
import gspread


def _load_dict_from_passpacker():
    return literal_eval(passwords["spreadsheet_json"])


def _authorize(jsondict=None):
    jsondict = jsondict or _load_dict_from_passpacker()
    print('authorizing...')
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        jsondict, scope)
    gc = gspread.authorize(credentials)
    return gc


def _open_spreadsheet(url, jsondict=None):
    gc = _authorize(jsondict)
    book = gc.open_by_url(url)
    return book


def open_worksheet(url, jsondict=None, sheetindex=0):
    book = _open_spreadsheet(url, jsondict)
    worksheet = book.get_worksheet(sheetindex)
    worksheet._update_cells = _update_cells
    return worksheet


def _update_cells(self, rows_cols_values_list):
    """
    for row, col, value in list(zip(*rows_cols_values_list)):
        cell(row, col).value = value
    """
    rows, cols, values = list(zip(*rows_cols_values_list))
    cell_list = []
    for row, col, value in zip(rows, cols, values):
        cell = self.cell(row + 1, col + 1)
        cell.value = value
        cell_list.append(cell)
    self.update_cells(cell_list)


if __name__ == '__main__':
    book_url = "https://docs.google.com/spreadsheets/d/15URyeuU9yUkk5hoj5p69AxOVFtu1e5JRdA0c-G_p2io/edit#gid=0"
    from pprint import pprint
    update_cell(book_url, 7, 7, 'test')
    pprint(load_spreadsheet(book_url))
