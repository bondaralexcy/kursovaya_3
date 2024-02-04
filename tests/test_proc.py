import pytest

from src import proc
import datetime
"""
Тесты
"""
def test_get():
    assert proc.get_date('2019-12-08T22:46:21.935582') == datetime.date(2019, 12, 8)

def test_incription():
    assert proc.inscription('Maestro') == 'Нет данных'
    assert proc.inscription('Счет 38611439522855669794') == '**9794'
    assert proc.inscription('Visa Classic 2842878893689012') == '2842 87** **** **** 9012'
    assert proc.inscription('') == 'Нет данных'
    assert proc.inscription(None) == 'Наличные'