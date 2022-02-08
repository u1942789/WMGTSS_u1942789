from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import datetime
import sqlite3
from classes import QAndABoard, Account, Question


app = Flask(__name__)
app.secret_key = "havefun"


accounts = []
qanda_boards = []
questions = []


def update_accounts_array():
    accounts.clear()
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute('SELECT * FROM accounts')
    for row in c:
        accounts.append(Account(row[0], row[1], row[2]))
    conn.close()


def update_accounts_database():
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("DELETE FROM accounts")
    for account in accounts:
        c.execute("INSERT INTO accounts VALUES (?, ?, ?)", (account.username, account.password, account.is_admin))
        conn.commit()
    conn.close()


def update_qanda_boards_array():
    qanda_boards.clear()
    conn = sqlite3.connect("qanda_boards.db")
    c = conn.cursor()
    c.execute('SELECT * FROM qanda_boards')
    for row in c:
        qanda_boards.append(QAndABoard(row[0], row[1], row[2]))
    conn.close()


def update_qanda_boards_database():
    conn = sqlite3.connect("qanda_boards.db")
    c = conn.cursor()
    c.execute("DELETE FROM qanda_boards")
    for q in qanda_boards:
        c.execute("INSERT INTO qanda_boards VALUES (?, ?, ?)", (q.qanda_board_id, q.topic, q.creator))
        conn.commit()
    conn.close()


def update_questions_array():
    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    c.execute('SELECT * FROM questions')
    questions.clear()
    for row in c:
        questions.append(Question(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
        conn.commit()
    conn.close()


def update_questions_database():
    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    c.execute("DELETE FROM questions")
    for question in questions:
        c.execute("INSERT INTO questions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            question.question_id, question.qanda_board_id, question.question, question.asker, question.date,
            question.answer, question.answerer, question.answer_date, str(question.likes), str(question.comments)))
    conn.close()


# Bring up-to-date information from the database into Python.
update_accounts_array()
update_qanda_boards_array()
update_questions_array()


def update_database():
    update_accounts_database()
    update_qanda_boards_database()
    update_questions_database()


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
            for account in accounts:
                usernames.append(account.username)
            if username in usernames:
                for account in accounts:
                    if account.username == username:
                        if account.password == password:
                            session["user"] = username
                            return redirect(url_for("home"))
                        else:
                            flash("Wrong password.", "info")
                            return redirect(url_for("login"))
            else:
                # Create an account.
                accounts.append(Account(username, password, 0))
                session["user"] = username
                update_database()
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
    if "user" not in session:
        return redirect(url_for("login"))
    else:
        return render_template("qanda_board_select_template.html", qanda_boards=qanda_boards)


@app.route("/qanda_board_select/create_qanda/", methods=['GET', 'POST'])
def create_qanda():
    if "user" not in session:
        return redirect(url_for("login"))
    else:
        for account in accounts:
            if session["user"] == account.username:
                # Only tutors can create Q&As.
                if account.is_admin:
                    # Make sure the tutor doesn't already have 2 boards.
                    board_count = 0
                    for q in qanda_boards:
                        if q.creator == account.username:
                            board_count += 1
                    if board_count <= 1:
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
                                topic = request.form["topic"]
                                asker = session["user"]
                                qanda_board_object = QAndABoard(potential_qanda_board_id, topic, asker)
                                qanda_boards.append(qanda_board_object)
                                update_database()
                            else:
                                flash("Please enter a topic.", "info")
                                return render_template("create_qanda_template.html")
                            return redirect(url_for("qanda_board_select"))
                        else:
                            return render_template("create_qanda_template.html")
                    else:
                        flash("You have already created 2 Q&As.", "info")
                        return redirect(url_for("qanda_board_select"))
        return redirect(url_for("qanda_board_select"))


@app.route("/<int:qanda_board_id>/delete/")
def delete_qanda(qanda_board_id):
    if "user" not in session:
        return redirect(url_for("login"))
    else:
        for account in accounts:
            if session["user"] == account.username:
                if account.is_admin:
                    for q in qanda_boards:
                        if q.qanda_board_id == qanda_board_id:
                            qanda_boards.remove(q)
                    # Delete all questions associated with the Q&A board after it is deleted.
                    # This is because new Q&A boards would take on the deleted Q&A boards ID, and would take the
                    # question data from the deleted Q&A boards.
                    # Do not loop over a list you are modifying.
                    # This caused only half (rounded down) of the questions to be deleted.
                    # Instead, a copy of the array, "questions", must be used.
                    for question in questions[:]:
                        if question.qanda_board_id == qanda_board_id:
                            questions.remove(question)
                    update_database()
                    return redirect(url_for("qanda_board_select"))
        return redirect(url_for("qanda_board_select"))


# Need to use "int:" else a String is returned.
@app.route("/<int:qanda_board_id>/")
def qanda_board(qanda_board_id):
    if "user" not in session:
        return redirect(url_for("login"))
    else:
        for q in qanda_boards:
            if q.qanda_board_id == qanda_board_id:
                valid_questions = []
                # Only pass questions that relate to the selected Q&A board.
                for question in questions:
                    if question.qanda_board_id == qanda_board_id:
                        valid_questions.append(question)
                # Pass the chosen Q&A board as well as the list of all valid questions.
                return render_template("qanda_board_template.html", username=session["user"], qanda_board=q,
                                       questions=valid_questions)
        # If the passed ID is not found as a board, then redirect to "home".
        # Could create an error 404 page later.
        return redirect(url_for("home"))


@app.route("/<int:qanda_board_id>/ask_question/", methods=['GET', 'POST'])
def ask_question(qanda_board_id):
    if "user" not in session:
        return redirect(url_for("login"))
    else:
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
                question = request.form["question"]
                asker = session["user"]
                date = datetime.today().strftime('%d/%m/%Y')
                question_object = Question(potential_question_id, qanda_board_id, question, asker, date)
                questions.append(question_object)
                update_database()
            else:
                flash("Please enter a question.", "info")
                return render_template("ask_question_template.html", qanda_board_id=qanda_board_id)
            return redirect(url_for("qanda_board", qanda_board_id=qanda_board_id))
        else:
            return render_template("ask_question_template.html", qanda_board_id=qanda_board_id)


@app.route("/<int:qanda_board_id>/<int:question_id>/")
def view_answer(qanda_board_id, question_id):
    if "user" not in session:
        return redirect(url_for("login"))
    else:
        for question in questions:
            if question.question_id == question_id:
                return render_template("view_answer_template.html", qanda_board_id=qanda_board_id, question=question)


@app.route("/<int:qanda_board_id>/<int:question_id>/answer/", methods=["GET", "POST"])
def answer_question(qanda_board_id, question_id):
    if "user" not in session:
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            # Check the answer is not empty.
            if request.form["answer"]:
                for question in questions:
                    if question.question_id == question_id:
                        question.answer = request.form["answer"]
                        update_database()
                return redirect(url_for("view_answer", qanda_board_id=qanda_board_id, question_id=question_id))
            else:
                flash("Please enter an answer.", "info")
                return render_template("answer_question_template.html", qanda_board_id=qanda_board_id,
                                       question_id=question_id)
        else:
            for question in questions:
                if question.question_id == question_id:
                    if question.answer == "":
                        return render_template("answer_question_template.html", qanda_board_id=qanda_board_id,
                                               question_id=question_id)
                    else:
                        return redirect(url_for("view_answer", qanda_board_id=qanda_board_id, question_id=question_id))


@app.route("/<int:qanda_board_id>/<int:question_id>/delete/")
def delete_question(qanda_board_id, question_id):
    if "user" in session:
        for account in accounts:
            if session["user"] == account.username:
                # Tutors can delete all questions.
                if account.is_admin:
                    for question in questions:
                        if question.question_id == question_id:
                            questions.remove(question)
                            update_database()
                    return redirect(url_for("qanda_board", qanda_board_id=qanda_board_id))
                # Students can delete a question if it is theirs.
                for question in questions:
                    if question.question_id == question_id:
                        if question.asker == account.username:
                            questions.remove(question)
                            update_database()
                            return redirect(url_for("qanda_board", qanda_board_id=qanda_board_id))
        return redirect(url_for("qanda_board", qanda_board_id=qanda_board_id))
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
    # app.run()
