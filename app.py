from flask import render_template

from backend import create_app

app = create_app()


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)