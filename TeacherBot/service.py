import json
from typing import Dict

import config
from store import StudentDBStore
from telegram_ui import Message, KeyboardMarkup, Button


class StudentService:
    def __init__(self):
        self.__message_id = None
        self.__store = StudentDBStore()

    def __main_menu(self, chat_id):
        students = self.__store.find_all()
        keyboard = KeyboardMarkup()
        for student in students:
            data = 'student_menu:' + str(student.get_id())
            button = Button(student.get_name(), data)
            keyboard.add_button([button.get()])
        button_help = Button('Помощь', 'help_list')
        keyboard.add_button([button_help.get()])
        return Message(chat_id).reply('Список учеников', keyboard)

    def __students_list(self, chat_id):
        students = self.__store.find_all()
        keyboard = KeyboardMarkup()
        for student in students:
            data = 'student_menu:' + str(student.get_id())
            button = Button(student.get_name(), data)
            keyboard.add_button([button.get()])
        button_help = Button('Помощь', 'help_list')
        keyboard.add_button([button_help.get()])
        return Message(chat_id).edit(self.__message_id, 'Список учеников', keyboard)

    def __help_list(self, chat_id):
        text = """Помощь в навигации.

Для того, чтобы узнать успеваемость ученика, выберите его имя в списке и нажмите на кнопку "Успеваемость". 

Чтобы поставить оценку ученику, выберите его имя в списке и нажмите на кнопку "Добавить оценку", далее выберите необходимый Вам предмет и оценку.

Кнопка "Вернуться" поможет Вам выйти в главное меню.
"""
        keyboard = KeyboardMarkup()
        button_back = Button('Вернуться', 'main_menu')
        keyboard.add_button([button_back.get()])
        return Message(chat_id).edit(self.__message_id, text, keyboard)

    def __student_info(self, chat_id, data):
        text = self.__get_by_id(int(data[1]))
        keyboard = KeyboardMarkup()
        button_back = Button('Вернуться', 'student_menu:' + data[1])
        keyboard.add_button([button_back.get()])
        return Message(chat_id).edit(self.__message_id, text, keyboard)

    def __student_menu(self,chat_id, data):
        student = self.__store.find_by_id(int(data[1]))
        text = student.get_name()
        keyboard = KeyboardMarkup()
        button1 = Button('Успеваемость', 'student_info:' + str(student.get_id()))
        button2 = Button('Добавить оценку', 'student_edit_menu:' + str(student.get_id()))
        button_back = Button('Вернуться', 'main_menu')
        keyboard.add_button([button1.get()])
        keyboard.add_button([button2.get()])
        keyboard.add_button([button_back.get()])
        return Message(chat_id).edit(self.__message_id, text, keyboard)

    def __student_edit_menu(self, chat_id, data):
        student = self.__store.find_by_id(int(data[1]))
        subjects = student.get_subjects()
        text = student.get_name()
        keyboard = KeyboardMarkup()
        for subject in subjects:
            button = Button(subject.get_name(), 'student_subject_score_menu:' + data[1] + ':' + str(subject.get_id()))
            keyboard.add_button([button.get()])
        button_back = Button('Вернуться', 'student_menu:' + str(student.get_id()))
        keyboard.add_button([button_back.get()])
        return Message(chat_id).edit(self.__message_id, text, keyboard)

    def __student_subject_score_menu(self, chat_id, data):
        keyboard = KeyboardMarkup()
        button_score_list = []
        for i in range(1, 6):
            button_score_list.append(Button(str(i), 'student_subject_score_add:' + data[1] + ':'+ data[2] + ':' + str(i)).get())
        keyboard.add_button(button_score_list)
        button_back = Button('Вернуться', 'student_edit_menu:' + data[1])
        keyboard.add_button([button_back.get()])
        return Message(chat_id).edit(self.__message_id, 'Выберете оценку', keyboard)

    def __student_subject_score_add(self, chat_id, data):
        self.__store.add_score_by_subject_id(data[2], data[3])
        keyboard = KeyboardMarkup()
        button_back = Button('Вернуться', 'student_edit_menu:' + data[1])
        keyboard.add_button([button_back.get()])
        return Message(chat_id).edit(self.__message_id, 'Добавлено: ' + data[3], keyboard)

    def __get_by_id(self, id):
        student = self.__store.find_by_id(id)
        if student is None:
            return ''
        result = str(student) + '\n'
        for subject in student.get_subjects():
            result += str(subject) + '\n'
        return result

    def generate_message(self, update: Dict):
        message = '&text='
        if 'callback_query' in update:
            self.__message_id = update['callback_query']['message']['message_id']
            data = update['callback_query']['data'].split(':')
            chat_id = update['callback_query']['message']['chat']['id']
            if data[0] == 'main_menu':
                message = self.__students_list(chat_id)
            if data[0] == 'help_list':  # help
                message = self.__help_list(chat_id)
            if data[0] == 'students_list':
                message = self.__students_list(chat_id)
            if data[0] == 'student_menu':
                message = self.__student_menu(chat_id, data)
            if data[0] == 'student_info':
                message = self.__student_info(chat_id, data)
            if data[0] == 'student_edit_menu':
                message = self.__student_edit_menu(chat_id, data)
            if data[0] == 'student_subject_score_menu':
                message = self.__student_subject_score_menu(chat_id, data)
            if data[0] == 'student_subject_score_add':
                message = self.__student_subject_score_add(chat_id, data)
        if 'message' in update:
            text: str = update['message']['text']
            chat_id = update['message']['chat']['id']
            if text == '/start':
                message = self.__main_menu(chat_id)
        return message
