from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
	__tablename__ = 'User'

	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self): # debug 有效
		return '<User %r>' % self.username

	def get_id(self): # flask-login 回调函数只能识别名字'id'，因此这里需要手动定义
		return (self.user_id)


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
	poster = db.Column(db.Unicode(256))

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


# flask-login 的回调函数
@login_manager.user_loader # user_loader 是自定义的名字吗？
def load_user(user_id):
	return User.query.get(int(user_id)) # SQLAlchemy 指令的 get() 方法，直接以 id 的 int 值为参数查询