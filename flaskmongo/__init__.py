from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from pykafka import KafkaClient

from flaskmongo.forms import LoginForm

def get_kafka_client():
    return KafkaClient(hosts='localhost:9092')

app = Flask(__name__, template_folder="./templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SECRET_KEY'] = 'secret'
logindb = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskmongo.views import views
