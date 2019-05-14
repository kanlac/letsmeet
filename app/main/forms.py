from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

# 登录表单类
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')


#申请表表单类
class ApplicationForm(FlaskForm):
	text = StringField('申请书', validators=[DataRequired()])
	submit = SubmitField('提交')