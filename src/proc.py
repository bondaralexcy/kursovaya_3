import json
import datetime
import os

def lastoperations(fn: str) -> object:
    """
    функция выводит на экран список из 5 последних выполненных
    клиентом операций в формате:
    <дата перевода> <описание перевода>
    <откуда> -> <куда>
    <сумма перевода> <валюта>
    """

    if os.path.exists(fn):
        payments: list = read_json_file(fn)
        if payments != []:
            sorted_pay = sort_list(payments)
            i = 0
            print()
            while i < 5:
                m_from = inscription(sorted_pay[i][2])
                m_to = inscription(sorted_pay[i][3])
                dt_string = sorted_pay[i][0].strftime("%d.%m.%Y")
                print(f"{dt_string} {sorted_pay[i][1]}")
                print(f"{m_from} -> {m_to}")
                print(f"{sorted_pay[i][4]} {sorted_pay[i][5]}")
                print()
                i += 1
        else:
            return []

    else:
        return []


def read_json_file(fn):
    """
    Функция открывает и читает JSON-файл в кодировке utf-8 и сохраняет его в список paymnt
    :type fn: имя файла
    """

    if fn[-4:] == 'json':
            with open(fn, "r", encoding="utf-8") as f:
                # загружаем структуру из файла
                paymnt = json.load(f)

            return paymnt

    else:
        return []


def get_date(dt):
    """
    Функция выделяет дату из строки
    :param dt: строка типа: '2019-12-08T22:46:21.935582'
    :return: дата в формате 'YYYY-mm-dd'
    """
    if len(dt) == len('2019-12-08T22:46:21.935582'):
        date_time_obj = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f')
        dt_str = date_time_obj.date()
        return dt_str

    elif dt == '':
        return ''

    else:
        return datetime.date(1900, 1, 1)


def sort_list(pnmt):
    """
    Функция выбирает нужные поля из списка выполненных операций (EXECUTED)
    и сортирует его по убыванию по первому полю (Дата операции)
    :param pnmt: список операций
    :return: отсортированный список операций
    """
    last_payments = []
    lp = []
    for pay in pnmt:
        if pay.get('state') == "EXECUTED":
            lp = [get_date(pay.get('date')), pay.get('description'), pay.get('from'), pay.get('to'),
                  pay.get('operationAmount')['amount'], pay.get('operationAmount')['currency']['name']]
            last_payments.append(lp)
        else:
            continue

    last_payments.sort(key=lambda x: x[0], reverse=True)
    return last_payments


def inscription(src):
    """
    Функция закрывает информацию о номере счета или карты
    """
    m_value = ""

    if src is None:
        m_value = 'Наличные'
    elif without_alfa(src) == '':
        m_value = 'Нет данных'
    elif "Счет" in src:
        account = without_alfa(src)
        m_value = without_digit(src) + '**' + account[-4:]
    elif (not (not ('Visa' in src) and not ('Maestro' in src) and not (
            'Master' in src))):
        account = without_alfa(src)
        m_value = without_digit(src) + account[-16:-12] + ' ' + account[-12:-10] + '** **** **** ' + account[-4:]
    else:
        m_value = src

    return m_value


def without_digit(st):
    """
    Функция извлекает из строки только буквы и пробелы

    """
    new_s = ''.join([a for a in st if a.isalpha() or a ==' '])
    return new_s


def without_alfa(st):
    """
    Функция извлекает из строки только цифры
    """
    new_s = ''.join(c if c.isdigit() else '' for c in st)
    return new_s


lastoperations('file.txt')