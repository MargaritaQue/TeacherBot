import sqlite3

import requests

from service import StudentService
import config


class TelegramAPIConnectionException(Exception):
    pass


class PerformanceBot:
    def __init__(self):
        self.__controller = StudentService()
        self.__url = config.URL + config.TOKEN
        self.__offset = config.OFFSET
        self.__chat_id = config.CHAT_ID

    def __test_db(self):
        print('checking database... ', end='')
        with open(config.SQLITE_SCHEMA, 'r') as sql_file:
            sql_script = sql_file.read()
        conn = sqlite3.connect(config.SQLITE_DB)
        cur = conn.cursor()
        cur.executescript(sql_script)
        conn.close()
        print('done')

    def __text_connection(self):
        print('checking connection... ', end='')
        response = requests.get(self.__url + '/getMe').ok
        if not response:
            raise TelegramAPIConnectionException('Fail to connect ' + self.__url)
        print('done')

    def __init(self):
        try:
            self.__test_db()
            self.__text_connection()
        except Exception:
            print('fail')
            raise
        print('start')
        print('https://t.me/teacher_for_bot')

    def __send_message(self, message):
        url_send = self.__url + message
        requests.get(url_send)

    def __get_request(self):
        url_get = self.__url + '/getUpdates?offset=' + str(self.__offset)
        response = requests.get(url_get, timeout=30).json()
        return response['result']

    def run(self):
        self.__init()
        while True:
            result = self.__get_request()
            if len(result) > 0:
                update_id = result[len(result) - 1]['update_id']
                self.__offset = update_id + 1
                for update in result:
                    message = self.__controller.generate_message(update)
                    self.__send_message(message)
