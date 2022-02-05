from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

questions = ["test", "best"]

@app.route("/")
def test():
    return redirect(url_for("qa_home"))


@app.route("/qa_home")
def qa_home():
    return render_template("qa_home_template.html", questions=questions)


if __name__ == "__main__":
    app.run(debug=True)
