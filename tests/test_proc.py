from src import proc
import datetime


def test_get():
    assert proc.get_date('2019-12-08T22:46:21.935582') == datetime.date(2019, 12, 8)
