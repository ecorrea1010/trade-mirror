from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from app.models.trades.strategy import Strategy

trades = Blueprint("trades", __name__)

@trades.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@trades.route("/history", methods=["GET"])
def history():
    return render_template("trades/history.html")

@trades.route("/register", methods=["GET", "POST"])
@login_required
def register():
    strategies = Strategy.query.order_by(Strategy.name).all()
 
    if request.method == "POST":
        # TODO: lógica de guardado — por ahora solo redirige
        flash("Operación registrada.", "success")
        return redirect(url_for("trades.history"))
 
    return render_template("trades/register.html", strategies=strategies)
 
 
@trades.route("/create", methods=["POST"])
@login_required
def create():
    # Aquí irá el servicio de creación cuando esté listo
    flash("Operación registrada.", "success")
    return redirect(url_for("trades.history"))
