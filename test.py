from run import db, User

# 获取 User 和 UE 的 join 表
r = db.session.execute('SELECT `User`.`user_id` AS `attendee_id`, `User`.`username` AS `attendee_name`, `User_Event`.`event_id`, `User_Event`.`status`, `User_Event`.`form` FROM User INNER JOIN User_Event ON User.user_id=User_Event.attendee_id')

for row in r:
	print(row['attendee_name'])