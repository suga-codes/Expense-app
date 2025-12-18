from flask import Flask, render_template, request, redirect
import json
from datetime import date

app = Flask(__name__)
FILE = "expenses.json"

def load_expenses():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_expenses(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    expenses = load_expenses()

    if request.method == "POST":
        expense = {
            "amount": int(request.form["amount"]),
            "category": request.form["category"],
            "note": request.form["note"],
            "date": str(date.today())
        }
        expenses.append(expense)
        save_expenses(expenses)
        return redirect("/home")

    total = sum(e["amount"] for e in expenses)
    return render_template("index.html", expenses=expenses, total=total)

@app.route("/delete/<int:i>")
def delete(i):
    expenses = load_expenses()
    expenses.pop(i)
    save_expenses(expenses)
    return redirect("/home")

@app.route("/exit")
def exit():
    return render_template("exit.html")

if __name__ == "__main__":
    app.run()
