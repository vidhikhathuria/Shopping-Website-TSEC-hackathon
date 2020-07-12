from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
import nexmo
from flask_mail import Mail
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///track.db'
app.config['SECRET_KEY'] = 'sfjwrjkfm279hr23iujkd'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
socket = SocketIO(app,cors_allowed_origins="*")
CORS(app)
trackData = ["dummy"]
client = nexmo.Client(
  application_id='e465d03f-f8cf-46f2-9d2d-880bc30995e1',
  private_key='C:\\Python_Projects\\basic\\private.key',
)
cli = nexmo.Client(key='62abeb73', secret= os.environ.get('nexmo_secret'))
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('USER')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
mail = Mail(app)





from track import routes, models
