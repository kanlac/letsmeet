from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, DateField
from wtforms.validators import DataRequired

#申请表表单类
class ApplicationForm(FlaskForm):
	text = StringField('申请书', validators=[DataRequired()])
	submit = SubmitField('提交')

class OriginatingForm(FlaskForm):
	title = StringField('活动名称', validators=[DataRequired()])
	description = StringField('活动简述', validators=[DataRequired()])
	city = StringField('城市', validators=[DataRequired()])
	location = StringField('地点', validators=[DataRequired()])
	date = DateField('日期', validators=[DataRequired()])
	quota_limit = DecimalField('期望人数')
	submit = SubmitField('提交')

