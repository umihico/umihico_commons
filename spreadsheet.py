from passpacker import passwords
from ast import literal_eval
from oauth2client.service_account import ServiceAccountCredentials
import gspread


def _load_dict_from_passpacker():
    return literal_eval(passwords["spreadsheet_json"])


gc = False


def authorize():
    global gc
    if gc:
        return gc
    print('authorizing...')
    scope = ['https://spreadsheets.google.com/feeds']
    json_key = _load_dict_from_passpacker()
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        json_key, scope)
    gc = gspread.authorize(credentials)
    return gc


def _open_spreadsheet(url):
    gc = authorize()
    book = gc.open_by_url(book_url)
    worksheet = book.get_worksheet(0)
    return worksheet


def load_spreadsheet(url):
    """return values by list of list"""
    worksheet = _open_spreadsheet(url)
    return worksheet.get_all_values()


def update_cell(url, row, col, value):
    worksheet = _open_spreadsheet(url)
    worksheet.update_cell(row, col, value)


if __name__ == '__main__':
    book_url = "https://docs.google.com/spreadsheets/d/15URyeuU9yUkk5hoj5p69AxOVFtu1e5JRdA0c-G_p2io/edit#gid=0"
    from pprint import pprint
    update_cell(book_url, 7, 7, 'test')
    pprint(load_spreadsheet(book_url))
