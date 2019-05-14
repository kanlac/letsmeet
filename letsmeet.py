import os
from app import create_app, db
from app.models import User, Event, User_Event
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, Event=Event, User_Event=User_Event)