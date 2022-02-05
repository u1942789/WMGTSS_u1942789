from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Might not be able to implement the reply feature.
# Might not be able to implement comment liking.
# May require a comment database.
questions = [
    # Question ID, Question Name, Question Asker, Date, Answer, Comments, Likes
    [1, "How do I use HTML?", "Joe, M.", "13/11/2021", "This is the answer.", ["Comment 1", "Comment 2"], ["User1", "User2", "User3"]],
    [2, "Has the assignment been released yet?", "Ben, D.", "15/11/2021", "This is the answer.", [], ["User2", "User3"]]
]


@app.route("/")
def test():
    return redirect(url_for("login"))


@app.route("/qa_home")
def qa_home():
    return render_template("qa_home_template.html", questions=questions)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username)
        print(password)
        return render_template("home_template.html")
    else:
        return render_template("login_template.html")


if __name__ == "__main__":
    app.run(debug=True)
