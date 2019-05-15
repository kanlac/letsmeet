from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#申请表表单类
class ApplicationForm(FlaskForm):
	text = StringField('申请书', validators=[DataRequired()])
	submit = SubmitField('提交')