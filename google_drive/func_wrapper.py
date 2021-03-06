from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


def _get_mine_type(filename):
    # print(filename)
    filename_wo_type, filetype = os.path.splitext(filename)
    mine_types_dict = {
        "xls": 'application/vnd.ms-excel',
        "xlsx": 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        "xml": 'text/xml',
        "ods": 'application/vnd.oasis.opendocument.spreadsheet',
        "csv": 'text/plain',
        "tmpl": 'text/plain',
        "pdf": 'application/pdf',
        "php": 'application/x-httpd-php',
        "jpg": 'image/jpeg',
        "png": 'image/png',
        "gif": 'image/gif',
        "bmp": 'image/bmp',
        "txt": 'text/plain',
        "doc": 'application/msword',
        "js": 'text/js',
        "swf": 'application/x-shockwave-flash',
        "mp3": 'audio/mpeg',
        "zip": 'application/zip',
        "rar": 'application/rar',
        "tar": 'application/tar',
        "arj": 'application/arj',
        "cab": 'application/cab',
        "html": 'text/html',
        "htm": 'text/html',
        "default": 'application/octet-stream',
        "folder": 'application/vnd.google-apps.folder', }
    return mine_types_dict[filetype[1:]]


def _gen_drive():
    settings_file_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'settings.yaml')
    gauth = GoogleAuth(settings_file=settings_file_path)
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)
    return drive


def upload_file(uploadingfile_fullpath, folder_id):
    # print(folder_id)
    drive = _gen_drive()
    # print(uploadingfile_fullpath)
    dirname, filename = os.path.split(uploadingfile_fullpath)
    minetype = _get_mine_type(filename)
    f = drive.CreateFile({'title': filename,
                          'mimeType': minetype,
                          'parents': [{'kind': 'drive#fileLink', 'id': folder_id}]})
    f.SetContentFile(uploadingfile_fullpath)
    f.Upload()
    # print(get_file_names(folder_id))
    print(f["title"], f["id"])


def get_file_names(folder_id):
    drive = _gen_drive()
    param = {'q': f"'{folder_id}' in parents"}
    file_list = drive.ListFile(param).GetList()
    filenames = [file1['title'] for file1 in file_list]
    return filenames


if __name__ == '__main__':
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)
    folder_id = '1Ol5I8Y6r2yuQxslL-4W_G1Tr6nNdfbrE'
    folder_id = '1cm7wTRz5co1LlJ1_6sd40f_iYMhrjoqD'
    param = {'q': f"'{folder_id}' in parents"}
    print(param)
    file_list = drive.ListFile(param).GetList()
    for file1 in file_list:
        # print(file1)
        print('title: %s, id: %s' % (file1['title'], file1['id']))

    f = drive.CreateFile({'title': 'test_excelfile.xlsx',
                          'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                          'parents': [{'kind': 'drive#fileLink', 'id': folder_id}]})
    f.SetContentFile('test_excelfile.xlsx')
    # f.Upload()
