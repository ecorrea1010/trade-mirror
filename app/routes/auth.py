from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from flask import session
from app.forms import LoginForm, RegisterForm
from app.extensions import FakeUser, db
from app.models.user import User, UserProfile, UserRole, Role
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

        # Validar username único
        if User.query.filter_by(username=form.username.data).first():
            flash("El nombre de usuario ya está en uso.", "danger")
            return render_template("auth/register.html", form=form)

        # Validar email único
        if User.query.filter_by(email=form.email.data).first():
            flash("El correo ya está registrado.", "danger")
            return render_template("auth/register.html", form=form)

        # Buscar rol trader por defecto
        rol_trader = Role.query.filter_by(name="trader").first()
        if not rol_trader:
            flash("Error de configuración: rol trader no encontrado.", "danger")
            return render_template("auth/register.html", form=form)

        try:
            # Crear usuario
            user = User(
                username = form.username.data,
                email    = form.email.data,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.flush()  # genera el UUID sin hacer commit

            # Crear perfil
            profile = UserProfile(
                user_id    = user.id,
                first_name = form.first_name.data,
                last_name  = form.last_name.data,
                time_zone  = form.timezone.data,
            )
            db.session.add(profile)

            # Asignar rol trader
            user_role = UserRole(
                user_id = user.id,
                role_id = rol_trader.id,
            )
            db.session.add(user_role)

            db.session.commit()
            flash("Cuenta creada exitosamente. Inicia sesión.", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            db.session.rollback()
            flash("Ocurrió un error al crear la cuenta. Intenta de nuevo.", "danger")

    return render_template("auth/register.html", form=form)
