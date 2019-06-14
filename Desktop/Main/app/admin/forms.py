from flask_wtf import FlaskForm
from wtforms import Form,StringField, SubmitField, PasswordField, BooleanField, SelectField,validators
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email

from .admin import db

PERMISSION_CHOICES=[('admin-level1','admin-level1'),('admin-level2','admin-level2'),('admin-level3','admin-level3'),('admin-level4','admin-level4')]

# Auth forms
class LoginForm(FlaskForm):
    """Admin Login Form """
    username = StringField('Username', validators=[DataRequired()])
    pw = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    """ Registers new admin user with the app """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pw = PasswordField('Password', validators=[DataRequired()])
    pw2 = PasswordField('Repeat Password', validators=[DataRequired(),
                                                       EqualTo('pw')])
    has_perm = SelectField('Permission', choices=PERMISSION_CHOICES)
    secret_key = PasswordField('Secret Key')
    submit = SubmitField('Register')

    def validate_username(self, name):
        """ validates if a username exists """
        user = db.Admins.find_one({'username': name.data})
        if user is not None:
            raise ValidationError('Username already taken, Please use another one.')

    def validate_email(self, email):
        """ validates if an email address exists """
        email = db.Admins.find_one({'email': email.data})
        if email is not None:
            raise ValidationError('Email already in use, Please use another one.')


class CraftingForm(Form):
    craft_name = StringField('craft_name', [validators.DataRequired()])
    product_name = StringField('product_name', [validators.DataRequired()])
    possible_amount= StringField('possible_amount', [validators.DataRequired()])
    amount_awarded = StringField('amount_awarded', [validators.DataRequired()])
    per_of_dropRate = StringField('per_of_dropRate', [validators.DataRequired()])
    value = StringField('value',[validators.DataRequired()])


class CraftDataForm(Form):
    craft_name = StringField('craft_name', [validators.DataRequired()])


class SearchForm(Form):
    search = StringField('search', [validators.DataRequired()])