import json
import datetime


def read_json_file(fn):
    """
    Функция открывает JSON-файл и сохраняет его в список paymnt
    :type fn: имя файла
    """
    # paymnt = {}
    with open(fn) as f:
        paymnt = json.load(f)

    return paymnt

def get_date(dt):
    """
    Функция выделяет дату из строки
    :param dt: строка типа: '2019-12-08T22:46:21.935582'
    :return: дата в формате 'YYYY-mm-dd'
    """
    date_time_obj = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f')
    dt_str = date_time_obj.date()
    return dt_str


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
    elif ''.join(c if c.isdigit() else '' for c in src) == '':
        m_value = 'Нет данных'
    elif "Счет" in src:
        account = ''.join(c if c.isdigit() else '' for c in src)
        m_value = '**' + account[-4:]
    elif (not (not ('Visa' in src) and not ('Maestro' in src) and not (
            'Master' in src))):
        account = ''.join(c if c.isdigit() else '' for c in src)
        m_value = account[-16:-12] + ' ' + account[-12:-10] + '** **** **** ' + account[-4:]
    else:
        m_value = src

    return m_value

def lastoperations(fn: object) -> object:
    """
    функция выводит на экран список из 5 последних выполненных
    клиентом операций в формате:
    <дата перевода> <описание перевода>
    <откуда> -> <куда>
    <сумма перевода> <валюта>
    """
    payments: list = read_json_file(fn)
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
