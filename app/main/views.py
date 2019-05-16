from flask import render_template, flash, url_for, session, redirect, request, jsonify
from ..models import User, Event, User_Event
from .. import db
from . import main
from .forms import ApplicationForm
from flask_login import current_user, login_required

@main.route('/', methods=['GET', 'POST'])
def index():
	if current_user.is_authenticated:
		events = Event.query.all()
		return render_template('index.html', events=events)
	flash("Please login first.")
	return redirect(url_for('auth.login'))

@main.route('/event/<event_id>')
@login_required
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
	return render_template('event.html', host=host, e=e, statusTxt=statusTxt)

@main.route('/apply/<event_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def showManagingTable(event_id):
	event = Event.query.filter_by(event_id=event_id).first()
	user = User.query.filter_by(user_id=event.host_id).first()

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
@login_required
def operateAttendee():
	ue_id = request.args.get('ue_id', type=int)
	newStatus = request.args.get('newStatus', type=int)
	# update database…
	record = User_Event.query.filter_by(ue_id=ue_id).one()
	record.status = newStatus
	db.session.commit()
	return jsonify(success=True)

@main.route('/hostings')
@login_required
def showHostings():
	hostings = Event.query.filter_by(host_id=current_user.user_id).all()
	return render_template('hostings.html', hostings=hostings)