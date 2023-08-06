# from errors import IncorrectDataRecivedError, NonDictInputError
import json
import sys

# from server.common.decos import log
from common.decos import log
# from server.common.variables import MAX_PACKAGE_LENGTH, ENCODING
# заменяем на:
from common.variables import *

# sys.path.append('../../')
sys.path.append('../')


# Утилита приёма и декодирования сообщения
# принимает байты выдаёт словарь, если приняточто-то другое отдаёт ошибку значения
@log
def get_message(client):
    """
    Функция приёма сообщений от удалённых компьютеров.
    Принимает сообщения JSON, декодирует полученное сообщение
    и проверяет что получен словарь.
    :param client: сокет для передачи данных.
    :return: словарь - сообщение.
    """
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    # if isinstance(encoded_response, bytes):
    json_response = encoded_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    else:
        # raise IncorrectDataRecivedError
        raise TypeError
    # else:
    # raise IncorrectDataRecivedError


# Утилита кодирования и отправки сообщения
# принимает словарь и отправляет его
@log
def send_message(sock, message):
    """
    Функция отправки словарей через сокет.
    Кодирует словарь в формат JSON и отправляет через сокет.
    :param sock: сокет для передачи
    :param message: словарь для передачи
    :return: ничего не возвращает
    """
    # уберём проверку на словарь
    # if not isinstance(message, dict):
    #     raise NonDictInputError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
