from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


class QAndABoard:
    def __init__(self, qanda_board_id, name, creator):
        self.qanda_board_id = qanda_board_id
        self.name = name
        self.creator = creator


qanda_boards = [QAndABoard(1, "Class1", "Tutor1"),
                QAndABoard(2, "Class2", "Tutor2")]


@app.route("/")
def default():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username)
        print(password)
        return redirect(url_for("home"))
    else:
        return render_template("login_template.html")


@app.route("/home")
def home():
    return render_template("home_template.html")


@app.route("/qanda_board_select")
def qanda_board_select():
    return render_template("qanda_board_select_template.html", qanda_boards=qanda_boards)


@app.route("/<qanda_board_name>")
def qanda_board():
    return render_template("qanda_board_template.html")


if __name__ == "__main__":
    app.run(debug=True)
