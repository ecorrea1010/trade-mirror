from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm
from app.extensions import FakeUser
from flask import session
#from app.models.user import User  # cuando tengas el modelo, por ahora lo dejamos comentado

auth = Blueprint("auth", __name__)

@auth.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username == "admin" and password == "1234":
            session["fake_logged_in"] = True
            login_user(FakeUser())
            return redirect(url_for("trades.dashboard"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("auth/login.html", form=form, full_width=True)


@auth.route("/logout")
@login_required
def logout():
    session.pop("fake_logged_in", None)
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # lógica de DB viene después
        flash("Cuenta creada exitosamente. Inicia sesión.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)
