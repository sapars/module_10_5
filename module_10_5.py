import os
from time import time, strftime, localtime
from multiprocessing import Pool, Process

# 7.799663066864014
folder = 'files_10_5'
files = [f'{folder}\\{file}' for file in os.listdir(folder)]


def read_info(name):
    '''
    Создайте функцию read_info(name), где name - название файла. Функция должна:
    Создавать локальный список all_data.
    Открывать файл name для чтения.
    Считывать информацию построчно (readline), пока считанная строка не окажется пустой.
    Во время считывания добавлять каждую строку в список all_data.
    '''
    all_data = []
    with open(name, 'r') as file:
        line = file.readline()
        while line:
            all_data.append(line.strip())
            line = file.readline()
    return all_data


def log_decorator(func):
    def wrapper(*args, **kwargs):
        # верхний колонтитул
        start = time()
        print('---------------------------')
        print(f'Начало работы {func.__name__}: {strftime('%H:%M:%S', localtime())}')
        print(f'Описание функции: {func.__doc__}')

        # вызов функции
        result = func(*args, **kwargs)

        # нижний колонтитул
        end = time()
        print('---------------------------')
        print(f'Завершение работы {func.__name__}: {strftime('%H:%M:%S', localtime())}')
        print("Время выполнения", end - start)
        print()
        return result

    return wrapper


@log_decorator
def single_process(files):
    '''Вызов функции read_info для каждого файла по очереди (линейно)'''
    for file in files:
        read_info(file)


@log_decorator
def pool_process(files):
    """Вызов функции read_info для каждого файла одновременно (параллельно)"""
    # При запуске процессов время выполнения сокращается в 2 раза
    p = []
    for file in files:
        p.append(Process(target=read_info, args=(file,)))
    for process in p:
        process.start()
    for process in p:
        process.join()
    # для Pool время выполнения в среднем в 3 раза выше, чем при линейной реализации
    # with Pool(processes=4) as pool:
    #     pool.map(read_info, files)


if __name__ == '__main__':
    single_process(files)
    pool_process(files)


