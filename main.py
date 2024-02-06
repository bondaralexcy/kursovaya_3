from src.proc import lastoperations
"""
Вызов функции lastoperations
"""
if __name__ == '__main__':
    """
    Вызов функции lastoperations - 
    вывод 5 последних операций из файла проводок
    """
    print("Последние 5 операций из json-файла")
    lastoperations('operations.json')
