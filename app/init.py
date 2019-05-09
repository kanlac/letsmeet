def refreshSampleData(db):
	from run import User, Event, User_Event

	db.drop_all()
	db.create_all()

	jack = User(username='Jack', password='123456')
	jane = User(username='Jane', password='123456')
	jacob = User(username='Jacob', password='123456')

	db.session.add_all([jack, jane, jacob])
	db.session.commit()

	hiking = Event(title="Let's go to Mount Tai!", host_id=jane.user_id, description="We wish you'll enjoy it~", city='Jinan', location='Road 23', date='2019-05-30')
	pythonConf = Event(title="Python Conference", host_id=jacob.user_id, description="A conference for Python lovers.", city='Tianjin', location='Road 67', date='2019-08-10')

	db.session.add_all([hiking, pythonConf])
	db.session.commit()

	jackGoHiking = User_Event(attendee_id=jack.user_id, event_id=hiking.event_id, status=1, form="I wanna join!")

	db.session.add(jackGoHiking)
	db.session.commit()

	# print(jack.username)