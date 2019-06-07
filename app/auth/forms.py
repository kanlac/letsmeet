from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Regexp, EqualTo
from ..models import User

# 登录表单类
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Keep me logged in') # 「记住我」
	submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[DataRequired()])
	submit = SubmitField('Register')

	# 自定义 username 的 validator
	def validate_username(self, field): # 名称为 validate_FIELD 的方法，将会自动被视为该 field 的 validator
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')


class ChangePasswordForm(FlaskForm):
	old_password = PasswordField('Old password', validators=[DataRequired()])
	new_password = PasswordField('New password', validators=[DataRequired(), EqualTo('new_password2', message="Passwords aren't identical.")])
	new_password2 = PasswordField('Confirm password', validators=[DataRequired()])
	submit = SubmitField('Submit')