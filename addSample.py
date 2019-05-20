def loadData(db):
	from app.models import User, Event, User_Event

	db.drop_all()
	db.create_all()

	jack = User(username='Jack', password='123456')
	jane = User(username='Jane', password='123456')
	jacob = User(username='Jacob', password='123456')
	jerry = User(username='Jerry', password='123456')
	jesse = User(username='Jesse', password='123456')
	josef = User(username='Josef', password='123456')
	jude = User(username='Jude', password='123456')
	jackson = User(username='Jackson', password='123456')
	jupiter = User(username='Jupiter', password='123456')

	db.session.add_all([jack, jane, jacob, jerry, jesse, josef, jude, jackson, jupiter])
	db.session.commit()

	hiking = Event(title="Let's go to Mountain Tai!", host_id=jane.user_id, \
		description="We wish you'll enjoy it~", city='Jinan', quota_limit=30, \
		location='Road 23', date='2019-05-30', poster='mountain.jpg')
	pythonConf = Event(title="Python Conference", host_id=jacob.user_id, \
		description="A conference for Python lovers.", city='Tianjin', quota_limit=100,  \
		location='Road 67', date='2019-08-10', poster='code.jpg')
	skateboardingDay = Event(title="World Skateboarding Day", host_id=jude.user_id, \
		description="All skaters in town, come celebrate the day!", city='Beijing', quota_limit=200, \
		location='XX Square', date='2019-06-21', poster='skateboarding.jpg')
	cycling = Event(title="Yuantong Mountain Riding", host_id=jerry.user_id, \
		description="We look for cycle lovers!", city='Kunming', quota_limit=14, \
		location='Yuantong Mountain', date='2019-12-07', poster='cycle.jpg')
	readingShareSession = Event(title="Reading Share Session", host_id=jacob.user_id, \
		description="New Book Sharing Session", city='Beijing', quota_limit=18, \
		location='Kubrick Book Store', date='2019-11-12', poster='bookstore.jpg')


	db.session.add_all([hiking, pythonConf, skateboardingDay, cycling, readingShareSession])
	db.session.commit()

	jackGoHiking = User_Event(attendee_id=jack.user_id, event_id=hiking.event_id, \
		status=1, form="I wanna join!")
	jesseGoPythonCof = User_Event(attendee_id=jesse.user_id, event_id=pythonConf.event_id, \
		status=1, form="Pythonist here~")
	jerryGoSkateboardingDay = User_Event(attendee_id=jerry.user_id, event_id=skateboardingDay.event_id, \
		status=1, form="A 3 years sk8er.")
	jerryGoReadingShareSession = User_Event(attendee_id=jerry.user_id, event_id=readingShareSession.event_id, \
		status=1, form="Excited about the new book!")
	janeGoReadingShareSession = User_Event(attendee_id=jane.user_id, event_id=readingShareSession.event_id, \
		status=1, form="I'm a fan of the author ;)")


	db.session.add_all([jackGoHiking, jesseGoPythonCof, jerryGoSkateboardingDay, jerryGoReadingShareSession, janeGoReadingShareSession])
	db.session.commit()


if __name__ == '__main__':
	from app import db, create_app
	app = create_app('development')
	app.app_context().push() # 要在该线程下激活(push)app 实例
	db.init_app(app)
	loadData(db)