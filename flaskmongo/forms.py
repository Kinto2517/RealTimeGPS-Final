from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Kullanici Adi',
                        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Parola', validators=[DataRequired()])
    submit = SubmitField('Giris')
