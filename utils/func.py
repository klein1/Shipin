import datetime
import os.path

def random_name():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def file_extension(path):
    # print(os.path.splitext(path)[1])
    return os.path.splitext(path)[1]

def now():
    # return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')