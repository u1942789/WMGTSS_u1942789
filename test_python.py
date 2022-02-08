import pytest

from classes import Question


# @pytest.fixture

def question_tester():
    return Question()


def question_test():
    return Question("")
