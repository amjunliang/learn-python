import zlib


def test_zlib():
    strtest = b"witch which has which witches wrist watch"
    assert len(zlib.compress(strtest)) < len(strtest)
    assert zlib.decompress(zlib.compress(strtest)) == strtest
    pass


import datetime


def test_datetime():
    print(datetime.date.today())
    i = datetime.date(2019, 5, 5)
    i.ctime()
    pass
