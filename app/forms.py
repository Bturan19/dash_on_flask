from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', 
    	validators=[DataRequired()], 
    	render_kw={"placeholder": "Username"})
    password = PasswordField('Password', 
    	validators=[DataRequired()], 
    	render_kw={"placeholder":"Password"})
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
    	validators=[DataRequired()],
    	render_kw={"placeholder": "Username"})
    password = PasswordField('Password', 
    	validators=[DataRequired()],
    	render_kw={"placeholder":"Password"})
    submit = SubmitField('Register')
