from classes import Question
from main import questions


# The data that is entered in the database.
question = Question(1, 1, "How do I use HTML?", "Student1", "13/11/2021", "This is the answer on how to use HTML.",
                    "Tutor1", "02/02/2022", str(["Student1", "Student2", "Student3"]), str([]))


def quest():
    return questions[0].question_id


def test_quest():
    assert quest() == question.question_id
