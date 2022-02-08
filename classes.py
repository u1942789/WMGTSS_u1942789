class Account:
    def __init__(self, username, password, is_admin=0):
        self.username = username
        self.password = password
        self.is_admin = is_admin


class QAndABoard:
    def __init__(self, qanda_board_id, topic, creator):
        self.qanda_board_id = qanda_board_id
        self.topic = topic
        self.creator = creator


class Question:
    # Set default values because when a question is created.
    # There will be no answer, no answerer, no answer date, no likes, and no comments.
    def __init__(self, question_id, qanda_board_id, question, asker, date,
                 answer="", answerer="", answer_date="",
                 likes=[], comments=[]):
        # Primary key.
        self.question_id = question_id
        # Foreign key.
        self.qanda_board_id = qanda_board_id
        # Initial data.
        self.question = question
        self.asker = asker
        self.date = date
        # Answer data.
        self.answer = answer
        self.answerer = answerer
        self.answer_date = answer_date
        # Likes.
        self.likes = likes
        self.number_of_likes = len(self.likes)
        # Comments.
        self.comments = comments
        self.number_of_comments = len(comments)
