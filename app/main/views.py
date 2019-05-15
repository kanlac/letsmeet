from flask import render_template, flash, url_for, session, redirect, request, jsonify
from ..models import User, Event, User_Event
from .. import db
from . import main
from .forms import ApplicationForm
from flask_login import current_user

@main.route('/', methods=['GET', 'POST'])
def index():
	if current_user.is_authenticated:
		events = Event.query.all()
		return render_template('index.html', events=events)
	flash("Please login first.")
	return redirect(url_for('auth.login'))

@main.route('/event/<event_id>')
def showEvent(event_id):
	e = Event.query.filter_by(event_id=event_id).first()
	host = User.query.filter_by(user_id=e.host_id).first()
	record = User_Event.query.filter_by(attendee_id=current_user.user_id, event_id=event_id).first()
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
	return render_template('event.html', host=host, e=e, statusTxt=statusTxt)

@main.route('/apply/<event_id>', methods=['GET', 'POST'])
def apply(event_id):
	applicationForm = ApplicationForm()
	event = Event.query.filter_by(event_id=event_id).first()
	attendee = current_user
	host = User.query.filter_by(user_id=event.host_id).first()
	if host == attendee:
		flash('不能申请参与自己的项目!')
		return redirect(url_for('.showEvent', event_id=event_id))
	if applicationForm.validate_on_submit(): # 提交申请表并且不为空
		if User_Event.query.filter_by(attendee_id=attendee.user_id, event_id=event_id).first() is not None:
			flash('不能重复提交.')
		else:
			record = User_Event(attendee_id=attendee.user_id, event_id=event_id, status=1, form=applicationForm.text.data)
			db.session.add(record)
			db.session.commit()
			flash('Success!')
		return redirect(url_for('.showEvent', event_id=event_id))
	return render_template('apply.html', event=event, form=applicationForm)

@main.route('/manageApplicants/<event_id>', methods=['GET'])
def showManagingTable(event_id):
	event = Event.query.filter_by(event_id=event_id).first()
	user = User.query.filter_by(user_id=event.host_id).first()
	print(user)
	print(current_user)

	if user.username is not current_user.username:
		flash('不是你发起的活动！')
		return redirect(url_for('.showEvent', event_id=event_id))

	rows = db.session.execute('SELECT `User`.`user_id` AS `attendee_id`,\
		`User`.`username` AS `attendee_name`,\
		`User_Event`.`ue_id`, `User_Event`.`event_id`, `User_Event`.`status`, `User_Event`.`form`\
		FROM User INNER JOIN User_Event\
		ON User.user_id=User_Event.attendee_id\
		WHERE event_id=:e', { "e": event.event_id })
	return render_template('manageApplicants.html', rows=rows)

@main.route('/operateAttendee')
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