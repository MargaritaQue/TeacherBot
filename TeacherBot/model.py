from typing import List


class Subject:
    def __init__(self, id=0, name=None, score: List[int] = None):
        self.__score = score
        self.__name = name
        self.__id = id

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_score(self):
        return self.__score

    def set_score(self, score: List[int]):
        self.__score = score

    def __str__(self) -> str:
        return self.__name + ': ' + str(self.__score)


class Student:
    def __init__(self, id=0, name=None, subjects: List[Subject] = None):
        self.__name = name
        self.__id = id
        self.__subjects = subjects

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_subjects(self):
        return self.__subjects

    def set_subjects(self, subjects: List[Subject]):
        self.__subjects = subjects

    def __str__(self) -> str:
        return str(self.__id) + '. ' + self.__name



