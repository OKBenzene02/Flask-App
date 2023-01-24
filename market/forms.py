from flask_wtf import FlaskForm
from wtforms import StringField, SearchField, SelectField, SubmitField, PasswordField
from wtforms.validators import Length, Email, EqualTo, InputRequired, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    def validate_name(self, user_to_check):
        name = User.query.filter_by(user=user_to_check.data).first()

        if name:
            raise ValidationError('Username already exists! Please try a different Username.')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()

        if email:
            raise ValidationError('Email address already exists! Please try a different Email address')

    name = StringField(label='Name', validators=[Length(min=5, max=30), DataRequired()])
    email = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=5), DataRequired()])
    password2 = PasswordField(label='Confirm Password',  validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    password_login = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign-In')


class PurchaseItem(FlaskForm):
    submit = SubmitField(label='Purchase Item!')


class SellItem(FlaskForm):
    submit = SubmitField(label='Sell Item!')