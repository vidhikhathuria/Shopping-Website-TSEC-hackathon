from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class WarehouseRegistrationForm(FlaskForm):
	name = StringField('Warehouse Name', validators=[DataRequired()])
	email = StringField('Email Address', validators = [DataRequired()])
	password = PasswordField('New Password', validators = [DataRequired()])
	confirm = PasswordField('Repeat Password', validators = [
	    DataRequired(),
	    EqualTo('confirm', message='Passwords must match')
	])
	x = StringField('x-coordinate', validators=[DataRequired()])
	y = StringField('y-coordinate', validators=[DataRequired()])
	submit = SubmitField('Submit')

class warehouseLoginForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')
		
class EmptyForm(FlaskForm):
	submit = SubmitField('Submit')