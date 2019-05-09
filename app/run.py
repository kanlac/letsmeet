from flask import Flask, render_template, flash, url_for, session, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:tbu33p6r9@localhost/letsmeet'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'hard to guess string'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class User(db.Model):
	__tablename__ = 'User'

	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.NVARCHAR(50), unique=False, nullable=False)

	def __repr__(self): # debug 有效
		return '<User %r>' % self.username


class Event(db.Model):
	__tablename__ = 'Event'

	event_id = db.Column(db.Integer, primary_key=True)
	host_id = db.Column(db.ForeignKey("User.user_id"), nullable=False) # 不需要指定 type，因为指定了外键
	quota_limit = db.Column(db.SMALLINT, unique=False, nullable=True)
	title = db.Column(db.Unicode(40))
	description = db.Column(db.Unicode(256))
	city = db.Column(db.Unicode(40))
	location = db.Column(db.Unicode(256))
	date = db.Column(db.DATE)

	def __repr__(self):
		return '<Event %r>' % self.event_id


class User_Event(db.Model):
	__tablename__ = 'User_Event'

	ue_id = db.Column(db.Integer, primary_key=True)
	attendee_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)
	event_id = db.Column(db.Integer, db.ForeignKey("Event.event_id"), nullable=False)
	status = db.Column(db.SMALLINT, nullable=False) # 1 已申请，2 未通过，3 通过
	form = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return '<User_Event %r>' % self.ue_id

# 登录表单类
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Login')


#申请表表单类
class ApplicationForm(FlaskForm):
	text = StringField('申请书', validators=[Required()])
	submit = SubmitField('提交')



@app.route('/', methods=['GET', 'POST'])
def index():
	if session.get('loginas') is not None:
		events = Event.query.all()
		return render_template('index.html', loginas=session.get('loginas'), events=events)
	flash("Please login first.")
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit(): # 点击 Submit 后…
		user = User.query.filter_by(username=form.username.data).first() # 查看数据库中是否有这个用户名
		if user is None: # 没有，提示错误，请注册
			flash("User doesn't exist.")
		elif form.password.data == user.password: # 有则判断输入密码是否正确 
			session['loginas'] = user.username
			return redirect(url_for('index'))
		else:
			flash("Password is wrong.")
	return render_template('login.html', form=form)
	
@app.route('/logout')
def logout():
	session['loginas'] = None
	flash('You have been logged out.')
	return redirect(url_for('login'))

@app.route('/event/<event_id>')
def showEvent(event_id):
	e = Event.query.filter_by(event_id=event_id).first()
	host = User.query.filter_by(user_id=e.host_id).first()
	user = User.query.filter_by(username=session.get('loginas')).first()
	record = User_Event.query.filter_by(attendee_id=user.user_id, event_id=event_id).first()
	statusTxt = None
	if record is not None:
		if record.status is 1:
			statusTxt = '已申请'
		if record.status is 2:
			statusTxt = '未通过'
		if record.status is 3:
			statusTxt = '已通过'
	if statusTxt is not None:
		print('statusTxt is: ' + statusTxt)
	return render_template('event.html', loginas=session.get('loginas'), host=host, e=e, statusTxt=statusTxt)

@app.route('/apply/<event_id>', methods=['GET', 'POST'])
def apply(event_id):
	applicationForm = ApplicationForm()
	event = Event.query.filter_by(event_id=event_id).first()
	attendee = User.query.filter_by(username=session.get('loginas')).first()
	host = User.query.filter_by(user_id=event.host_id).first()
	if host == attendee:
		flash('不能申请参与自己的项目!')
		return redirect(url_for('showEvent', event_id=event_id))
	if applicationForm.validate_on_submit(): # 提交申请表并且不为空
		if User_Event.query.filter_by(attendee_id=attendee.user_id, event_id=event_id).first() is not None:
			flash('不能重复提交.')
		else:
			record = User_Event(attendee_id=attendee.user_id, event_id=event_id, status=1, form=applicationForm.text.data)
			db.session.add(record)
			db.session.commit()
			flash('Success!')
		return redirect(url_for('showEvent', event_id=event_id))
	return render_template('apply.html', loginas=session.get('loginas'), event=event, form=applicationForm)

@app.route('/manageApplicants/<event_id>', methods=['GET'])
def showManagingTable(event_id):
	event = Event.query.filter_by(event_id=event_id).first()
	user = User.query.filter_by(user_id=event.host_id).first()

	if user is not User.query.filter_by(username=session.get('loginas')).first():
		flash('不是你发起的活动！')
		return redirect(url_for('showEvent', event_id=event_id))

	rows = db.session.execute('SELECT `User`.`user_id` AS `attendee_id`,\
		`User`.`username` AS `attendee_name`,\
		`User_Event`.`ue_id`, `User_Event`.`event_id`, `User_Event`.`status`, `User_Event`.`form`\
		FROM User INNER JOIN User_Event\
		ON User.user_id=User_Event.attendee_id\
		WHERE event_id=:e', { "e": event.event_id })
	return render_template('manageApplicants.html', loginas=session.get('loginas'), rows=rows)

@app.route('/operateAttendee')
def operateAttendee():
	ue_id = request.args.get('ue_id', type=int)
	newStatus = request.args.get('newStatus', type=int)
	print("ue_id:" + str(ue_id))
	print(newStatus)
	# update database…
	record = User_Event.query.filter_by(ue_id=ue_id).one()
	print(record)
	record.status = newStatus
	db.session.commit()
	return jsonify(success=True)


if __name__ == '__main__':
	app.run(debug=True)