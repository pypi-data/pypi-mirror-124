from flask.json import tag


def hello_world():
    print("Hello World!")


def date1910():
    print(tag.datetime(2021, 10, 19))