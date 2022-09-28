import json


class Button:
    def __init__(self, text: str, callback_query: str):
        self.__button = {'text': text, "callback_data": callback_query}

    def get(self):
        return self.__button


class KeyboardMarkup:
    def __init__(self):
        self.__board = {'inline_keyboard': []}

    def add_button(self, buttons):
        self.__board['inline_keyboard'].append(buttons)

    def get(self):
        return self.__board


class Message:
    def __init__(self, chat_id: int):
        self.__chat_id = chat_id

    def reply(self, text: str, keyboard: KeyboardMarkup = None):
        return '/sendMessage?chat_id=' + str(self.__chat_id) + '&text=' + text \
               + '&reply_markup=' + json.dumps(keyboard.get(), indent=5) if keyboard is not None else ''

    def edit(self, message_id: int, text: str, keyboard: KeyboardMarkup = None):
        return '/editMessageText?chat_id=' + str(self.__chat_id) \
               + '&message_id=' + str(message_id) \
               + '&text=' + text \
               + '&reply_markup=' + json.dumps(keyboard.get(), indent=5) if keyboard is not None else ''
