from flask import Flask, redirect, url_for, render_template, request, session
from datetime import datetime


app = Flask(__name__)
app.secret_key = "pleasecanthisbeagoodsubmission"


class QAndABoard:
    def __init__(self, qanda_board_id, name, creator):
        self.qanda_board_id = qanda_board_id
        self.name = name
        self.creator = creator


qanda_boards = [QAndABoard(1, "Computer Science", "Tutor1"),
                QAndABoard(2, "Mathematics", "Tutor2")]


class Question:
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


credentials = ["Tutor1"]


# Have the default path redirect to the login page.
@app.route("/", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["user"] = username
        return redirect(url_for("home"))
    else:
        # If the user is already logged in then redirect to home.
        if "user" in session:
            return redirect(url_for("home"))
        return render_template("login_template.html")


@app.route("/home/")
def home():
    if "user" in session:
        return render_template("home_template.html")
    else:
        return redirect(url_for("login"))


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
            topic = request.form["topic"]
            print("Topic:" + topic)
            return redirect(url_for("qanda_board_select"))
        else:
            return render_template("create_qanda_template.html")
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
            return redirect(url_for("qanda_board", qanda_board_id=qanda_board_id))
        else:
            return render_template("ask_question_template.html")
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
