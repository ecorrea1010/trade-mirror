from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit   = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    first_name = StringField('Nombres', validators=[DataRequired()])
    last_name = StringField('Apellidos', validators=[DataRequired()])
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Correo', validators=[DataRequired(), Email()])
    timezone = SelectField('Zona horaria', choices=[
        ('America/Bogota',      '(UTC-5) Bogotá, Lima, Quito'),
        ('America/New_York',    '(UTC-5) Nueva York, Toronto'),
        ('America/Chicago',     '(UTC-6) Chicago, Ciudad de México'),
        ('America/Los_Angeles', '(UTC-8) Los Ángeles, Vancouver'),
        ('America/Sao_Paulo',   '(UTC-3) São Paulo, Buenos Aires'),
        ('Europe/London',       '(UTC+0) Londres, Dublín'),
        ('Europe/Madrid',       '(UTC+1) Madrid, Berlín, París'),
        ('Asia/Shanghai',       '(UTC+8) Pekín, Singapur'),
        ('Asia/Tokyo',          '(UTC+9) Tokio, Seúl'),
    ])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Repetir contraseña', validators=[
        DataRequired(),
        EqualTo('password', message='Las contraseñas no coinciden')
    ])
    submit = SubmitField('Registrarse')
