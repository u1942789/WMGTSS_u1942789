import pytest
from classes import Question
from main import questions


question = Question(1, 1, "How do I use HTML?", "Student1", "13/11/2021", "This is the answer on how to use HTML.",
                    "Tutor1", "02/02/2022", str(["Student1", "Student2", "Student3"]), str([]))


def question_func(q):
    return q.question_id


def question_test():
    assert question.question_id == questions[0]

