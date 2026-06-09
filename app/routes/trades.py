from flask import Blueprint, render_template

trades = Blueprint("trades", __name__)

@trades.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@trades.route("/history", methods=["GET"])
def history():
    return render_template("trades/history.html")
