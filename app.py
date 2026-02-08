from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login_docent")
def login_docent():
    return render_template("login_docent.html")

@app.route("/dashboard-student")
def student():
    return render_template("dashboard-student.html")

@app.route("/dashboard-docent")
def docent():
    return render_template("dashboard-docent.html")


if __name__ == "__main__":
    app.run(debug=True)
