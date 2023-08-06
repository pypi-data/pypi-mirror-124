import os
import sys
import argparse
import logging
import configparser
import logs.config_server_log
# полный путь:
# from server.common.decos import log
# сокращённый путь:
from common.utils import *
from common.decos import log
from server.core import MessageProcessor
from server.database import ServerStorage
# from server.common.variables import DEFAULT_PORT
from server.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt

# Инициализация логирования сервера.
logger = logging.getLogger('server')


# Парсер аргументов коммандной строки.
@log
def arg_parser(default_port, default_address):
    """
    Парсер аргументов коммандной строки.
    """
    logger.debug(
        f'Инициализация парсера аргументов коммандной строки: {sys.argv}')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('--no_gui', action='store_true')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    gui_flag = namespace.no_gui
    logger.debug('Аргументы успешно загружены.')
    # вынесем проверку порта в файл "дескриптор" класса "Port"
    # # проверка получения корретного номера порта для работы сервера.
    # if not 1023 < listen_port < 65536:
    #     logger.critical(
    #         f'Попытка запуска сервера с указанием неподходящего порта {listen_port}. Допустимы адреса с 1024 до 65535.')
    #     exit(1)
    return listen_address, listen_port, gui_flag


@log
def config_load():
    """
    Загрузка файла конфигурации.
    Парсер конфигурационного ini файла.
    """
    config = configparser.ConfigParser()
    # определяем путь(директорию) до файла
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # перед размещением в проде убираем обращения
    # к "os.path.realpath(__file__)" заменяя на "os.getcwd()"
    dir_path = os.getcwd()
    # читаем файл парсером
    config.read(f"{dir_path}/{'server.ini'}")
    # Если конфиг файл загружен правильно, запускаемся, иначе конфиг по умолчанию.
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        # config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Default_port', DEFAULT_PORT)
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'server_database.db3')
        return config

@log
def main():
    """
    Основная функция
    """
    # Загрузка файла конфигурации сервера
    # config = configparser.ConfigParser()
    config = config_load()

    # вынесли в config_load()
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # config.read(f"{dir_path}/{'server.ini'}")

    # Загрузка параметров командной строки, если нет параметров, то задаём
    # значения по умоланию.
    listen_address, listen_port, gui_flag = arg_parser(
        config['SETTINGS']['Default_port'], config['SETTINGS']['Listen_Address'])

    # Инициализация базы данных
    # database = ServerStorage()
    database = ServerStorage(
        os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file']))

    # Создание экземпляра класса - сервера и его запуск.
    # server = Server(listen_address, listen_port)
    # server = Server(listen_address, listen_port, database)
    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()
    # server.main_loop()

    # Печатаем справочное меню:
    # print_help()

    # Если  указан параметр без GUI то запускаем простенький обработчик
    # консольного ввода
    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            if command == 'exit':
                # Если выход, то завршаем основной цикл сервера.
                server.running = False
                server.join()
                break
    # Если не указан запуск без GUI, то запускаем GUI:
    else:
        # Создаём графическое окуружение для сервера:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)
        # server_app.MainWindow(database, server, config)

        # Запускаем GUI
        server_app.exec_()

        # По закрытию окон останавливаем обработчик сообщений
        server.running = False


if __name__ == '__main__':
    main()
