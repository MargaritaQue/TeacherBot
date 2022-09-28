import sqlite3

from typing import Dict

from model import Student, Subject
import config


class StudentDBStore:
    def find_by_id(self, id):
        student = None
        try:
            conn = sqlite3.connect(config.SQLITE_DB)
            cur = conn.cursor()
            cur.execute("SELECT * FROM student s WHERE s.id = " + str(id))
            student_db = cur.fetchone()
            student = Student(student_db[0], student_db[1])
            cur.execute("SELECT * FROM subject WHERE student_id = " + str(student.get_id()) + ";")
            subject_db_list = cur.fetchall()
            subjects = list()
            for row_subj in subject_db_list:
                subject = Subject(row_subj[0], row_subj[1])
                cur.execute("SELECT * FROM score WHERE subject_id = " + str(subject.get_id()) + ";")
                list_of_score_raw = cur.fetchall()
                score_list = list()
                for score in list_of_score_raw:
                    score_list.append(score[1])
                subject.set_score(score_list)
                subjects.append(subject)
            student.set_subjects(subjects)
            conn.close()
        except Exception as e:
            print(e)
        return student

    def find_all(self):
        students = list()
        try:
            conn = sqlite3.connect(config.SQLITE_DB)
            cur = conn.cursor()
            cur.execute("SELECT * FROM student")
            student_db_list = cur.fetchall()
            for row_stud in student_db_list:
                student = Student(row_stud[0], row_stud[1])
                cur.execute("SELECT * FROM subject WHERE student_id = " + str(student.get_id()) + ";")
                subject_db_list = cur.fetchall()
                subjects = list()
                for row_subj in subject_db_list:
                    subject = Subject(row_subj[0], row_subj[1])
                    cur.execute("SELECT * FROM score WHERE subject_id = " + str(subject.get_id()) + ";")
                    subject.set_score(cur.fetchall())
                    subjects.append(subject)
                student.set_subjects(subjects)
                students.append(student)
            conn.close()
        except Exception as e:
            print(e)
        return students

    def add_score_by_subject_id(self, subject_id: str, score: str):
        try:
            conn = sqlite3.connect(config.SQLITE_DB)
            cur = conn.cursor()
            cur.execute("INSERT INTO score(volume, subject_id)"
                        "VALUES (" + score +", " + subject_id +");")
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)