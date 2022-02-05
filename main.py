from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


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
        return redirect(url_for("qanda_board_select"))
    else:
        return render_template("login_template.html")


@app.route("/home")
def home():
    return render_template("home_template.html")


@app.route("/qanda_board_select")
def qanda_board_select():
    return render_template("qanda_board_select_template.html")


@app.route("/qanda_board")
def qanda_board():
    return render_template("qanda_board_template.html")


if __name__ == "__main__":
    app.run(debug=True)
