'''
Библиотека для работы с моделями машинного обучения в производственной среде

V0.01
21.10.2021
'''

try:
    import PIconnect as PI # библиотека для подключения к PI-System
except:
    import PIconnect as PI # на случай бага с ошибкой первого импорта
import pandas as pd
import numpy as np

PORPHYRY_VERSION = '0.01'
server = PI.PIServer()

def check_server():
    '''
    Проверка подключения к серверу PI-System
    '''

    print(server)


def check_tags(tags):
    '''
    Функция для проверки корректности заполнения словаря с тэгами.

    Args:
        tags (dict): словарь, состоящий из ключей в виде кратких названий колонок и значений в виде имен тэгов
    Returns:
        None
    '''
    
    for name in tags:
        print(name, server.search(tags[name])[0])


def dataset(tags, start, end, interval='5m', fix=False, step=10, tz='Asia/Tashkent'):
    """
    Функция для выгрузки данных из PI-System в виде объекта Pandas DataFrame.

    Args:
        tags (dict): словарь, состоящий из ключей в виде кратких названий колонок и значений в виде имен тэгов
        start (str): дата начала выгрузки в формате YYYY-MM-DD
        end (str): дата окончания выгрузки в формате YYYY-MM-DD
        interval (int): дискретность данных. например, 1h, 1m, 1d
        fix (bool): фиксированное значение, соответствующее дате start
        step (int): максимальное количество дней для одного запроса к базе данных
        tz (str): регион для определения часового пояса, например 'Asia/Tashkent'
    Returns:
        dataset (Pandas DataFrame):

    Example:

    tags = {'P1': 'tag_1', 'P2': 'tag_2'}
    data = dataset(tags=tags, start='2021-01-01', end='2021-02-01', intarval='1m', fix=False, step=30, tz='Asia/Tashkent')
    print(data)
    """

    start_step = pd.to_datetime(start)
    end_step = pd.to_datetime(end)
    step = pd.to_timedelta(str(step) + ' day')
    current_date = start_step
    dataset = pd.DataFrame()

    while current_date < end_step: # цикл входа в очередной промежуток времени
        current_start = current_date
        current_end = current_start + step
        current_date = current_start + step
        fraction = pd.DataFrame()

        if current_date > end_step: # приводит к фактической дате завершения
            current_end = end_step

        for name in tags: # датафрейм из всех тэгов
            point = server.search(tags[name])[0]
            data = point.interpolated_values(str(current_start), str(current_end), interval)
            data.index = data.index.tz_convert(tz) # исходно в GMT+0, переводим в GMT+5
            fraction = pd.concat([fraction, data], axis=1)

        fraction.columns = tags.keys()
        dataset = dataset.append(fraction)
        print(current_end.date(), end=' ') # прогрессбар
    if fix == True:
        dataset = dataset.head(1)
    
    return dataset


def current_values(tags):
    '''
    Функция для выгрузки данных из PI-System в виде объектов Pandas DataFrame.

    Args:
        tags (dict): словарь, состоящий из ключей в виде кратких названий колонок и значений в виде имен тэгов
        start (str): дата начала выгрузки в формате YYYY-MM-DD
        end (str): дата окончания выгрузки в формате YYYY-MM-DD
        interval (int): дискретность данных
        step (str): максимальное количество дней для одного запроса к базе данных
        dropna (bool): удаление пропусков в данных
    Returns:
        dataset (pandas dataframe): 
    '''
    data = pd.DataFrame(index=['current'])
    for name in tags:
        point = server.search(tags[name])[0]
        data[name] = point._current_value()
    return data