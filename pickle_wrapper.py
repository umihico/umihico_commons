import pickle
# import csv_wrapper
import os


def parse_dir_filename(filename):
    # r"C:\Users\umi\GoogleDrive\code\crowdworks\ceoinfo\test.csv"
    # ('C:\\Users\\umi\\GoogleDrive\\code\\crowdworks\\ceoinfo', 'test.csv')
    # path = r"test.csv"
    # ('', 'test.csv')
    return os.path.split(filename)


def split_filetype(filename):
    return os.path.splitext(filename)


def save(path, data):
    with open(path, mode='wb') as f:
        pickle.dump(data, f)


def load(path):
    with open(path, mode='rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    path = r"C:\Users\umi\GoogleDrive\code\crowdworks\ceoinfo\test.csv"
    path = r"test.csv"
    print(split_filetype(path))
