import pytest
import datetime

from src import proc


def test_get():
    assert proc.get_date('2019-12-08T22:46:21.935582') == datetime.date(2019, 12, 8)
    assert proc.get_date('2020-01-01T22:46:21.935582') == datetime.date(2020, 1, 1)
    assert proc.get_date('2020-01-01') == datetime.date(1900, 1, 1)
    assert proc.get_date('') == ''


def test_inscription():
    assert proc.inscription('Maestro') == 'Нет данных'
    assert proc.inscription('Счет 38611439522855669794') == 'Счет **9794'
    assert proc.inscription('Visa Classic 2842878893689012') == 'Visa Classic 2842 87** **** **** 9012'
    assert proc.inscription('') == 'Нет данных'
    assert proc.inscription(None) == 'Наличные'

def test_without_digit():
    assert proc.without_digit('1a2l3f4a') == 'alfa'
    assert proc.without_digit('Счет 1234567890') == 'Счет '
    assert proc.without_digit('Visa Classic 1234567890') == 'Visa Classic '
    assert proc.without_digit('1234567890') == ''

def test_without_alfa():
    assert proc.without_alfa('1a2l3f4a') == '1234'
    assert proc.without_alfa('Счет 1234567890') == '1234567890'
    assert proc.without_alfa('Visa Classic 1234567890') == '1234567890'
    assert proc.without_alfa('abc') == ''

def test_sort_list():
    assert proc.sort_list([]) == []
    assert proc.sort_list([{"id": 594226727, "state": "CANCELED"}]) == []
    assert proc.sort_list([{"id": 594226727, "state": "CANCELED"}]) == []
    assert proc.sort_list(
    [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        }
    ]
    ) == [[datetime.date(2019, 8, 26), 'Перевод организации', 'Maestro 1596837868705199', 'Счет 64686473678894779589', '31957.58', 'руб.']]


def test_read_json_file():
    assert proc.read_json_file('') == []
    assert proc.read_json_file('file.txt') == []


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        proc.read_json_file('file.json')


def test_lastoperations():
    assert proc.lastoperations('nofile.json') == []
    assert proc.lastoperations('file.txt') == []
    assert proc.lastoperations('noop.json') == []
    assert proc.lastoperations('') == []
