from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import datetime


app = Flask(__name__)
app.secret_key = "pleasecanthisbeagoodsubmission"


class QAndABoard:
    def __init__(self, qanda_board_id, topic, creator):
        self.qanda_board_id = qanda_board_id
        self.topic = topic
        self.creator = creator


qanda_boards = [QAndABoard(1, "Computer Science", "Tutor1"),
                QAndABoard(2, "Mathematics", "Tutor2")]


class Question:
    # Set default values because when a question is created, there will be no answer, no likes, and no comments.
    def __init__(self, question_id, qanda_board_id, question, asker, date, answer="", likes=None, comments=None):
        if comments is None:
            comments = []
        if likes is None:
            likes = []
        self.question_id = question_id
        self. qanda_board_id = qanda_board_id
        self.question = question
        self.asker = asker
        self.date = date
        self.answer = answer

        self.likes = likes
        self.number_of_likes = len(self.likes)

        self.comments = comments
        self.number_of_comments = len(comments)


questions = [Question(1, 1, "How do I use HTML?", "Student1", "13/11/2021", "This is the answer on how to use HTML.",
                      ["Student1", "Student2", "Student3"], []),
             Question(2, 1, "Has the assignment been released yet?", "Student2", "15/11/2021", "",
                      ["Student2", "Student3"], [])]


credentials = [["Tutor1", "pass", True],
               ["Tutor2", "word", True],
               ["Student1", "stu", False],
               ["Student2", "dent", False]]


# Have the default path redirect to the login page.
@app.route("/", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check that both of the fields have been filled in.
        if request.form["username"] and request.form["password"]:
            username = request.form["username"]
            password = request.form["password"]
            usernames = []
            for credential in credentials:
                usernames.append(credential[0])
            if username in usernames:
                for credential in credentials:
                    if credential[0] == username:
                        if credential[1] == password:
                            session["user"] = username
                            return redirect(url_for("home"))
                        else:
                            print("Wrong password.")
                            flash("Wrong password.", "info")
                            return redirect(url_for("login"))
            else:
                # Create an account.
                credentials.append([username, password])
                session["user"] = username
                return redirect(url_for("home"))
        else:
            return render_template("login_template.html")
    else:
        # If the user is already logged in then redirect to home.
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("login_template.html")


@app.route("/home/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    else:
        return render_template("home_template.html")


@app.route("/logout/")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/qanda_board_select/")
def qanda_board_select():
    if "user" in session:
        return render_template("qanda_board_select_template.html", qanda_boards=qanda_boards)
    else:
        return redirect(url_for("login"))


@app.route("/qanda_board_select/create_qanda/", methods=['GET', 'POST'])
def create_qanda():
    if "user" in session:
        if request.method == "POST":
            # Check that the topic is not empty.
            if request.form["topic"]:
                qanda_board_ids = []
                for q in qanda_boards:
                    qanda_board_ids.append(q.qanda_board_id)
                potential_qanda_board_id = 1
                while True:
                    if potential_qanda_board_id in qanda_board_ids:
                        potential_qanda_board_id += 1
                    else:
                        break
                print("Q&A Board ID: " + str(potential_qanda_board_id))
                topic = request.form["topic"]
                print("Topic: " + topic)
                asker = session["user"]
                print("Asker: " + asker)
                qanda_board_object = QAndABoard(potential_qanda_board_id, topic, asker)
                qanda_boards.append(qanda_board_object)
            else:
                print("Please enter a topic.")
                flash("Please enter a topic.", "info")
                return render_template("create_qanda_template.html")
            return redirect(url_for("qanda_board_select"))
        else:
            return render_template("create_qanda_template.html")
    else:
        return redirect(url_for("login"))


@app.route("/<int:qanda_board_id>/delete/")
def delete_qanda(qanda_board_id):
    if "user" in session:
        for q in qanda_boards:
            if q.qanda_board_id == qanda_board_id:
                qanda_boards.remove(q)
        # Delete all questions associated with the Q&A board after it is deleted.
        # This is because new Q&A boards would take on the deleted Q&A boards ID, and would take the question data from
        # the deleted Q&A boards.
        # Do not loop over a list you are modifying.
        # This caused only half (rounded down) of the questions to be deleted.
        # Instead, a copy of the array, "questions", must be used.
        for question in questions[:]:
            if question.qanda_board_id == qanda_board_id:
                questions.remove(question)
        return redirect(url_for("qanda_board_select"))
    else:
        return redirect(url_for("login"))


# Need to use "int:" else a String is returned.
@app.route("/<int:qanda_board_id>/")
def qanda_board(qanda_board_id):
    if "user" in session:
        for q in qanda_boards:
            if q.qanda_board_id == qanda_board_id:
                valid_questions = []
                # Only pass questions that relate to the selected Q&A board.
                for question in questions:
                    if question.qanda_board_id == qanda_board_id:
                        valid_questions.append(question)
                # Pass the chosen Q&A board as well as the list of all valid questions.
                return render_template("qanda_board_template.html", qanda_board=q, questions=valid_questions)
        # If the passed ID is not found as a board, then redirect to "home".
        # Could create an error 404 page later.
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route("/<int:qanda_board_id>/ask_question/", methods=['GET', 'POST'])
def ask_question(qanda_board_id):
    if "user" in session:
        if request.method == "POST":
            # Check that the question is not empty.
            if request.form["question"]:
                question_ids = []
                for question in questions:
                    question_ids.append(question.question_id)
                potential_question_id = 1
                while True:
                    if potential_question_id in question_ids:
                        potential_question_id += 1
                    else:
                        break
                print("Question ID: " + str(potential_question_id))
                print("Q&A Board ID: " + str(qanda_board_id))
                question = request.form["question"]
                print("Question: " + question)
                asker = session["user"]
                print("Asker: " + asker)
                date = datetime.today().strftime('%d/%m/%Y')
                print("Date: " + date)
                question_object = Question(potential_question_id, qanda_board_id, question, asker, date)
                questions.append(question_object)
            else:
                print("Please enter a question.")
                flash("Please enter a question.", "info")
                return render_template("ask_question_template.html")
            return redirect(url_for("qanda_board", qanda_board_id=qanda_board_id))
        else:
            return render_template("ask_question_template.html")
    else:
        return redirect(url_for("login"))


@app.route("/<qanda_board_id>/<int:question_id>/")
def question_view(qanda_board_id, question_id):
    pass


@app.route("/<qanda_board_id>/<int:question_id>/answer/")
def answer_question(qanda_board_id, question_id):
    if "user" in session:
        answerer = session["user"]
        # Only tutors can answer questions.
        for credential in credentials:
            # "credential[0]" is the username.
            if credential[0] == answerer:
                # This checks that they are a tutor. As tutors have "True" in the third part of their array.
                if credential[2]:
                    # If there is no answer to the question currently.
                    for question in questions:
                        if question.question_id == question_id:
                            if question.answer == "":
                                # Let the tutor answer.
                                render_template("answer_question_template")
                            else:
                                # Redirect to the answer page.
                                render_template("answer_page_template.html")
                else:
                    # Redirect to the answer page.
                    render_template("answer_page_template.html")
        # for question in questions:
        #     if question.question_id == question_id:
        #         questions.remove(question)
        # return redirect(url_for("qanda_board", qanda_board_id=qanda_board_id))
    else:
        return redirect(url_for("login"))


@app.route("/<qanda_board_id>/<int:question_id>/delete/")
def delete_question(qanda_board_id, question_id):
    if "user" in session:
        for question in questions:
            if question.question_id == question_id:
                questions.remove(question)
        return redirect(url_for("qanda_board", qanda_board_id=qanda_board_id))
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
