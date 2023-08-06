import dis


class ServerMaker(type):
    """
    Метакласс, проверяющий что в результирующем классе нет клиентских
    вызовов таких как: connect. Также проверяется, что серверный
    сокет является TCP и работает по IPv4 протоколу.
    """

    def __init__(cls, clsname, bases, clsdict):
        # список методов используемых в функциях класса
        methods = []
        # атрибуты используемые в функциях классов
        attrs = []
        # перебираем ключи из словаря
        for func in clsdict:
            # Пробуем
            try:
                ret = dis.get_instructions(clsdict[func])
                # Если не функция то ловим исключение
            except TypeError:
                pass
            else:
                # Преребираем код, получая методы и атрибуты.
                for i in ret:
                    # print(i)
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            # добавляем в список методы, использующиеся в функциях класса
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            # Преребираем код, получая атрибуты.
                            attrs.append(i.argval)
        # print(methods)
        # Если обнаружено использование недопустимого метода connect,
        # бросаем исключение:
        if 'connect' in methods:
            raise TypeError(
                'Использование метода connect недопустимо в серверном классе')
        # Если сокет не инициализировался константами SOCK_STREAM(TCP)
        # AF_INET(IPv4), тоже исключение.
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')
        # Вызываем конструктор предка:
        super().__init__(clsname, bases, clsdict)


# # ClientMaker - метакласс для проверки корректности клиентов
# class ClientMaker(type):
#     """
#     Метакласс, проверяющий что в результирующем классе нет серверных
#     вызовов таких как: accept, listen. Также проверяется, что сокет не
#     создаётся внутри конструктора класса.
#     """
#
#     def __init__(cls, clsname, bases, clsdict):
#         # Список методов
#         methods = []
#         for func in clsdict:
#             # Пробуем
#             try:
#                 ret = dis.get_instructions(clsdict[func])
#                 # Если не функция, получаем исключение
#             except TypeError:
#                 pass
#             else:
#                 # У функции получаем используемые методы.
#                 for i in ret:
#                     if i.opname == 'LOAD_GLOBAL':
#                         if i.argval not in methods:
#                             methods.append(i.argval)
#         # Если обнаружено использование недопустимого метода accept, listen,
#         # socket вызываем исключение:
#         for command in ('accept', 'listen', 'socket'):
#             if command in methods:
#                 raise TypeError(
#                     'В классе обнаружено использование запрещённого метода')
#         # Вызов get_message или send_message из utils считаем корректным
#         # использованием сокетов
#         if 'get_message' in methods or 'send_message' in methods:
#             pass
#         else:
#             raise TypeError(
#                 'Отсутствуют вызовы функций, работающих с сокетами.')
#         super().__init__(clsname, bases, clsdict)
