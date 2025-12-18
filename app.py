
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "expense-secret-key"from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "expense_secret_key"   # session ku

# Temporary user storage (database illa)
users = {}
@app.route("/")
def root():
    return redirect("/login")
    

# ------------------ REGISTER ------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return "User already exists 😕"

        users[username] = password
        return redirect(url_for("login"))

    return render_template("register.html")

# ------------------ LOGIN ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid username or password ❌"

    return render_template("login.html")

# ------------------ HOME ------------------
@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("home.html", user=session["user"])

# ------------------ LOGOUT ------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ------------------ EXIT PAGE (optional) ------------------
@app.route("/exit")
def exit():
    return render_template("exit.html")

# ------------------ RUN ------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
